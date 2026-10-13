from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from routes.auth import login_required, role_required
from database import query_all, query_one, execute, log_audit

courses_bp = Blueprint('courses', __name__)

# ============================================================================
# COURSES MANAGEMENT
# ============================================================================
@courses_bp.route('/courses')
@login_required
@role_required(['admin', 'faculty'])
def list_courses():
    dept_id = request.args.get('dept_id', '')
    query = """
        SELECT c.*, d.dept_name, d.dept_code,
               (SELECT COUNT(*) FROM sections sec WHERE sec.course_id = c.course_id AND sec.is_active = TRUE) AS active_sections_count
        FROM courses c
        JOIN departments d ON c.dept_id = d.dept_id
        WHERE 1=1
    """
    params = []
    if dept_id and dept_id.isdigit():
        query += " AND c.dept_id = %s"
        params.append(int(dept_id))

    query += " ORDER BY c.course_code ASC"

    try:
        course_list = query_all(query, tuple(params))
        departments = query_all("SELECT * FROM departments ORDER BY dept_name")
        return render_template('courses.html', courses=course_list, departments=departments, dept_id=dept_id)
    except Exception as e:
        flash(f"Error fetching courses: {str(e)}", "danger")
        return render_template('courses.html', courses=[], departments=[])

@courses_bp.route('/courses/add', methods=['POST'])
@login_required
@role_required(['admin'])
def add_course():
    course_code = request.form.get('course_code', '').strip().upper()
    course_title = request.form.get('course_title', '').strip()
    credits = request.form.get('credits', '3').strip()
    dept_id = request.form.get('dept_id', '').strip()

    if not all([course_code, course_title, dept_id]):
        flash("Course code, title, and department are required.", "danger")
        return redirect(url_for('courses.list_courses'))

    try:
        existing = query_one("SELECT course_id FROM courses WHERE course_code = %s", (course_code,))
        if existing:
            flash(f"Course code '{course_code}' already exists.", "danger")
            return redirect(url_for('courses.list_courses'))

        course_id, _ = execute(
            """
            INSERT INTO courses (course_code, course_title, credits, dept_id, is_active)
            VALUES (%s, %s, %s, %s, TRUE)
            """,
            (course_code, course_title, int(credits) if credits.isdigit() else 3, int(dept_id))
        )
        log_audit(session['user_id'], 'ADD_COURSE', 'courses', course_id, f"Added course {course_code} - {course_title}", request.remote_addr)
        flash(f"Course '{course_code}: {course_title}' created successfully.", "success")
    except Exception as e:
        flash(f"Error creating course: {str(e)}", "danger")

    return redirect(url_for('courses.list_courses'))

