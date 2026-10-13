from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import date, datetime
from routes.auth import login_required, role_required
from database import query_all, query_one, execute, execute_transaction, log_audit
from config import Config

attendance_bp = Blueprint('attendance', __name__)

def update_attendance_alerts_for_section(section_id):
    """
    Evaluates attendance for all enrolled students in section_id and creates/updates
    or resolves alerts according to the configured threshold.
    """
    threshold = Config.ATTENDANCE_THRESHOLD
    try:
        setting = query_one("SELECT setting_value FROM system_settings WHERE setting_key = 'min_attendance_threshold'")
        if setting:
            threshold = float(setting['setting_value'])
    except Exception:
        pass

    # Fetch stats per student in this section
    stats = query_all("""
        SELECT 
            e.student_id,
            COUNT(a.attendance_id) AS total_counted,
            SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) AS attended_count,
            SUM(CASE WHEN a.status = 'absent' THEN 1 ELSE 0 END) AS missed_count,
            COALESCE(ROUND((SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) / NULLIF(COUNT(a.attendance_id), 0)) * 100, 2), 0.0) AS pct
        FROM enrollments e
        LEFT JOIN class_sessions cs ON cs.section_id = e.section_id
        LEFT JOIN attendance a ON a.session_id = cs.session_id AND a.student_id = e.student_id
        WHERE e.section_id = %s AND e.status = 'enrolled'
        GROUP BY e.student_id
    """, (section_id,))

    for s in stats:
        student_id = s['student_id']
        total = s['total_counted'] or 0
        attended = s['attended_count'] or 0
        missed = s['missed_count'] or 0
        pct = float(s['pct'] or 0.0)

        # Only evaluate alert after at least 2 sessions to avoid false early alarms
        if total >= 2 and pct < threshold:
            existing = query_one(
                "SELECT alert_id FROM attendance_alerts WHERE student_id = %s AND section_id = %s AND status = 'active'",
                (student_id, section_id)
            )
            if existing:
                execute(
                    """
                    UPDATE attendance_alerts
                    SET current_percentage = %s, classes_attended = %s, classes_missed = %s, updated_at = CURRENT_TIMESTAMP
                    WHERE alert_id = %s
                    """,
                    (pct, attended, missed, existing['alert_id'])
                )
            else:
                execute(
                    """
                    INSERT INTO attendance_alerts (student_id, section_id, current_percentage, threshold_percentage, classes_attended, classes_missed, status)
                    VALUES (%s, %s, %s, %s, %s, %s, 'active')
                    """,
                    (student_id, section_id, pct, threshold, attended, missed)
                )
        elif pct >= threshold:
            # Resolve any existing active alerts
            execute(
                "UPDATE attendance_alerts SET status = 'resolved', updated_at = CURRENT_TIMESTAMP WHERE student_id = %s AND section_id = %s AND status = 'active'",
                (student_id, section_id)
            )

@attendance_bp.route('/attendance')
@login_required
@role_required(['admin', 'faculty'])
def index():
    role = session.get('role')
    faculty_id = session.get('faculty_id')
    section_filter = request.args.get('section_id', '')

    query = """
        SELECT cs.*, sec.section_name, c.course_code, c.course_title, f.full_name AS faculty_name,
               (SELECT COUNT(*) FROM enrollments e WHERE e.section_id = sec.section_id AND e.status = 'enrolled') AS total_enrolled,
               COUNT(a.attendance_id) AS marked_students,
               SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) AS present_count,
               SUM(CASE WHEN a.status = 'absent' THEN 1 ELSE 0 END) AS absent_count,
               SUM(CASE WHEN a.status = 'leave' THEN 1 ELSE 0 END) AS leave_count
        FROM class_sessions cs
        JOIN sections sec ON cs.section_id = sec.section_id
        JOIN courses c ON sec.course_id = c.course_id
        JOIN faculty f ON cs.faculty_id = f.faculty_id
        LEFT JOIN attendance a ON cs.session_id = a.session_id
        WHERE 1=1
    """
    params = []

    if role == 'faculty':
        query += " AND (cs.faculty_id = %s OR sec.faculty_id = %s)"
        params.extend([faculty_id, faculty_id])

    if section_filter and section_filter.isdigit():
        query += " AND cs.section_id = %s"
        params.append(int(section_filter))

    query += " GROUP BY cs.session_id ORDER BY cs.session_date DESC, cs.start_time DESC"

    try:
        sessions = query_all(query, tuple(params))
        
        # Load sections available to the user for creating new sessions
        if role == 'faculty':
            available_sections = query_all("""
                SELECT sec.section_id, sec.section_name, c.course_code, c.course_title
                FROM sections sec
                JOIN courses c ON sec.course_id = c.course_id
                WHERE sec.faculty_id = %s AND sec.is_active = TRUE
                ORDER BY c.course_code, sec.section_name
            """, (faculty_id,))
        else:
            available_sections = query_all("""
                SELECT sec.section_id, sec.section_name, c.course_code, c.course_title, f.full_name AS faculty_name
                FROM sections sec
                JOIN courses c ON sec.course_id = c.course_id
                JOIN faculty f ON sec.faculty_id = f.faculty_id
                WHERE sec.is_active = TRUE
                ORDER BY c.course_code, sec.section_name
            """)

        return render_template(
            'attendance.html',
            sessions=sessions,
            available_sections=available_sections,
            selected_section=section_filter,
            today=date.today().isoformat()
        )
    except Exception as e:
        flash(f"Error loading attendance hub: {str(e)}", "danger")
        return render_template('attendance.html', sessions=[], available_sections=[])

