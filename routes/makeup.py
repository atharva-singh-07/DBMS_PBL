from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import date
from routes.auth import login_required, role_required
from database import query_all, query_one, execute, execute_transaction, log_audit

makeup_bp = Blueprint('makeup', __name__)

@makeup_bp.route('/makeup')
@login_required
def index():
    role = session.get('role')
    faculty_id = session.get('faculty_id')
    student_id = session.get('student_id')

    try:
        if role == 'student':
            # View makeup sessions for enrolled courses
            makeups = query_all("""
                SELECT ms.*, sec.section_name, c.course_code, c.course_title, f.full_name AS faculty_name,
                       ma.status AS my_attendance_status
                FROM makeup_sessions ms
                JOIN sections sec ON ms.section_id = sec.section_id
                JOIN courses c ON sec.course_id = c.course_id
                JOIN faculty f ON ms.faculty_id = f.faculty_id
                JOIN enrollments e ON sec.section_id = e.section_id
                LEFT JOIN makeup_attendance ma ON ma.makeup_id = ms.makeup_id AND ma.student_id = %s
                WHERE e.student_id = %s AND e.status = 'enrolled'
                ORDER BY ms.session_date DESC, ms.start_time DESC
            """, (student_id, student_id))

            return render_template('makeup_sessions.html', makeups=makeups, sections=[])

        # Faculty / Admin view
        query = """
            SELECT ms.*, sec.section_name, c.course_code, c.course_title, f.full_name AS faculty_name,
                   (SELECT COUNT(*) FROM enrollments e WHERE e.section_id = sec.section_id AND e.status = 'enrolled') AS total_enrolled,
                   (SELECT COUNT(*) FROM makeup_attendance ma WHERE ma.makeup_id = ms.makeup_id AND ma.status = 'present') AS present_count
            FROM makeup_sessions ms
            JOIN sections sec ON ms.section_id = sec.section_id
            JOIN courses c ON sec.course_id = c.course_id
            JOIN faculty f ON ms.faculty_id = f.faculty_id
            WHERE 1=1
        """
        params = []
        if role == 'faculty':
            query += " AND ms.faculty_id = %s"
            params.append(faculty_id)

        query += " ORDER BY ms.session_date DESC, ms.start_time DESC"
        makeups = query_all(query, tuple(params))

        # Sections list for scheduling
        if role == 'faculty':
            sections = query_all("""
                SELECT sec.section_id, sec.section_name, c.course_code, c.course_title
                FROM sections sec
                JOIN courses c ON sec.course_id = c.course_id
                WHERE sec.faculty_id = %s AND sec.is_active = TRUE
                ORDER BY c.course_code
            """, (faculty_id,))
        else:
            sections = query_all("""
                SELECT sec.section_id, sec.section_name, c.course_code, c.course_title
                FROM sections sec
                JOIN courses c ON sec.course_id = c.course_id
                WHERE sec.is_active = TRUE
                ORDER BY c.course_code
            """)

        return render_template(
            'makeup_sessions.html',
            makeups=makeups,
            sections=sections,
            today=date.today().isoformat()
        )

    except Exception as e:
        flash(f"Error loading makeup sessions: {str(e)}", "danger")
        return render_template('makeup_sessions.html', makeups=[], sections=[])

