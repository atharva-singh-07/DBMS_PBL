from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from routes.auth import login_required, role_required
from database import query_all, query_one, execute, execute_transaction, log_audit

students_bp = Blueprint('students', __name__)

@students_bp.route('/students')
@login_required
@role_required(['admin', 'faculty'])
def list_students():
    search = request.args.get('search', '').strip()
    dept_id = request.args.get('dept_id', '')
    status = request.args.get('status', '')

    query = """
        SELECT s.*, d.dept_name, d.dept_code, u.is_active AS user_active
        FROM students s
        JOIN departments d ON s.dept_id = d.dept_id
        JOIN users u ON s.user_id = u.user_id
        WHERE 1=1
    """
    params = []

    if search:
        query += " AND (s.full_name LIKE %s OR s.roll_number LIKE %s OR s.email LIKE %s)"
        pattern = f"%{search}%"
        params.extend([pattern, pattern, pattern])

    if dept_id and dept_id.isdigit():
        query += " AND s.dept_id = %s"
        params.append(int(dept_id))

    if status in ['active', 'inactive']:
        query += " AND s.is_active = %s"
        params.append(1 if status == 'active' else 0)

    query += " ORDER BY s.roll_number ASC"

    try:
        students = query_all(query, tuple(params))
        departments = query_all("SELECT * FROM departments ORDER BY dept_name")
        return render_template(
            'students.html',
            students=students,
            departments=departments,
            search=search,
            dept_id=dept_id,
            status=status
        )
    except Exception as e:
        flash(f"Error fetching students: {str(e)}", "danger")
        return render_template('students.html', students=[], departments=[])

@students_bp.route('/students/add', methods=['POST'])
@login_required
@role_required(['admin'])
def add_student():
    roll_number = request.form.get('roll_number', '').strip().upper()
    full_name = request.form.get('full_name', '').strip()
    email = request.form.get('email', '').strip().lower()
    dept_id = request.form.get('dept_id', '').strip()
    program = request.form.get('program', '').strip()
    semester = request.form.get('semester', '1').strip()
    phone = request.form.get('phone', '').strip()
    password = request.form.get('password', 'Password@123').strip()

    if not all([roll_number, full_name, email, dept_id, program]):
        flash("Please fill in all required fields (Roll Number, Name, Email, Department, Program).", "danger")
        return redirect(url_for('students.list_students'))

    try:
        # Check duplicate roll number or email
        existing_student = query_one(
            "SELECT student_id FROM students WHERE roll_number = %s OR email = %s",
            (roll_number, email)
        )
        if existing_student:
            flash(f"A student with roll number '{roll_number}' or email '{email}' already exists.", "danger")
            return redirect(url_for('students.list_students'))

        existing_user = query_one("SELECT user_id FROM users WHERE email = %s OR username = %s", (email, roll_number))
        if existing_user:
            flash(f"A user with email '{email}' or username '{roll_number}' already exists.", "danger")
            return redirect(url_for('students.list_students'))

        # Create user account and student profile in atomic transaction
        pwd_hash = generate_password_hash(password)
        username = roll_number.lower().replace('-', '_')

        user_id, _ = execute(
            """
            INSERT INTO users (username, email, password_hash, role, is_active)
            VALUES (%s, %s, %s, 'student', TRUE)
            """,
            (username, email, pwd_hash)
        )

        student_id, _ = execute(
            """
            INSERT INTO students (user_id, roll_number, full_name, email, dept_id, program, current_semester, phone, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, TRUE)
            """,
            (user_id, roll_number, full_name, email, int(dept_id), program, int(semester) if semester.isdigit() else 1, phone)
        )

        log_audit(session['user_id'], 'ADD_STUDENT', 'students', student_id, f"Added student {full_name} ({roll_number})", request.remote_addr)
        flash(f"Student '{full_name}' added successfully! Default password is '{password}'.", "success")

    except Exception as e:
        flash(f"Failed to add student: {str(e)}", "danger")

    return redirect(url_for('students.list_students'))

@students_bp.route('/students/edit/<int:student_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def edit_student(student_id):
    full_name = request.form.get('full_name', '').strip()
    email = request.form.get('email', '').strip().lower()
    dept_id = request.form.get('dept_id', '').strip()
    program = request.form.get('program', '').strip()
    semester = request.form.get('semester', '1').strip()
    phone = request.form.get('phone', '').strip()

    if not all([full_name, email, dept_id, program]):
        flash("Please fill in all required fields.", "danger")
        return redirect(url_for('students.list_students'))

    try:
        student = query_one("SELECT user_id FROM students WHERE student_id = %s", (student_id,))
        if not student:
            flash("Student not found.", "danger")
            return redirect(url_for('students.list_students'))

        # Check duplicate email on another user
        dup_check = query_one("SELECT student_id FROM students WHERE email = %s AND student_id != %s", (email, student_id))
        if dup_check:
            flash("That email address is already assigned to another student.", "danger")
            return redirect(url_for('students.list_students'))

        # Update student and user
        execute(
            """
            UPDATE students
            SET full_name = %s, email = %s, dept_id = %s, program = %s, current_semester = %s, phone = %s
            WHERE student_id = %s
            """,
            (full_name, email, int(dept_id), program, int(semester) if semester.isdigit() else 1, phone, student_id)
        )
        execute("UPDATE users SET email = %s WHERE user_id = %s", (email, student['user_id']))

        log_audit(session['user_id'], 'EDIT_STUDENT', 'students', student_id, f"Updated profile for student #{student_id}", request.remote_addr)
        flash(f"Student '{full_name}' profile updated successfully.", "success")

    except Exception as e:
        flash(f"Failed to update student: {str(e)}", "danger")

    return redirect(url_for('students.list_students'))

@students_bp.route('/students/toggle-status/<int:student_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def toggle_status(student_id):
    try:
        student = query_one("SELECT student_id, user_id, full_name, is_active FROM students WHERE student_id = %s", (student_id,))
        if not student:
            flash("Student record not found.", "danger")
            return redirect(url_for('students.list_students'))

        new_status = not student['is_active']
        execute("UPDATE students SET is_active = %s WHERE student_id = %s", (new_status, student_id))
        execute("UPDATE users SET is_active = %s WHERE user_id = %s", (new_status, student['user_id']))

        status_str = "activated" if new_status else "deactivated"
        log_audit(session['user_id'], 'TOGGLE_STUDENT_STATUS', 'students', student_id, f"Student {student['full_name']} {status_str}", request.remote_addr)
        flash(f"Student '{student['full_name']}' has been {status_str}.", "info")

    except Exception as e:
        flash(f"Error toggling student status: {str(e)}", "danger")

    return redirect(url_for('students.list_students'))
