import json
from flask import Blueprint, render_template, session, redirect, url_for, flash
from routes.auth import login_required
from database import query_one, query_all

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('auth.login'))

@dashboard_bp.route('/dashboard')
@login_required
def index():
    role = session.get('role')
    user_id = session.get('user_id')
    stats = {}
    chart_data = {}
    recent_activity = []
    shortcuts = []

    try:
        # ====================================================================
        # 1. ADMIN DASHBOARD
        # ====================================================================
        if role == 'admin':
            # Metric cards
            total_students = query_one("SELECT COUNT(*) AS val FROM students WHERE is_active = TRUE")['val']
            total_faculty = query_one("SELECT COUNT(*) AS val FROM faculty WHERE is_active = TRUE")['val']
            total_courses = query_one("SELECT COUNT(*) AS val FROM courses WHERE is_active = TRUE")['val']
            total_sections = query_one("SELECT COUNT(*) AS val FROM sections WHERE is_active = TRUE")['val']
            today_sessions = query_one("SELECT COUNT(*) AS val FROM class_sessions WHERE session_date = CURDATE()")['val']
            
            avg_att_row = query_one("""
                SELECT COALESCE(
                    ROUND((SUM(CASE WHEN status = 'present' THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0)) * 100, 1), 
                    0.0
                ) AS val 
                FROM attendance
            """)
            overall_avg_attendance = avg_att_row['val'] if avg_att_row else 0.0

            shortage_count = query_one("SELECT COUNT(DISTINCT student_id) AS val FROM attendance_alerts WHERE status = 'active'")['val']
            pending_leaves = query_one("SELECT COUNT(*) AS val FROM leave_applications WHERE status = 'pending'")['val']
            approved_leaves = query_one("SELECT COUNT(*) AS val FROM leave_applications WHERE status = 'approved'")['val']
            rejected_leaves = query_one("SELECT COUNT(*) AS val FROM leave_applications WHERE status = 'rejected'")['val']

            stats = {
                'total_students': total_students,
                'total_faculty': total_faculty,
                'total_courses': total_courses,
                'total_sections': total_sections,
                'today_sessions': today_sessions,
                'overall_avg_attendance': overall_avg_attendance,
                'shortage_count': shortage_count,
                'pending_leaves': pending_leaves,
                'approved_leaves': approved_leaves,
                'rejected_leaves': rejected_leaves
            }

            # Monthly attendance trend for Chart.js
            monthly_trends = query_all("""
                SELECT 
                    DATE_FORMAT(cs.session_date, '%b %Y') AS month_label,
                    COUNT(a.attendance_id) AS total_counted,
                    SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) AS present_count,
                    ROUND((SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) / NULLIF(COUNT(a.attendance_id), 0)) * 100, 1) AS att_pct
                FROM class_sessions cs
                JOIN attendance a ON cs.session_id = a.session_id
                GROUP BY DATE_FORMAT(cs.session_date, '%Y-%m'), month_label
                ORDER BY MIN(cs.session_date) ASC
                LIMIT 6
            """)

            # Department wise stats
            dept_stats = query_all("""
                SELECT 
                    d.dept_code,
                    COUNT(DISTINCT s.student_id) AS student_count,
                    COUNT(DISTINCT f.faculty_id) AS faculty_count
                FROM departments d
                LEFT JOIN students s ON d.dept_id = s.dept_id AND s.is_active = TRUE
                LEFT JOIN faculty f ON d.dept_id = f.dept_id AND f.is_active = TRUE
                GROUP BY d.dept_id, d.dept_code
            """)

            chart_data = {
                'trend_labels': [row['month_label'] for row in monthly_trends],
                'trend_values': [float(row['att_pct']) for row in monthly_trends],
                'dept_labels': [row['dept_code'] for row in dept_stats],
                'dept_students': [row['student_count'] for row in dept_stats],
                'dept_faculty': [row['faculty_count'] for row in dept_stats]
            }

            # Recent audit activity
            recent_activity = query_all("""
                SELECT a.*, u.username, u.role
                FROM audit_logs a
                LEFT JOIN users u ON a.user_id = u.user_id
                ORDER BY a.created_at DESC
                LIMIT 6
            """)

            shortcuts = [
                {'title': 'Manage Students', 'url': url_for('students.list_students'), 'icon': 'bi-people'},
                {'title': 'Course Allocations', 'url': url_for('courses.list_sections'), 'icon': 'bi-grid'},
                {'title': 'Attendance Reports', 'url': url_for('reports.index'), 'icon': 'bi-graph-up'},
                {'title': 'Shortage Alerts', 'url': url_for('reports.index', report='shortage'), 'icon': 'bi-exclamation-triangle'}
            ]

        # ====================================================================
        # 2. FACULTY DASHBOARD
        # ====================================================================
        elif role == 'faculty':
            faculty_id = session.get('faculty_id')
            
            # Faculty assigned sections
            my_sections = query_all("""
                SELECT sec.*, c.course_code, c.course_title,
                       (SELECT COUNT(*) FROM enrollments e WHERE e.section_id = sec.section_id AND e.status = 'enrolled') AS enrolled_students
                FROM sections sec
                JOIN courses c ON sec.course_id = c.course_id
                WHERE sec.faculty_id = %s AND sec.is_active = TRUE
            """, (faculty_id,))

            section_ids = [s['section_id'] for s in my_sections]
            total_students_enrolled = sum(s['enrolled_students'] for s in my_sections)

            # Today's sessions
            today_sessions_count = query_one("""
                SELECT COUNT(*) AS val
                FROM class_sessions
                WHERE faculty_id = %s AND session_date = CURDATE()
            """, (faculty_id,))['val']

            # Pending leave requests from students in this faculty's sections
            pending_leaves_count = 0
            if section_ids:
                format_strings = ','.join(['%s'] * len(section_ids))
                pending_leaves_query = f"""
                    SELECT COUNT(DISTINCT la.application_id) AS val
                    FROM leave_applications la
                    JOIN enrollments e ON la.student_id = e.student_id
                    WHERE e.section_id IN ({format_strings}) AND la.status = 'pending'
                """
                pending_leaves_count = query_one(pending_leaves_query, tuple(section_ids))['val']

            # Average attendance in faculty's sessions
            faculty_avg_att = query_one("""
                SELECT COALESCE(
                    ROUND((SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) / NULLIF(COUNT(a.attendance_id), 0)) * 100, 1),
                    0.0
                ) AS val
                FROM class_sessions cs
                JOIN attendance a ON cs.session_id = a.session_id
                WHERE cs.faculty_id = %s
            """, (faculty_id,))['val']

            # Active shortages in this faculty's sections
            faculty_shortages = 0
            if section_ids:
                format_strings = ','.join(['%s'] * len(section_ids))
                shortage_q = f"SELECT COUNT(*) AS val FROM attendance_alerts WHERE section_id IN ({format_strings}) AND status = 'active'"
                faculty_shortages = query_one(shortage_q, tuple(section_ids))['val']

            stats = {
                'assigned_sections': len(my_sections),
                'enrolled_students': total_students_enrolled,
                'today_sessions': today_sessions_count,
                'pending_leaves': pending_leaves_count,
                'avg_attendance': faculty_avg_att,
                'active_shortages': faculty_shortages
            }

            # Recent sessions conducted
            recent_activity = query_all("""
                SELECT cs.*, sec.section_name, c.course_code,
                       COUNT(a.attendance_id) AS marked_count,
                       SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) AS present_count
                FROM class_sessions cs
                JOIN sections sec ON cs.section_id = sec.section_id
                JOIN courses c ON sec.course_id = c.course_id
                LEFT JOIN attendance a ON cs.session_id = a.session_id
                WHERE cs.faculty_id = %s
                GROUP BY cs.session_id
                ORDER BY cs.session_date DESC, cs.start_time DESC
                LIMIT 5
            """, (faculty_id,))

            # Section-wise attendance comparison chart
            sec_performance = []
            if section_ids:
                format_strings = ','.join(['%s'] * len(section_ids))
                sec_perf_query = f"""
                    SELECT sec.section_name, c.course_code,
                           ROUND((SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) / NULLIF(COUNT(a.attendance_id), 0)) * 100, 1) AS att_pct
                    FROM sections sec
                    JOIN courses c ON sec.course_id = c.course_id
                    JOIN class_sessions cs ON sec.section_id = cs.section_id
                    JOIN attendance a ON cs.session_id = a.session_id
                    WHERE sec.section_id IN ({format_strings})
                    GROUP BY sec.section_id, sec.section_name, c.course_code
                """
                sec_performance = query_all(sec_perf_query, tuple(section_ids))

            chart_data = {
                'section_labels': [f"{row['course_code']} ({row['section_name']})" for row in sec_performance],
                'section_values': [float(row['att_pct']) if row['att_pct'] else 0.0 for row in sec_performance]
            }

            shortcuts = [
                {'title': 'Mark Attendance', 'url': url_for('attendance.index'), 'icon': 'bi-check2-square'},
                {'title': 'Review Leaves', 'url': url_for('leaves.index'), 'icon': 'bi-calendar-check'},
                {'title': 'Schedule Makeup', 'url': url_for('makeup.index'), 'icon': 'bi-clock-history'},
                {'title': 'Shortage Alerts', 'url': url_for('reports.index', report='shortage'), 'icon': 'bi-shield-exclamation'}
            ]

        # ====================================================================
        # 3. STUDENT DASHBOARD
        # ====================================================================
        elif role == 'student':
            student_id = session.get('student_id')
            
            # Course attendance summary from view
            student_courses = query_all("""
                SELECT * FROM v_student_course_attendance
                WHERE student_id = %s
            """, (student_id,))

            total_present = sum(sc['present_count'] or 0 for sc in student_courses)
            total_absent = sum(sc['absent_count'] or 0 for sc in student_courses)
            total_leave = sum(sc['leave_count'] or 0 for sc in student_courses)
            total_counted = sum(sc['total_counted_classes'] or 0 for sc in student_courses)

            overall_pct = round((total_present / total_counted * 100), 1) if total_counted > 0 else 0.0

            # Active shortage alerts
            active_alerts = query_all("""
                SELECT a.*, sec.section_name, c.course_code, c.course_title
                FROM attendance_alerts a
                JOIN sections sec ON a.section_id = sec.section_id
                JOIN courses c ON sec.course_id = c.course_id
                WHERE a.student_id = %s AND a.status = 'active'
            """, (student_id,))

            # Student leave applications summary
            pending_leaves = query_one("""
                SELECT COUNT(*) AS val FROM leave_applications
                WHERE student_id = %s AND status = 'pending'
            """, (student_id,))['val']

            # Upcoming makeup sessions for enrolled courses
            upcoming_makeups = query_all("""
                SELECT m.*, sec.section_name, c.course_code, c.course_title, f.full_name AS faculty_name
                FROM makeup_sessions m
                JOIN sections sec ON m.section_id = sec.section_id
                JOIN courses c ON sec.course_id = c.course_id
                JOIN faculty f ON m.faculty_id = f.faculty_id
                JOIN enrollments e ON e.section_id = sec.section_id
                WHERE e.student_id = %s AND m.session_date >= CURDATE() AND m.status = 'scheduled'
                ORDER BY m.session_date ASC, m.start_time ASC
                LIMIT 3
            """, (student_id,))

            stats = {
                'overall_percentage': overall_pct,
                'total_present': total_present,
                'total_absent': total_absent,
                'total_leave': total_leave,
                'total_counted': total_counted,
                'courses_count': len(student_courses),
                'shortage_alerts_count': len(active_alerts),
                'pending_leaves_count': pending_leaves
            }

            chart_data = {
                'course_labels': [row['course_code'] for row in student_courses],
                'course_values': [float(row['attendance_percentage'] or 0.0) for row in student_courses],
                'course_titles': [row['course_title'] for row in student_courses]
            }

            recent_activity = query_all("""
                SELECT a.marked_at, a.status, a.remarks, cs.session_date, cs.topic, c.course_code
                FROM attendance a
                JOIN class_sessions cs ON a.session_id = cs.session_id
                JOIN sections sec ON cs.section_id = sec.section_id
                JOIN courses c ON sec.course_id = c.course_id
                WHERE a.student_id = %s
                ORDER BY cs.session_date DESC, a.marked_at DESC
                LIMIT 5
            """, (student_id,))

            shortcuts = [
                {'title': 'View Attendance History', 'url': url_for('attendance.my_attendance'), 'icon': 'bi-bar-chart-line'},
                {'title': 'Apply for Leave', 'url': url_for('leaves.index'), 'icon': 'bi-file-earmark-plus'},
                {'title': 'Upcoming Makeups', 'url': url_for('makeup.index'), 'icon': 'bi-calendar-event'},
                {'title': 'Attendance Shortages', 'url': url_for('attendance.my_attendance'), 'icon': 'bi-exclamation-triangle'}
            ]

        return render_template(
            'dashboard.html',
            stats=stats,
            chart_data=json.dumps(chart_data),
            recent_activity=recent_activity,
            shortcuts=shortcuts,
            student_courses=student_courses if role == 'student' else [],
            active_alerts=active_alerts if role == 'student' else [],
            upcoming_makeups=upcoming_makeups if role == 'student' else []
        )

    except Exception as e:
        flash(f"Error loading dashboard: {str(e)}", "danger")
        return render_template('dashboard.html', stats={}, chart_data="{}", recent_activity=[], shortcuts=[])
