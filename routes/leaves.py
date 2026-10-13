import os
from datetime import datetime, date
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.utils import secure_filename
from routes.auth import login_required, role_required
from database import query_all, query_one, execute, execute_transaction, log_audit
from config import Config

leaves_bp = Blueprint('leaves', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@leaves_bp.route('/leaves')
@login_required
def index():
    role = session.get('role')
    user_id = session.get('user_id')
    status_filter = request.args.get('status', '')

    try:
        leave_types = query_all("SELECT * FROM leave_types WHERE is_active = TRUE ORDER BY type_name")

        if role == 'student':
            student_id = session.get('student_id')
            query = """
                SELECT la.*, lt.type_name,
                       lap.decision, lap.decision_notes, lap.reviewed_at,
                       u.username AS reviewer_name, f.full_name AS reviewer_full_name
                FROM leave_applications la
                JOIN leave_types lt ON la.leave_type_id = lt.leave_type_id
                LEFT JOIN leave_approvals lap ON la.application_id = lap.application_id
                LEFT JOIN users u ON lap.reviewed_by = u.user_id
                LEFT JOIN faculty f ON u.user_id = f.user_id
                WHERE la.student_id = %s
            """
            params = [student_id]
            if status_filter in ['pending', 'approved', 'rejected']:
                query += " AND la.status = %s"
                params.append(status_filter)
            query += " ORDER BY la.applied_at DESC"
            applications = query_all(query, tuple(params))

            return render_template(
                'leaves.html',
                applications=applications,
                leave_types=leave_types,
                status_filter=status_filter,
                today=date.today().isoformat()
            )

        elif role == 'faculty':
            faculty_id = session.get('faculty_id')
            # Fetch applications for students who take courses with this faculty
            query = """
                SELECT DISTINCT la.*, lt.type_name, s.roll_number, s.full_name AS student_name, s.email AS student_email,
                       d.dept_code,
                       lap.decision, lap.decision_notes, lap.reviewed_at,
                       u.username AS reviewer_name, f.full_name AS reviewer_full_name
                FROM leave_applications la
                JOIN students s ON la.student_id = s.student_id
                JOIN departments d ON s.dept_id = d.dept_id
                JOIN leave_types lt ON la.leave_type_id = lt.leave_type_id
                JOIN enrollments e ON s.student_id = e.student_id
                JOIN sections sec ON e.section_id = sec.section_id
                LEFT JOIN leave_approvals lap ON la.application_id = lap.application_id
                LEFT JOIN users u ON lap.reviewed_by = u.user_id
                LEFT JOIN faculty f ON u.user_id = f.user_id
                WHERE sec.faculty_id = %s
            """
            params = [faculty_id]
            if status_filter in ['pending', 'approved', 'rejected']:
                query += " AND la.status = %s"
                params.append(status_filter)
            query += " ORDER BY la.applied_at DESC"
            applications = query_all(query, tuple(params))

            return render_template(
                'leaves.html',
                applications=applications,
                leave_types=leave_types,
                status_filter=status_filter
            )

        else: # Admin
            query = """
                SELECT la.*, lt.type_name, s.roll_number, s.full_name AS student_name, s.email AS student_email,
                       d.dept_code,
                       lap.decision, lap.decision_notes, lap.reviewed_at,
                       u.username AS reviewer_name, f.full_name AS reviewer_full_name
                FROM leave_applications la
                JOIN students s ON la.student_id = s.student_id
                JOIN departments d ON s.dept_id = d.dept_id
                JOIN leave_types lt ON la.leave_type_id = lt.leave_type_id
                LEFT JOIN leave_approvals lap ON la.application_id = lap.application_id
                LEFT JOIN users u ON lap.reviewed_by = u.user_id
                LEFT JOIN faculty f ON u.user_id = f.user_id
                WHERE 1=1
            """
            params = []
            if status_filter in ['pending', 'approved', 'rejected']:
                query += " AND la.status = %s"
                params.append(status_filter)
            query += " ORDER BY la.applied_at DESC"
            applications = query_all(query, tuple(params))

            return render_template(
                'leaves.html',
                applications=applications,
                leave_types=leave_types,
                status_filter=status_filter
            )

    except Exception as e:
        flash(f"Error fetching leave applications: {str(e)}", "danger")
        return render_template('leaves.html', applications=[], leave_types=[])

@leaves_bp.route('/leaves/apply', methods=['POST'])
@login_required
@role_required(['student'])
def apply():
    student_id = session.get('student_id')
    leave_type_id = request.form.get('leave_type_id', '').strip()
    start_date_str = request.form.get('start_date', '').strip()
    end_date_str = request.form.get('end_date', '').strip()
    reason = request.form.get('reason', '').strip()

    if not all([leave_type_id, start_date_str, end_date_str, reason]):
        flash("All fields (Leave Type, Start Date, End Date, Reason) are required.", "danger")
        return redirect(url_for('leaves.index'))

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        if end_date < start_date:
            flash("Validation Error: End date cannot be earlier than start date.", "danger")
            return redirect(url_for('leaves.index'))

        total_days = (end_date - start_date).days + 1

        # Check optional document upload
        document_filename = None
        if 'document' in request.files:
            file = request.files['document']
            if file and file.filename != '':
                if allowed_file(file.filename):
                    filename = secure_filename(f"leave_{student_id}_{int(datetime.now().timestamp())}_{file.filename}")
                    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
                    file.save(os.path.join(Config.UPLOAD_FOLDER, filename))
                    document_filename = filename
                else:
                    flash("Invalid document format. Allowed: PNG, JPG, PDF, DOC, DOCX.", "warning")

        app_id, _ = execute(
            """
            INSERT INTO leave_applications (student_id, leave_type_id, start_date, end_date, total_days, reason, document_url, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'pending')
            """,
            (student_id, int(leave_type_id), start_date, end_date, total_days, reason, document_filename)
        )

        log_audit(session['user_id'], 'SUBMIT_LEAVE', 'leave_applications', app_id, f"Applied for {total_days} days leave ({start_date} to {end_date})", request.remote_addr)
        flash("Leave request submitted successfully. It will be reviewed by your course faculty.", "success")

    except ValueError:
        flash("Invalid date format provided.", "danger")
    except Exception as e:
        flash(f"Error submitting leave request: {str(e)}", "danger")

    return redirect(url_for('leaves.index'))

@leaves_bp.route('/leaves/review/<int:application_id>', methods=['POST'])
@login_required
@role_required(['admin', 'faculty'])
def review(application_id):
    decision = request.form.get('decision', '').strip().lower()
    notes = request.form.get('decision_notes', '').strip()

    if decision not in ['approved', 'rejected']:
        flash("Invalid decision specified.", "danger")
        return redirect(url_for('leaves.index'))

    try:
        app_record = query_one("""
            SELECT la.*, s.full_name AS student_name, s.roll_number
            FROM leave_applications la
            JOIN students s ON la.student_id = s.student_id
            WHERE la.application_id = %s
        """, (application_id,))

        if not app_record:
            flash("Leave application not found.", "danger")
            return redirect(url_for('leaves.index'))

        if app_record['status'] != 'pending':
            flash(f"Application has already been {app_record['status']}.", "warning")
            return redirect(url_for('leaves.index'))

        # Atomic transaction: Update application status + Insert into leave_approvals audit
        operations = [
            (
                "UPDATE leave_applications SET status = %s WHERE application_id = %s",
                (decision, application_id)
            ),
            (
                """
                INSERT INTO leave_approvals (application_id, reviewed_by, decision, decision_notes, reviewed_at)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                """,
                (application_id, session['user_id'], decision, notes)
            )
        ]
        execute_transaction(operations)

        log_audit(
            session['user_id'],
            'REVIEW_LEAVE',
            'leave_applications',
            application_id,
            f"Set leave #{application_id} ({app_record['student_name']}) status to {decision.upper()}",
            request.remote_addr
        )

        flash(f"Leave application for {app_record['student_name']} has been {decision.upper()}.", "success")

    except Exception as e:
        flash(f"Error reviewing leave request: {str(e)}", "danger")

    return redirect(url_for('leaves.index'))

@leaves_bp.route('/uploads/<filename>')
@login_required
def download_document(filename):
    return send_from_directory(Config.UPLOAD_FOLDER, filename)