@courses_bp.route('/courses/edit/<int:course_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def edit_course(course_id):
    course_title = request.form.get('course_title', '').strip()
    credits = request.form.get('credits', '3').strip()
    dept_id = request.form.get('dept_id', '').strip()

    if not all([course_title, dept_id]):
        flash("Title and department are required.", "danger")
        return redirect(url_for('courses.list_courses'))

    try:
        execute(
            """
            UPDATE courses
            SET course_title = %s, credits = %s, dept_id = %s
            WHERE course_id = %s
            """,
            (course_title, int(credits) if credits.isdigit() else 3, int(dept_id), course_id)
        )
        log_audit(session['user_id'], 'EDIT_COURSE', 'courses', course_id, f"Updated course #{course_id}", request.remote_addr)
        flash("Course details updated successfully.", "success")
    except Exception as e:
        flash(f"Failed to update course: {str(e)}", "danger")

    return redirect(url_for('courses.list_courses'))


# ============================================================================
# SECTIONS MANAGEMENT
# ============================================================================
@courses_bp.route('/sections')
@login_required
@role_required(['admin', 'faculty'])
def list_sections():
    role = session.get('role')
    faculty_id = session.get('faculty_id')
    
    query = """
        SELECT sec.*, c.course_code, c.course_title, c.credits,
               f.full_name AS faculty_name, f.employee_id, d.dept_name,
               (SELECT COUNT(*) FROM enrollments e WHERE e.section_id = sec.section_id AND e.status = 'enrolled') AS enrolled_count,
               (SELECT COUNT(*) FROM class_sessions cs WHERE cs.section_id = sec.section_id) AS sessions_count
        FROM sections sec
        JOIN courses c ON sec.course_id = c.course_id
        JOIN faculty f ON sec.faculty_id = f.faculty_id
        JOIN departments d ON c.dept_id = d.dept_id
        WHERE 1=1
    """
    params = []

    # If faculty, option to see all or only their own
    if role == 'faculty':
        filter_my = request.args.get('my_only', '1')
        if filter_my == '1':
            query += " AND sec.faculty_id = %s"
            params.append(faculty_id)

    query += " ORDER BY c.course_code ASC, sec.section_name ASC"

    try:
        sections = query_all(query, tuple(params))
        courses = query_all("SELECT course_id, course_code, course_title FROM courses WHERE is_active = TRUE ORDER BY course_code")
        faculty_list = query_all("SELECT faculty_id, full_name, employee_id FROM faculty WHERE is_active = TRUE ORDER BY full_name")
        return render_template(
            'sections.html',
            sections=sections,
            courses=courses,
            faculty_list=faculty_list
        )
    except Exception as e:
        flash(f"Error fetching sections: {str(e)}", "danger")
        return render_template('sections.html', sections=[], courses=[], faculty_list=[])

@courses_bp.route('/sections/add', methods=['POST'])
@login_required
@role_required(['admin'])
def add_section():
    course_id = request.form.get('course_id', '').strip()
    faculty_id = request.form.get('faculty_id', '').strip()
    section_name = request.form.get('section_name', '').strip()
    academic_term = request.form.get('academic_term', 'Fall').strip()
    academic_year = request.form.get('academic_year', '2026-2027').strip()
    classroom = request.form.get('classroom', '').strip()
    max_capacity = request.form.get('max_capacity', '60').strip()

    if not all([course_id, faculty_id, section_name, classroom]):
        flash("Course, faculty, section name, and classroom are required.", "danger")
        return redirect(url_for('courses.list_sections'))

    try:
        # Check duplicate course + section + term + year
        existing = query_one(
            """
            SELECT section_id FROM sections
            WHERE course_id = %s AND section_name = %s AND academic_term = %s AND academic_year = %s
            """,
            (int(course_id), section_name, academic_term, academic_year)
        )
        if existing:
            flash(f"Section '{section_name}' for this course in {academic_term} {academic_year} already exists.", "danger")
            return redirect(url_for('courses.list_sections'))

        sec_id, _ = execute(
            """
            INSERT INTO sections (course_id, faculty_id, section_name, academic_term, academic_year, classroom, max_capacity, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE)
            """,
            (int(course_id), int(faculty_id), section_name, academic_term, academic_year, classroom, int(max_capacity) if max_capacity.isdigit() else 60)
        )
        log_audit(session['user_id'], 'ADD_SECTION', 'sections', sec_id, f"Created section {section_name}", request.remote_addr)
        flash(f"Section '{section_name}' created and assigned to faculty.", "success")
    except Exception as e:
        flash(f"Failed to create section: {str(e)}", "danger")

    return redirect(url_for('courses.list_sections'))

@courses_bp.route('/sections/edit/<int:section_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def edit_section(section_id):
    faculty_id = request.form.get('faculty_id', '').strip()
    classroom = request.form.get('classroom', '').strip()
    max_capacity = request.form.get('max_capacity', '60').strip()

    if not all([faculty_id, classroom]):
        flash("Faculty assignment and classroom are required.", "danger")
        return redirect(url_for('courses.list_sections'))

    try:
        execute(
            """
            UPDATE sections
            SET faculty_id = %s, classroom = %s, max_capacity = %s
            WHERE section_id = %s
            """,
            (int(faculty_id), classroom, int(max_capacity) if max_capacity.isdigit() else 60, section_id)
        )
        log_audit(session['user_id'], 'EDIT_SECTION', 'sections', section_id, f"Updated section #{section_id}", request.remote_addr)
        flash("Section allocation and classroom updated successfully.", "success")
    except Exception as e:
        flash(f"Failed to update section: {str(e)}", "danger")

    return redirect(url_for('courses.list_sections'))

@courses_bp.route('/sections/<int:section_id>/enrollments', methods=['GET', 'POST'])
@login_required
@role_required(['admin', 'faculty'])
def manage_enrollments(section_id):
    try:
        section = query_one("""
            SELECT sec.*, c.course_code, c.course_title, f.full_name AS faculty_name
            FROM sections sec
            JOIN courses c ON sec.course_id = c.course_id
            JOIN faculty f ON sec.faculty_id = f.faculty_id
            WHERE sec.section_id = %s
        """, (section_id,))

        if not section:
            flash("Section not found.", "danger")
            return redirect(url_for('courses.list_sections'))

        # Handle student enrollment submission (Admin only)
        if request.method == 'POST':
            if session.get('role') != 'admin':
                flash("Only administrators can modify student enrollments.", "danger")
                return redirect(url_for('courses.manage_enrollments', section_id=section_id))

            student_id = request.form.get('student_id')
            if not student_id:
                flash("Please select a student to enroll.", "danger")
            else:
                # Check section capacity
                enrolled_count = query_one(
                    "SELECT COUNT(*) AS val FROM enrollments WHERE section_id = %s AND status = 'enrolled'",
                    (section_id,)
                )['val']
                if enrolled_count >= section['max_capacity']:
                    flash(f"Cannot enroll student: Section has reached its maximum capacity ({section['max_capacity']}).", "danger")
                else:
                    # Check duplicate
                    existing = query_one(
                        "SELECT enrollment_id, status FROM enrollments WHERE section_id = %s AND student_id = %s",
                        (section_id, int(student_id))
                    )
                    if existing:
                        if existing['status'] == 'enrolled':
                            flash("Student is already enrolled in this section.", "warning")
                        else:
                            # Re-enroll
                            execute("UPDATE enrollments SET status = 'enrolled' WHERE enrollment_id = %s", (existing['enrollment_id'],))
                            flash("Student re-enrolled in this section.", "success")
                    else:
                        execute(
                            "INSERT INTO enrollments (student_id, section_id, status) VALUES (%s, %s, 'enrolled')",
                            (int(student_id), section_id)
                        )
                        log_audit(session['user_id'], 'ENROLL_STUDENT', 'enrollments', section_id, f"Enrolled student #{student_id} into section #{section_id}", request.remote_addr)
                        flash("Student enrolled successfully.", "success")

            return redirect(url_for('courses.manage_enrollments', section_id=section_id))

        # View enrollments
        enrolled_students = query_all("""
            SELECT e.enrollment_id, e.enrolled_at, e.status,
                   s.student_id, s.roll_number, s.full_name, s.email, d.dept_code,
                   (SELECT COALESCE(ROUND((SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) / NULLIF(COUNT(a.attendance_id), 0)) * 100, 1), 0.0)
                    FROM class_sessions cs
                    JOIN attendance a ON cs.session_id = a.session_id
                    WHERE cs.section_id = %s AND a.student_id = s.student_id) AS current_att_pct
            FROM enrollments e
            JOIN students s ON e.student_id = s.student_id
            JOIN departments d ON s.dept_id = d.dept_id
            WHERE e.section_id = %s AND e.status = 'enrolled'
            ORDER BY s.roll_number ASC
        """, (section_id, section_id))

        # Available students for enrollment (not yet enrolled in this section)
        available_students = query_all("""
            SELECT s.student_id, s.roll_number, s.full_name, d.dept_code
            FROM students s
            JOIN departments d ON s.dept_id = d.dept_id
            WHERE s.is_active = TRUE AND s.student_id NOT IN (
                SELECT student_id FROM enrollments WHERE section_id = %s AND status = 'enrolled'
            )
            ORDER BY s.roll_number ASC
        """, (section_id,))

        return render_template(
            'section_enrollments.html',
            section=section,
            enrolled_students=enrolled_students,
            available_students=available_students
        )
    except Exception as e:
        flash(f"Error managing enrollments: {str(e)}", "danger")
        return redirect(url_for('courses.list_sections'))

@courses_bp.route('/sections/<int:section_id>/unenroll/<int:student_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def unenroll_student(section_id, student_id):
    try:
        execute(
            "UPDATE enrollments SET status = 'dropped' WHERE section_id = %s AND student_id = %s",
            (section_id, student_id)
        )
        log_audit(session['user_id'], 'DROP_ENROLLMENT', 'enrollments', section_id, f"Dropped student #{student_id} from section #{section_id}", request.remote_addr)
        flash("Student removed from section enrollment.", "info")
    except Exception as e:
        flash(f"Error unenrolling student: {str(e)}", "danger")

    return redirect(url_for('courses.manage_enrollments', section_id=section_id))
