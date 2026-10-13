import functools
from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, session, g
)
from werkzeug.security import check_password_hash, generate_password_hash
from database import query_one, query_all, execute, log_audit

auth_bp = Blueprint('auth', __name__)

def login_required(view):
    """Decorator to require login for a route."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('auth.login', next=request.url))
        return view(**kwargs)
    return wrapped_view

def role_required(allowed_roles):
    """Decorator to enforce role-based access control (RBAC)."""
    def decorator(view):
        @functools.wraps(view)
        def wrapped_view(**kwargs):
            if 'user_id' not in session:
                flash("Please log in to continue.", "warning")
                return redirect(url_for('auth.login'))
            if session.get('role') not in allowed_roles:
                flash("Access denied: You do not have permission for this resource.", "danger")
                return redirect(url_for('dashboard.index'))
            return view(**kwargs)
        return wrapped_view
    return decorator

@auth_bp.before_app_request
def load_logged_in_user():
    """Load user details before every request if logged in."""
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        try:
            user = query_one(
                "SELECT user_id, username, email, role, is_active FROM users WHERE user_id = %s",
                (user_id,)
            )
            g.user = user
        except Exception:
            g.user = None

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password', '')

        if not identifier or not password:
            flash("Please enter both username/email and password.", "danger")
            return render_template('login.html', identifier=identifier)

        try:
            # Check user by username OR email
            user = query_one(
                """
                SELECT user_id, username, email, password_hash, role, is_active
                FROM users
                WHERE (username = %s OR email = %s)
                """,
                (identifier, identifier)
            )

            if not user or not check_password_hash(user['password_hash'], password):
                flash("Invalid username/email or password.", "danger")
                return render_template('login.html', identifier=identifier)

            if not user['is_active']:
                flash("This account has been deactivated. Please contact the administrator.", "danger")
                return render_template('login.html', identifier=identifier)

            # Session data
            session.clear()
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['email'] = user['email']
            session['role'] = user['role']

            # Attach linked entity details based on role
            if user['role'] == 'student':
                student = query_one(
                    """
                    SELECT student_id, roll_number, full_name, dept_id, program, current_semester
                    FROM students WHERE user_id = %s
                    """,
                    (user['user_id'],)
                )
                if student:
                    session['student_id'] = student['student_id']
                    session['full_name'] = student['full_name']
                    session['roll_number'] = student['roll_number']
                    session['dept_id'] = student['dept_id']
                else:
                    session['full_name'] = user['username']

            elif user['role'] == 'faculty':
                faculty = query_one(
                    """
                    SELECT faculty_id, employee_id, full_name, dept_id, designation
                    FROM faculty WHERE user_id = %s
                    """,
                    (user['user_id'],)
                )
                if faculty:
                    session['faculty_id'] = faculty['faculty_id']
                    session['full_name'] = faculty['full_name']
                    session['employee_id'] = faculty['employee_id']
                    session['dept_id'] = faculty['dept_id']
                else:
                    session['full_name'] = user['username']
            else:
                session['full_name'] = "Administrator"

            log_audit(user['user_id'], 'USER_LOGIN', 'users', user['user_id'], 'User logged in successfully', request.remote_addr)
            flash(f"Welcome back, {session.get('full_name')}!", "success")

            next_url = request.args.get('next')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect(url_for('dashboard.index'))

        except Exception as e:
            flash(f"Database error during login: {str(e)}", "danger")
            return render_template('login.html', identifier=identifier)

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    user_id = session.get('user_id')
    if user_id:
        log_audit(user_id, 'USER_LOGOUT', 'users', user_id, 'User logged out', request.remote_addr)
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    user_id = session['user_id']
    role = session['role']
    profile_data = {}

    try:
        user = query_one("SELECT user_id, username, email, role, created_at FROM users WHERE user_id = %s", (user_id,))
        if role == 'student':
            profile_data = query_one(
                """
                SELECT s.*, d.dept_name, d.dept_code
                FROM students s
                JOIN departments d ON s.dept_id = d.dept_id
                WHERE s.user_id = %s
                """,
                (user_id,)
            )
        elif role == 'faculty':
            profile_data = query_one(
                """
                SELECT f.*, d.dept_name, d.dept_code
                FROM faculty f
                JOIN departments d ON f.dept_id = d.dept_id
                WHERE f.user_id = %s
                """,
                (user_id,)
            )

        recent_logs = query_all(
            "SELECT * FROM audit_logs WHERE user_id = %s ORDER BY created_at DESC LIMIT 10",
            (user_id,)
        )
        return render_template('profile.html', user=user, profile_data=profile_data, logs=recent_logs)
    except Exception as e:
        flash(f"Error fetching profile: {str(e)}", "danger")
        return redirect(url_for('dashboard.index'))

@auth_bp.route('/profile/change-password', methods=['POST'])
@login_required
def change_password():
    user_id = session['user_id']
    current_pwd = request.form.get('current_password', '')
    new_pwd = request.form.get('new_password', '')
    confirm_pwd = request.form.get('confirm_password', '')

    if not current_pwd or not new_pwd or not confirm_pwd:
        flash("All password fields are required.", "danger")
        return redirect(url_for('auth.profile'))

    if new_pwd != confirm_pwd:
        flash("New password and confirm password do not match.", "danger")
        return redirect(url_for('auth.profile'))

    if len(new_pwd) < 6:
        flash("New password must be at least 6 characters long.", "danger")
        return redirect(url_for('auth.profile'))

    try:
        user = query_one("SELECT password_hash FROM users WHERE user_id = %s", (user_id,))
        if not user or not check_password_hash(user['password_hash'], current_pwd):
            flash("Current password is incorrect.", "danger")
            return redirect(url_for('auth.profile'))

        new_hash = generate_password_hash(new_pwd)
        execute("UPDATE users SET password_hash = %s WHERE user_id = %s", (new_hash, user_id))
        log_audit(user_id, 'PASSWORD_CHANGE', 'users', user_id, 'Password changed successfully', request.remote_addr)
        flash("Password updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating password: {str(e)}", "danger")

    return redirect(url_for('auth.profile'))
