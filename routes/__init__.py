from .auth import auth_bp
from .dashboard import dashboard_bp
from .students import students_bp
from .faculty import faculty_bp
from .courses import courses_bp
from .attendance import attendance_bp
from .leaves import leaves_bp
from .makeup import makeup_bp
from .reports import reports_bp

__all__ = [
    'auth_bp',
    'dashboard_bp',
    'students_bp',
    'faculty_bp',
    'courses_bp',
    'attendance_bp',
    'leaves_bp',
    'makeup_bp',
    'reports_bp'
]
