import csv
import io
from flask import Blueprint, render_template, request, Response, flash, session
from routes.auth import login_required, role_required
from database import query_all, query_one
from config import Config

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/reports')
@login_required
@role_required(['admin', 'faculty'])
def index():
    report_type = request.args.get('report', 'student_wise')
    dept_id = request.args.get('dept_id', '')
    course_id = request.args.get('course_id', '')
    threshold = float(request.args.get('threshold', Config.ATTENDANCE_THRESHOLD))

    data = []
    columns = []
    report_title = ""
    report_description = ""

    try:
        departments = query_all("SELECT * FROM departments ORDER BY dept_name")
        courses = query_all("SELECT * FROM courses WHERE is_active = TRUE ORDER BY course_code")

        # --------------------------------------------------------------------
        # Report 1: Student-wise Attendance Percentage
        # Uses View: v_student_course_attendance
        # --------------------------------------------------------------------
        if report_type == 'student_wise':
            report_title = "Student-wise Attendance Percentage Report"
            report_description = "Detailed breakdown of student attendance by course and section, utilizing the v_student_course_attendance SQL VIEW."
            
            query = """
                SELECT 
                    roll_number, student_name, dept_code, course_code, course_title,
                    section_name, academic_term, total_counted_classes, present_count,
                    absent_count, leave_count, attendance_percentage
                FROM v_student_course_attendance
                WHERE 1=1
            """
            params = []
            if dept_id and dept_id.isdigit():
                query += " AND dept_id = %s"
                params.append(int(dept_id))
            if course_id and course_id.isdigit():
                query += " AND course_id = %s"
                params.append(int(course_id))

            query += " ORDER BY roll_number, course_code"
            data = query_all(query, tuple(params))
            columns = [
                ('roll_number', 'Roll No'),
                ('student_name', 'Student Name'),
                ('dept_code', 'Dept'),
                ('course_code', 'Course Code'),
                ('course_title', 'Course Title'),
                ('section_name', 'Section'),
                ('total_counted_classes', 'Counted Classes'),
                ('present_count', 'Present'),
                ('absent_count', 'Absent'),
                ('leave_count', 'Leave'),
                ('attendance_percentage', 'Attendance %')
            ]

        # --------------------------------------------------------------------
        # Report 2: Course-wise Attendance Summary
        # Demonstrates: JOINs, COUNT, SUM, ROUND, GROUP BY
        # --------------------------------------------------------------------
        elif report_type == 'course_summary':
            report_title = "Course-wise Attendance Summary"
            report_description = "Aggregated course metrics showing sections, conducted sessions, student attendance rates across courses."

            query = """
                SELECT 
                    c.course_code,
                    c.course_title,
                    c.credits,
                    d.dept_code,
                    COUNT(DISTINCT sec.section_id) AS sections_count,
                    COUNT(DISTINCT cs.session_id) AS total_sessions_conducted,
                    COUNT(a.attendance_id) AS total_attendance_entries,
                    SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) AS total_presents,
                    COALESCE(
                        ROUND(
                            (SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) / 
                             NULLIF(COUNT(a.attendance_id), 0)) * 100, 
                            2
                        ), 
                        0.0
                    ) AS overall_attendance_pct
                FROM courses c
                JOIN departments d ON c.dept_id = d.dept_id
                LEFT JOIN sections sec ON c.course_id = sec.course_id AND sec.is_active = TRUE
                LEFT JOIN class_sessions cs ON sec.section_id = cs.section_id
                LEFT JOIN attendance a ON cs.session_id = a.session_id
                WHERE 1=1
            """
            params = []
            if dept_id and dept_id.isdigit():
                query += " AND c.dept_id = %s"
                params.append(int(dept_id))

            query += """
                GROUP BY c.course_id, c.course_code, c.course_title, c.credits, d.dept_code
                ORDER BY c.course_code ASC
            """
            data = query_all(query, tuple(params))
            columns = [
                ('course_code', 'Course Code'),
                ('course_title', 'Course Title'),
                ('credits', 'Credits'),
                ('dept_code', 'Dept'),
                ('sections_count', 'Active Sections'),
                ('total_sessions_conducted', 'Sessions Held'),
                ('total_presents', 'Total Present Marks'),
                ('overall_attendance_pct', 'Average Attendance %')
            ]

        # --------------------------------------------------------------------
        # Report 3: Students Below Threshold (Shortage List)
        # Demonstrates: HAVING clause, aggregate filtering, threshold calculation
        # --------------------------------------------------------------------
        elif report_type == 'shortage':
            report_title = f"Attendance Shortage List (< {threshold}%)"
            report_description = "Official shortage roster identifying students currently below the minimum required attendance threshold."

            query = """
                SELECT 
                    s.roll_number,
                    s.full_name AS student_name,
                    s.email,
                    d.dept_code,
                    c.course_code,
                    c.course_title,
                    sec.section_name,
                    COUNT(a.attendance_id) AS total_counted,
                    SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) AS attended,
                    SUM(CASE WHEN a.status = 'absent' THEN 1 ELSE 0 END) AS missed,
                    COALESCE(
                        ROUND(
                            (SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) / 
                             NULLIF(COUNT(a.attendance_id), 0)) * 100, 
                            2
                        ), 
                        0.0
                    ) AS current_pct,
                    %s AS required_threshold,
                    GREATEST(0, CEIL((%s * COUNT(a.attendance_id) / 100) - SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END))) AS classes_shortfall
                FROM enrollments e
                JOIN students s ON e.student_id = s.student_id
                JOIN departments d ON s.dept_id = d.dept_id
                JOIN sections sec ON e.section_id = sec.section_id
                JOIN courses c ON sec.course_id = c.course_id
                JOIN class_sessions cs ON sec.section_id = cs.section_id
                JOIN attendance a ON cs.session_id = a.session_id AND a.student_id = s.student_id
                WHERE e.status = 'enrolled'
            """
            params = [threshold, threshold]
            if dept_id and dept_id.isdigit():
                query += " AND s.dept_id = %s"
                params.append(int(dept_id))

            query += """
                GROUP BY e.enrollment_id, s.roll_number, s.full_name, s.email, d.dept_code, c.course_code, c.course_title, sec.section_name
                HAVING COUNT(a.attendance_id) >= 2 AND current_pct < %s
                ORDER BY current_pct ASC, s.roll_number ASC
            """
            params.append(threshold)
            data = query_all(query, tuple(params))
            columns = [
                ('roll_number', 'Roll Number'),
                ('student_name', 'Student Name'),
                ('dept_code', 'Dept'),
                ('course_code', 'Course'),
                ('section_name', 'Section'),
                ('total_counted', 'Total Classes'),
                ('attended', 'Attended'),
                ('missed', 'Missed'),
                ('current_pct', 'Current %'),
                ('required_threshold', 'Required %'),
                ('classes_shortfall', 'Shortfall (Classes)')
            ]

        # --------------------------------------------------------------------
        # Report 4: Leave Application History and Decision Status
        # Demonstrates: Multi-table JOINs, review audit trail, date filtering
        # --------------------------------------------------------------------
        elif report_type == 'leave_history':
            report_title = "Leave Application & Decision Audit History"
            report_description = "Complete history of submitted student leave requests, approvals, reviewer identity, and remarks."

            query = """
                SELECT 
                    la.application_id,
                    s.roll_number,
                    s.full_name AS student_name,
                    d.dept_code,
                    lt.type_name AS leave_type,
                    la.start_date,
                    la.end_date,
                    la.total_days,
                    la.reason,
                    la.status AS decision_status,
                    COALESCE(rf.full_name, ru.username, 'Pending Review') AS reviewed_by_name,
                    lap.decision_notes,
                    lap.reviewed_at
                FROM leave_applications la
                JOIN students s ON la.student_id = s.student_id
                JOIN departments d ON s.dept_id = d.dept_id
                JOIN leave_types lt ON la.leave_type_id = lt.leave_type_id
                LEFT JOIN leave_approvals lap ON la.application_id = lap.application_id
                LEFT JOIN users ru ON lap.reviewed_by = ru.user_id
                LEFT JOIN faculty rf ON ru.user_id = rf.user_id
                WHERE 1=1
            """
            params = []
            if dept_id and dept_id.isdigit():
                query += " AND s.dept_id = %s"
                params.append(int(dept_id))

            query += " ORDER BY la.applied_at DESC"
            data = query_all(query, tuple(params))
            columns = [
                ('application_id', 'App #'),
                ('roll_number', 'Roll No'),
                ('student_name', 'Student Name'),
                ('dept_code', 'Dept'),
                ('leave_type', 'Type'),
                ('start_date', 'From'),
                ('end_date', 'To'),
                ('total_days', 'Days'),
                ('decision_status', 'Status'),
                ('reviewed_by_name', 'Reviewed By'),
                ('decision_notes', 'Decision Notes')
            ]

        # --------------------------------------------------------------------
        # Report 5: Pending Leave Applications
        # --------------------------------------------------------------------
        elif report_type == 'pending_leaves':
            report_title = "Pending Leave Applications Queue"
            report_description = "List of all student leave requests currently awaiting faculty review and action."

            query = """
                SELECT 
                    la.application_id,
                    s.roll_number,
                    s.full_name AS student_name,
                    s.email,
                    d.dept_code,
                    lt.type_name AS leave_type,
                    la.start_date,
                    la.end_date,
                    la.total_days,
                    la.reason,
                    la.applied_at
                FROM leave_applications la
                JOIN students s ON la.student_id = s.student_id
                JOIN departments d ON s.dept_id = d.dept_id
                JOIN leave_types lt ON la.leave_type_id = lt.leave_type_id
                WHERE la.status = 'pending'
            """
            params = []
            if dept_id and dept_id.isdigit():
                query += " AND s.dept_id = %s"
                params.append(int(dept_id))

            query += " ORDER BY la.applied_at ASC"
            data = query_all(query, tuple(params))
            columns = [
                ('application_id', 'App #'),
                ('roll_number', 'Roll No'),
                ('student_name', 'Student Name'),
                ('email', 'Email'),
                ('dept_code', 'Dept'),
                ('leave_type', 'Leave Type'),
                ('start_date', 'Start Date'),
                ('end_date', 'End Date'),
                ('total_days', 'Days'),
                ('reason', 'Reason'),
                ('applied_at', 'Submission Time')
            ]

        # --------------------------------------------------------------------
        # Report 6: Faculty-wise Allocation and Teaching Load
        # Demonstrates: Subqueries, aggregations across allocations
        # --------------------------------------------------------------------
        elif report_type == 'faculty_allocation':
            report_title = "Faculty Course & Section Allocation Matrix"
            report_description = "Overview of faculty workload, assigned courses, sections, and total enrolled students."

            query = """
                SELECT 
                    f.employee_id,
                    f.full_name AS faculty_name,
                    f.designation,
                    d.dept_code,
                    COUNT(DISTINCT sec.section_id) AS allocated_sections,
                    COUNT(DISTINCT sec.course_id) AS distinct_courses,
                    COUNT(DISTINCT cs.session_id) AS sessions_taught,
                    COALESCE(SUM(e_sub.enrolled_students), 0) AS total_student_load
                FROM faculty f
                JOIN departments d ON f.dept_id = d.dept_id
                LEFT JOIN sections sec ON f.faculty_id = sec.faculty_id AND sec.is_active = TRUE
                LEFT JOIN class_sessions cs ON sec.section_id = cs.section_id
                LEFT JOIN (
                    SELECT section_id, COUNT(student_id) AS enrolled_students
                    FROM enrollments
                    WHERE status = 'enrolled'
                    GROUP BY section_id
                ) e_sub ON sec.section_id = e_sub.section_id
                WHERE f.is_active = TRUE
            """
            params = []
            if dept_id and dept_id.isdigit():
                query += " AND f.dept_id = %s"
                params.append(int(dept_id))

            query += """
                GROUP BY f.faculty_id, f.employee_id, f.full_name, f.designation, d.dept_code
                ORDER BY f.full_name ASC
            """
            data = query_all(query, tuple(params))
            columns = [
                ('employee_id', 'Employee ID'),
                ('faculty_name', 'Faculty Name'),
                ('designation', 'Designation'),
                ('dept_code', 'Dept'),
                ('allocated_sections', 'Allocated Sections'),
                ('distinct_courses', 'Distinct Courses'),
                ('sessions_taught', 'Sessions Taught'),
                ('total_student_load', 'Total Student Load')
            ]

        # --------------------------------------------------------------------
        # Report 7: Makeup Session Participation
        # --------------------------------------------------------------------
        elif report_type == 'makeup_participation':
            report_title = "Makeup Session Participation & Recovery"
            report_description = "Participation metrics for scheduled makeup sessions designed for attendance recovery."

            query = """
                SELECT 
                    ms.makeup_id,
                    c.course_code,
                    sec.section_name,
                    f.full_name AS faculty_name,
                    ms.session_date,
                    ms.classroom,
                    ms.topic,
                    ms.status AS session_status,
                    COUNT(ma.makeup_att_id) AS recorded_participants,
                    SUM(CASE WHEN ma.status = 'present' THEN 1 ELSE 0 END) AS students_attended
                FROM makeup_sessions ms
                JOIN sections sec ON ms.section_id = sec.section_id
                JOIN courses c ON sec.course_id = c.course_id
                JOIN faculty f ON ms.faculty_id = f.faculty_id
                LEFT JOIN makeup_attendance ma ON ms.makeup_id = ma.makeup_id
                GROUP BY ms.makeup_id, c.course_code, sec.section_name, f.full_name, ms.session_date, ms.classroom, ms.topic, ms.status
                ORDER BY ms.session_date DESC
            """
            data = query_all(query)
            columns = [
                ('makeup_id', 'Session #'),
                ('course_code', 'Course'),
                ('section_name', 'Section'),
                ('faculty_name', 'Faculty'),
                ('session_date', 'Date'),
                ('classroom', 'Room'),
                ('topic', 'Topic'),
                ('session_status', 'Status'),
                ('students_attended', 'Students Attended')
            ]

        # --------------------------------------------------------------------
        # Report 8: Monthly Attendance Trends
        # Demonstrates: DATE_FORMAT, aggregation over time intervals
        # --------------------------------------------------------------------
        elif report_type == 'monthly_trends':
            report_title = "Monthly Attendance Trends Analysis"
            report_description = "Chronological attendance patterns, counted classes, and institutional engagement over time."

            query = """
                SELECT 
                    DATE_FORMAT(cs.session_date, '%Y-%m') AS year_month,
                    DATE_FORMAT(cs.session_date, '%M %Y') AS month_name,
                    COUNT(DISTINCT cs.session_id) AS total_sessions,
                    COUNT(a.attendance_id) AS total_counted_records,
                    SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) AS present_count,
                    SUM(CASE WHEN a.status = 'absent' THEN 1 ELSE 0 END) AS absent_count,
                    SUM(CASE WHEN a.status = 'leave' THEN 1 ELSE 0 END) AS leave_count,
                    COALESCE(
                        ROUND(
                            (SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) / 
                             NULLIF(COUNT(a.attendance_id), 0)) * 100, 
                            2
                        ), 
                        0.0
                    ) AS monthly_pct
                FROM class_sessions cs
                LEFT JOIN attendance a ON cs.session_id = a.session_id
                GROUP BY year_month, month_name
                ORDER BY year_month ASC
            """
            data = query_all(query)
            columns = [
                ('month_name', 'Month & Year'),
                ('total_sessions', 'Sessions Held'),
                ('total_counted_records', 'Counted Attendance Records'),
                ('present_count', 'Total Present'),
                ('absent_count', 'Total Absent'),
                ('leave_count', 'Total Leave'),
                ('monthly_pct', 'Attendance Rate %')
            ]

        # CSV Export Handling
        if request.args.get('export') == 'csv':
            output = io.StringIO()
            writer = csv.writer(output)
            # Write header
            writer.writerow([label for _, label in columns])
            # Write rows
            for row in data:
                writer.writerow([row.get(key, '') for key, _ in columns])

            filename = f"AttendEase_{report_type}_{threshold}pct.csv"
            return Response(
                output.getvalue(),
                mimetype="text/csv",
                headers={"Content-Disposition": f"attachment;filename={filename}"}
            )

        return render_template(
            'reports.html',
            report_type=report_type,
            report_title=report_title,
            report_description=report_description,
            data=data,
            columns=columns,
            departments=departments,
            courses=courses,
            dept_id=dept_id,
            course_id=course_id,
            threshold=threshold
        )

    except Exception as e:
        flash(f"Error generating SQL report: {str(e)}", "danger")
        return render_template('reports.html', report_type=report_type, data=[], columns=[], departments=[], courses=[])
