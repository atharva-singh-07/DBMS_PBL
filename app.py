import os
from datetime import datetime, date
from flask import Flask, render_template, session, g
from config import Config
from database import init_db_pool, query_one
from routes import (
    auth_bp,
    dashboard_bp,
    students_bp,
    faculty_bp,
    courses_bp,
    attendance_bp,
    leaves_bp,
    makeup_bp,
    reports_bp
)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize MySQL Connection Pool
    with app.app_context():
        init_db_pool()

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(faculty_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(leaves_bp)
    app.register_blueprint(makeup_bp)
    app.register_blueprint(reports_bp)

    # Global Jinja Context Processor
    @app.context_processor
    def inject_global_data():
        role = session.get('role')
        user_id = session.get('user_id')
        pending_leaves_badge = 0
        active_alerts_badge = 0

        if user_id:
            try:
                if role == 'admin':
                    pending_leaves_row = query_one("SELECT COUNT(*) AS val FROM leave_applications WHERE status = 'pending'")
                    pending_leaves_badge = pending_leaves_row['val'] if pending_leaves_row else 0
                    alerts_row = query_one("SELECT COUNT(*) AS val FROM attendance_alerts WHERE status = 'active'")
                    active_alerts_badge = alerts_row['val'] if alerts_row else 0
                elif role == 'faculty':
                    fac_id = session.get('faculty_id')
                    pending_row = query_one("""
                        SELECT COUNT(DISTINCT la.application_id) AS val
                        FROM leave_applications la
                        JOIN enrollments e ON la.student_id = e.student_id
                        JOIN sections sec ON e.section_id = sec.section_id
                        WHERE sec.faculty_id = %s AND la.status = 'pending'
                    """, (fac_id,))
                    pending_leaves_badge = pending_row['val'] if pending_row else 0
                elif role == 'student':
                    stu_id = session.get('student_id')
                    alerts_row = query_one("SELECT COUNT(*) AS val FROM attendance_alerts WHERE student_id = %s AND status = 'active'", (stu_id,))
                    active_alerts_badge = alerts_row['val'] if alerts_row else 0
            except Exception:
                pass

        return {
            'app_name': 'AttendEase',
            'app_tagline': 'Smart Attendance. Simple Leave Management.',
            'current_year': datetime.now().year,
            'default_threshold': Config.ATTENDANCE_THRESHOLD,
            'pending_leaves_badge': pending_leaves_badge,
            'active_alerts_badge': active_alerts_badge
        }

    # Jinja Template Filters
    @app.template_filter('format_date')
    def format_date(value):
        if not value:
            return '—'
        if isinstance(value, (datetime, date)):
            return value.strftime('%b %d, %Y')
        try:
            d = datetime.strptime(str(value)[:10], '%Y-%m-%d')
            return d.strftime('%b %d, %Y')
        except Exception:
            return str(value)

    @app.template_filter('format_time')
    def format_time(value):
        if not value:
            return '—'
        try:
            return str(value)[:5]
        except Exception:
            return str(value)

    @app.template_filter('badge_status')
    def badge_status(val):
        status = str(val).lower()
        if status in ['present', 'approved', 'active', 'enrolled', 'completed']:
            return 'badge-success'
        elif status in ['absent', 'rejected', 'dropped', 'inactive', 'cancelled']:
            return 'badge-danger'
        elif status in ['leave', 'pending', 'scheduled', 'warning']:
            return 'badge-warning'
        return 'badge-secondary'

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html', error_code=404, message="The requested page could not be found."), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error.html', error_code=500, message="An internal server or database error occurred."), 500

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', '1') == '1'
    print(f"\n* Starting AttendEase on http://127.0.0.1:{port}")
    print("* Application: AttendEase — Student Attendance and Leave Approval System")
    app.run(host='0.0.0.0', port=port, debug=debug)