@makeup_bp.route('/makeup/create', methods=['POST'])
@login_required
@role_required(['admin', 'faculty'])
def create():
    section_id = request.form.get('section_id', '').strip()
    session_date = request.form.get('session_date', '').strip()
    start_time = request.form.get('start_time', '').strip()
    end_time = request.form.get('end_time', '').strip()
    classroom = request.form.get('classroom', '').strip()
    topic = request.form.get('topic', '').strip()

    if not all([section_id, session_date, start_time, end_time, classroom, topic]):
        flash("All fields (Section, Date, Times, Classroom, Topic) are required.", "danger")
        return redirect(url_for('makeup.index'))

    role = session.get('role')
    faculty_id = session.get('faculty_id')

    try:
        section = query_one("SELECT faculty_id FROM sections WHERE section_id = %s", (int(section_id),))
        if not section:
            flash("Section not found.", "danger")
            return redirect(url_for('makeup.index'))

        assigned_faculty = faculty_id if role == 'faculty' else section['faculty_id']

        makeup_id, _ = execute(
            """
            INSERT INTO makeup_sessions (section_id, faculty_id, session_date, start_time, end_time, classroom, topic, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'scheduled')
            """,
            (int(section_id), assigned_faculty, session_date, start_time, end_time, classroom, topic)
        )

        log_audit(session['user_id'], 'CREATE_MAKEUP_SESSION', 'makeup_sessions', makeup_id, f"Scheduled makeup session on {session_date}", request.remote_addr)
        flash(f"Makeup session '{topic}' scheduled successfully.", "success")

    except Exception as e:
        flash(f"Error scheduling makeup session: {str(e)}", "danger")

    return redirect(url_for('makeup.index'))

@makeup_bp.route('/makeup/mark/<int:makeup_id>', methods=['GET', 'POST'])
@login_required
@role_required(['admin', 'faculty'])
def mark(makeup_id):
    try:
        makeup = query_one("""
            SELECT ms.*, sec.section_name, sec.section_id, c.course_code, c.course_title, f.full_name AS faculty_name
            FROM makeup_sessions ms
            JOIN sections sec ON ms.section_id = sec.section_id
            JOIN courses c ON sec.course_id = c.course_id
            JOIN faculty f ON ms.faculty_id = f.faculty_id
            WHERE ms.makeup_id = %s
        """, (makeup_id,))

        if not makeup:
            flash("Makeup session not found.", "danger")
            return redirect(url_for('makeup.index'))

        if request.method == 'POST':
            attended_students = request.form.getlist('attended_students')
            
            # Fetch all enrolled students in section
            all_enrolled = query_all("SELECT student_id FROM enrollments WHERE section_id = %s AND status = 'enrolled'", (makeup['section_id'],))
            
            operations = []
            for student in all_enrolled:
                sid = student['student_id']
                status = 'present' if str(sid) in attended_students else 'absent'
                query = """
                    INSERT INTO makeup_attendance (makeup_id, student_id, status, marked_by, marked_at)
                    VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                    ON DUPLICATE KEY UPDATE status = VALUES(status), marked_by = VALUES(marked_by), marked_at = CURRENT_TIMESTAMP
                """
                operations.append((query, (makeup_id, sid, status, session['user_id'])))

            # Also update makeup session status to completed
            operations.append(("UPDATE makeup_sessions SET status = 'completed' WHERE makeup_id = %s", (makeup_id,)))

            execute_transaction(operations)

            log_audit(session['user_id'], 'MARK_MAKEUP_ATTENDANCE', 'makeup_sessions', makeup_id, f"Recorded makeup attendance ({len(attended_students)} attended)", request.remote_addr)
            flash("Makeup attendance successfully saved.", "success")
            return redirect(url_for('makeup.index'))

        # GET: List students
        students = query_all("""
            SELECT s.student_id, s.roll_number, s.full_name, s.email, d.dept_code,
                   ma.status AS makeup_status
            FROM enrollments e
            JOIN students s ON e.student_id = s.student_id
            JOIN departments d ON s.dept_id = d.dept_id
            LEFT JOIN makeup_attendance ma ON ma.makeup_id = %s AND ma.student_id = s.student_id
            WHERE e.section_id = %s AND e.status = 'enrolled'
            ORDER BY s.roll_number ASC
        """, (makeup_id, makeup['section_id']))

        return render_template('mark_makeup.html', makeup=makeup, students=students)

    except Exception as e:
        flash(f"Error managing makeup attendance: {str(e)}", "danger")
        return redirect(url_for('makeup.index'))