@attendance_bp.route('/attendance/sessions/create', methods=['POST'])
@login_required
@role_required(['admin', 'faculty'])
def create_session():
    section_id = request.form.get('section_id', '').strip()
    session_date = request.form.get('session_date', '').strip()
    start_time = request.form.get('start_time', '').strip()
    end_time = request.form.get('end_time', '').strip()
    topic = request.form.get('topic', '').strip()
    session_type = request.form.get('session_type', 'regular').strip()

    if not all([section_id, session_date, start_time, end_time]):
        flash("Section, date, start time, and end time are required.", "danger")
        return redirect(url_for('attendance.index'))

    role = session.get('role')
    faculty_id = session.get('faculty_id')

    try:
        # Validate faculty authorization on section
        section = query_one("SELECT faculty_id FROM sections WHERE section_id = %s", (int(section_id),))
        if not section:
            flash("Selected section was not found.", "danger")
            return redirect(url_for('attendance.index'))

        if role == 'faculty' and section['faculty_id'] != faculty_id:
            flash("You can only create sessions for sections assigned to you.", "danger")
            return redirect(url_for('attendance.index'))

        assigned_faculty = section['faculty_id'] if role == 'admin' else faculty_id

        session_id, _ = execute(
            """
            INSERT INTO class_sessions (section_id, faculty_id, session_date, start_time, end_time, topic, session_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (int(section_id), assigned_faculty, session_date, start_time, end_time, topic or 'Lecture', session_type)
        )

        log_audit(session['user_id'], 'CREATE_CLASS_SESSION', 'class_sessions', session_id, f"Created session for section #{section_id} on {session_date}", request.remote_addr)
        flash("Class session created. Proceed to mark student attendance.", "success")
        return redirect(url_for('attendance.mark_attendance', session_id=session_id))

    except Exception as e:
        flash(f"Failed to create class session: {str(e)}", "danger")
        return redirect(url_for('attendance.index'))

@attendance_bp.route('/attendance/mark/<int:session_id>', methods=['GET', 'POST'])
@login_required
@role_required(['admin', 'faculty'])
def mark_attendance(session_id):
    role = session.get('role')
    faculty_id = session.get('faculty_id')

    try:
        session_info = query_one("""
            SELECT cs.*, sec.section_name, sec.classroom, sec.section_id,
                   c.course_code, c.course_title, f.full_name AS faculty_name, f.faculty_id AS assigned_faculty_id
            FROM class_sessions cs
            JOIN sections sec ON cs.section_id = sec.section_id
            JOIN courses c ON sec.course_id = c.course_id
            JOIN faculty f ON cs.faculty_id = f.faculty_id
            WHERE cs.session_id = %s
        """, (session_id,))

        if not session_info:
            flash("Class session record not found.", "danger")
            return redirect(url_for('attendance.index'))

        # Check permissions: faculty can only mark their own sessions
        if role == 'faculty' and session_info['assigned_faculty_id'] != faculty_id:
            flash("Unauthorized: You can only record attendance for your own sessions.", "danger")
            return redirect(url_for('attendance.index'))

        if request.method == 'POST':
            # Collect attendance data from form
            student_ids = request.form.getlist('student_ids')
            if not student_ids:
                flash("No enrolled students found to mark.", "warning")
                return redirect(url_for('attendance.index'))

            # Prepare atomic transaction operations
            operations = []
            for sid_str in student_ids:
                sid = int(sid_str)
                status = request.form.get(f'status_{sid}', 'present')
                remarks = request.form.get(f'remarks_{sid}', '').strip()

                if status not in ['present', 'absent', 'leave']:
                    status = 'present'

                # Use ON DUPLICATE KEY UPDATE to allow both new marking and corrections
                query = """
                    INSERT INTO attendance (session_id, student_id, status, remarks, marked_by, marked_at)
                    VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                    ON DUPLICATE KEY UPDATE
                        status = VALUES(status),
                        remarks = VALUES(remarks),
                        marked_by = VALUES(marked_by),
                        marked_at = CURRENT_TIMESTAMP
                """
                operations.append((query, (session_id, sid, status, remarks, session['user_id'])))

            execute_transaction(operations)

            # Update attendance shortage alerts dynamically
            update_attendance_alerts_for_section(session_info['section_id'])

            log_audit(session['user_id'], 'MARK_ATTENDANCE', 'class_sessions', session_id, f"Recorded attendance for {len(student_ids)} students", request.remote_addr)
            flash(f"Attendance for '{session_info['course_code']} ({session_info['section_name']})' saved successfully!", "success")
            return redirect(url_for('attendance.index', section_id=session_info['section_id']))

        # GET: Fetch all enrolled students and their attendance status for this session
        students = query_all("""
            SELECT s.student_id, s.roll_number, s.full_name, s.email, d.dept_code,
                   a.attendance_id, a.status AS attendance_status, a.remarks,
                   (SELECT COALESCE(ROUND((SUM(CASE WHEN att.status = 'present' THEN 1 ELSE 0 END) / NULLIF(COUNT(att.attendance_id), 0)) * 100, 1), 0.0)
                    FROM class_sessions all_cs
                    JOIN attendance att ON all_cs.session_id = att.session_id
                    WHERE all_cs.section_id = %s AND att.student_id = s.student_id) AS current_overall_pct
            FROM enrollments e
            JOIN students s ON e.student_id = s.student_id
            JOIN departments d ON s.dept_id = d.dept_id
            LEFT JOIN attendance a ON a.session_id = %s AND a.student_id = s.student_id
            WHERE e.section_id = %s AND e.status = 'enrolled'
            ORDER BY s.roll_number ASC
        """, (session_info['section_id'], session_id, session_info['section_id']))

        return render_template(
            'mark_attendance.html',
            session_info=session_info,
            students=students
        )

    except Exception as e:
        flash(f"Error loading attendance sheet: {str(e)}", "danger")
        return redirect(url_for('attendance.index'))

@attendance_bp.route('/my-attendance')
@login_required
@role_required(['student'])
def my_attendance():
    student_id = session.get('student_id')
    try:
        # Course-wise breakdown from the SQL VIEW
        course_summaries = query_all("""
            SELECT * FROM v_student_course_attendance
            WHERE student_id = %s
            ORDER BY course_code ASC
        """, (student_id,))

        # Attendance log entries
        history = query_all("""
            SELECT a.status, a.remarks, a.marked_at,
                   cs.session_date, cs.start_time, cs.end_time, cs.topic, cs.session_type,
                   c.course_code, c.course_title, sec.section_name, f.full_name AS faculty_name
            FROM attendance a
            JOIN class_sessions cs ON a.session_id = cs.session_id
            JOIN sections sec ON cs.section_id = sec.section_id
            JOIN courses c ON sec.course_id = c.course_id
            JOIN faculty f ON cs.faculty_id = f.faculty_id
            WHERE a.student_id = %s
            ORDER BY cs.session_date DESC, cs.start_time DESC
        """, (student_id,))

        # Active shortage alerts
        alerts = query_all("""
            SELECT al.*, sec.section_name, c.course_code, c.course_title
            FROM attendance_alerts al
            JOIN sections sec ON al.section_id = sec.section_id
            JOIN courses c ON sec.course_id = c.course_id
            WHERE al.student_id = %s AND al.status = 'active'
        """, (student_id,))

        # Makeup sessions attended
        makeups = query_all("""
            SELECT ma.status AS makeup_status, ms.session_date, ms.topic, ms.classroom,
                   c.course_code, c.course_title
            FROM makeup_attendance ma
            JOIN makeup_sessions ms ON ma.makeup_id = ms.makeup_id
            JOIN sections sec ON ms.section_id = sec.section_id
            JOIN courses c ON sec.course_id = c.course_id
            WHERE ma.student_id = %s
            ORDER BY ms.session_date DESC
        """, (student_id,))

        threshold = Config.ATTENDANCE_THRESHOLD

        return render_template(
            'student_attendance.html',
            courses=course_summaries,
            history=history,
            alerts=alerts,
            makeups=makeups,
            threshold=threshold
        )
    except Exception as e:
        flash(f"Error fetching attendance records: {str(e)}", "danger")
        return redirect(url_for('dashboard.index'))
