from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from routes.auth import login_required, role_required
from database import query_all, query_one, execute, log_audit

faculty_bp = Blueprint('faculty', __name__)

@faculty_bp.route('/faculty')
@login_required
@role_required(['admin'])
def list_faculty():
    search = request.args.get('search', '').strip()
    dept_id = request.args.get('dept_id', '')

    query = """
        SELECT f.*, d.dept_name, d.dept_code,
               (SELECT COUNT(*) FROM sections sec WHERE sec.faculty_id = f.faculty_id AND sec.is_active = TRUE) AS active_sections_count
        FROM faculty f
        JOIN departments d ON f.dept_id = d.dept_id
        WHERE 1=1
    """
    params = []

    if search:
        query += " AND (f.full_name LIKE %s OR f.employee_id LIKE %s OR f.email LIKE %s)"
        pattern = f"%{search}%"
        params.extend([pattern, pattern, pattern])

    if dept_id and dept_id.isdigit():
        query += " AND f.dept_id = %s"
        params.append(int(dept_id))

    query += " ORDER BY f.full_name ASC"

    try:
        faculty_members = query_all(query, tuple(params))
        departments = query_all("SELECT * FROM departments ORDER BY dept_name")
        return render_template(
            'faculty.html',
            faculty=faculty_members,
            departments=departments,
            search=search,
            dept_id=dept_id
        )
    except Exception as e:
        flash(f"Error fetching faculty records: {str(e)}", "danger")
        return render_template('faculty.html', faculty=[], departments=[])

@faculty_bp.route('/faculty/add', methods=['POST'])
@login_required
@role_required(['admin'])
def add_faculty():
    employee_id = request.form.get('employee_id', '').strip().upper()
    full_name = request.form.get('full_name', '').strip()
    email = request.form.get('email', '').strip().lower()
    dept_id = request.form.get('dept_id', '').strip()
    designation = request.form.get('designation', 'Assistant Professor').strip()
    phone = request.form.get('phone', '').strip()
    password = request.form.get('password', 'Password@123').strip()

    if not all([employee_id, full_name, email, dept_id]):
        flash("Please fill in required fields (Employee ID, Name, Email, Department).", "danger")
        return redirect(url_for('faculty.list_faculty'))

    try:
        # Check duplicate employee_id or email
        existing_f = query_one("SELECT faculty_id FROM faculty WHERE employee_id = %s OR email = %s", (employee_id, email))
        if existing_f:
            flash(f"Faculty with Employee ID '{employee_id}' or email '{email}' already exists.", "danger")
            return redirect(url_for('faculty.list_faculty'))

        pwd_hash = generate_password_hash(password)
        username = employee_id.lower().replace('-', '_')

        user_id, _ = execute(
            """
            INSERT INTO users (username, email, password_hash, role, is_active)
            VALUES (%s, %s, %s, 'faculty', TRUE)
            """,
            (username, email, pwd_hash)
        )

        faculty_id, _ = execute(
            """
            INSERT INTO faculty (user_id, employee_id, full_name, email, dept_id, designation, phone, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE)
            """,
            (user_id, employee_id, full_name, email, int(dept_id), designation, phone)
        )

        log_audit(session['user_id'], 'ADD_FACULTY', 'faculty', faculty_id, f"Added faculty {full_name} ({employee_id})", request.remote_addr)
        flash(f"Faculty '{full_name}' added successfully! Initial password is '{password}'.", "success")

    except Exception as e:
        flash(f"Failed to add faculty: {str(e)}", "danger")

    return redirect(url_for('faculty.list_faculty'))

@faculty_bp.route('/faculty/edit/<int:faculty_id>', methods=['POST'])
@login_required
@role_required(['admin'])
def edit_faculty(faculty_id):
    full_name = request.form.get('full_name', '').strip()
    email = request.form.get('email', '').strip().lower()
    dept_id = request.form.get('dept_id', '').strip()
    designation = request.form.get('designation', '').strip()
    phone = request.form.get('phone', '').strip()

    if not all([full_name, email, dept_id]):
        flash("Please fill in all required fields.", "danger")
        return redirect(url_for('faculty.list_faculty'))

    try:
        faculty_record = query_one("SELECT user_id FROM faculty WHERE faculty_id = %s", (faculty_id,))
        if not faculty_record:
            flash("Faculty record not found.", "danger")
            return redirect(url_for('faculty.list_faculty'))

        # Check duplicate email
        dup_check = query_one("SELECT faculty_id FROM faculty WHERE email = %s AND faculty_id != %s", (email, faculty_id))
        if dup_check:
            flash("That email address is already assigned to another faculty member.", "danger")
            return redirect(url_for('faculty.list_faculty'))

        execute(
            """
            UPDATE faculty
            SET full_name = %s, email = %s, dept_id = %s, designation = %s, phone = %s
            WHERE faculty_id = %s
            """,
            (full_name, email, int(dept_id), designation, phone, faculty_id)
        )
        execute("UPDATE users SET email = %s WHERE user_id = %s", (email, faculty_record['user_id']))

        log_audit(session['user_id'], 'EDIT_FACULTY', 'faculty', faculty_id, f"Updated faculty profile for #{faculty_id}", request.remote_addr)
        flash(f"Faculty '{full_name}' profile updated successfully.", "success")

    except Exception as e:
        flash(f"Failed to update faculty: {str(e)}", "danger")

    return redirect(url_for('faculty.list_faculty'))

@faculty_bp.route('/departments', methods=['GET', 'POST'])
@login_required
@role_required(['admin'])
def departments():
    if request.method == 'POST':
        dept_code = request.form.get('dept_code', '').strip().upper()
        dept_name = request.form.get('dept_name', '').strip()

        if not dept_code or not dept_name:
            flash("Both Department Code and Department Name are required.", "danger")
        else:
            try:
                existing = query_one("SELECT dept_id FROM departments WHERE dept_code = %s", (dept_code,))
                if existing:
                    flash(f"Department code '{dept_code}' already exists.", "danger")
                else:
                    dept_id, _ = execute(
                        "INSERT INTO departments (dept_code, dept_name) VALUES (%s, %s)",
                        (dept_code, dept_name)
                    )
                    log_audit(session['user_id'], 'ADD_DEPARTMENT', 'departments', dept_id, f"Added department {dept_code} - {dept_name}", request.remote_addr)
                    flash(f"Department '{dept_name}' ({dept_code}) created successfully.", "success")
            except Exception as e:
                flash(f"Error creating department: {str(e)}", "danger")

        return redirect(url_for('faculty.departments'))

    try:
        depts = query_all("""
            SELECT d.*,
                   COUNT(DISTINCT s.student_id) AS student_count,
                   COUNT(DISTINCT f.faculty_id) AS faculty_count,
                   COUNT(DISTINCT c.course_id) AS course_count
            FROM departments d
            LEFT JOIN students s ON d.dept_id = s.dept_id
            LEFT JOIN faculty f ON d.dept_id = f.dept_id
            LEFT JOIN courses c ON d.dept_id = c.dept_id
            GROUP BY d.dept_id
            ORDER BY d.dept_code ASC
        """)
        return render_template('departments.html', departments=depts)
    except Exception as e:
        flash(f"Error loading departments: {str(e)}", "danger")
        return render_template('departments.html', departments=[])
