-- ============================================================================
-- AttendEase: Realistic Sample Seed Data
-- Default Password for all accounts: Password@123
-- ============================================================================

USE attendease_db;

-- 1. System Settings
INSERT INTO system_settings (setting_key, setting_value, description) VALUES
('min_attendance_threshold', '75.0', 'Minimum percentage required to avoid shortage warning'),
('academic_year', '2026-2027', 'Current active academic year'),
('academic_term', 'Fall', 'Current active semester / term'),
('institution_name', 'Metropolitan Institute of Technology', 'College / University Name');

-- 2. Departments
INSERT INTO departments (dept_id, dept_code, dept_name) VALUES
(1, 'CSE', 'Computer Science and Engineering'),
(2, 'ECE', 'Electronics and Communication Engineering'),
(3, 'IT', 'Information Technology'),
(4, 'ME', 'Mechanical Engineering');

-- 3. Users (Hash for 'Password@123')
-- Hash: scrypt:32768:8:1$tU8DUaO7DnkC4yex$2bcff0a6f640376c608d865015815dc73f043f334fc53bddb9ac64d9f04e7447aeca36c5bc7885c7ea33bcf72945311006f395330d27ff708387ba024820ae1d
INSERT INTO users (user_id, username, email, password_hash, role, is_active) VALUES
(1, 'admin', 'admin@college.edu', 'scrypt:32768:8:1$tU8DUaO7DnkC4yex$2bcff0a6f640376c608d865015815dc73f043f334fc53bddb9ac64d9f04e7447aeca36c5bc7885c7ea33bcf72945311006f395330d27ff708387ba024820ae1d', 'admin', TRUE),
(2, 'prof_alan', 'alan.turing@college.edu', 'scrypt:32768:8:1$tU8DUaO7DnkC4yex$2bcff0a6f640376c608d865015815dc73f043f334fc53bddb9ac64d9f04e7447aeca36c5bc7885c7ea33bcf72945311006f395330d27ff708387ba024820ae1d', 'faculty', TRUE),
(3, 'prof_grace', 'grace.hopper@college.edu', 'scrypt:32768:8:1$tU8DUaO7DnkC4yex$2bcff0a6f640376c608d865015815dc73f043f334fc53bddb9ac64d9f04e7447aeca36c5bc7885c7ea33bcf72945311006f395330d27ff708387ba024820ae1d', 'faculty', TRUE),
(4, 'prof_claude', 'claude.shannon@college.edu', 'scrypt:32768:8:1$tU8DUaO7DnkC4yex$2bcff0a6f640376c608d865015815dc73f043f334fc53bddb9ac64d9f04e7447aeca36c5bc7885c7ea33bcf72945311006f395330d27ff708387ba024820ae1d', 'faculty', TRUE),
(5, 'alex_rivera', 'alex.r@college.edu', 'scrypt:32768:8:1$tU8DUaO7DnkC4yex$2bcff0a6f640376c608d865015815dc73f043f334fc53bddb9ac64d9f04e7447aeca36c5bc7885c7ea33bcf72945311006f395330d27ff708387ba024820ae1d', 'student', TRUE),
(6, 'priya_patel', 'priya.p@college.edu', 'scrypt:32768:8:1$tU8DUaO7DnkC4yex$2bcff0a6f640376c608d865015815dc73f043f334fc53bddb9ac64d9f04e7447aeca36c5bc7885c7ea33bcf72945311006f395330d27ff708387ba024820ae1d', 'student', TRUE),
(7, 'marcus_vance', 'marcus.v@college.edu', 'scrypt:32768:8:1$tU8DUaO7DnkC4yex$2bcff0a6f640376c608d865015815dc73f043f334fc53bddb9ac64d9f04e7447aeca36c5bc7885c7ea33bcf72945311006f395330d27ff708387ba024820ae1d', 'student', TRUE),
(8, 'elena_rostova', 'elena.r@college.edu', 'scrypt:32768:8:1$tU8DUaO7DnkC4yex$2bcff0a6f640376c608d865015815dc73f043f334fc53bddb9ac64d9f04e7447aeca36c5bc7885c7ea33bcf72945311006f395330d27ff708387ba024820ae1d', 'student', TRUE),
(9, 'david_kim', 'david.k@college.edu', 'scrypt:32768:8:1$tU8DUaO7DnkC4yex$2bcff0a6f640376c608d865015815dc73f043f334fc53bddb9ac64d9f04e7447aeca36c5bc7885c7ea33bcf72945311006f395330d27ff708387ba024820ae1d', 'student', TRUE),
(10, 'sarah_connor', 'sarah.c@college.edu', 'scrypt:32768:8:1$tU8DUaO7DnkC4yex$2bcff0a6f640376c608d865015815dc73f043f334fc53bddb9ac64d9f04e7447aeca36c5bc7885c7ea33bcf72945311006f395330d27ff708387ba024820ae1d', 'student', TRUE);

-- 4. Faculty Profiles
INSERT INTO faculty (faculty_id, user_id, employee_id, full_name, email, dept_id, designation, phone) VALUES
(1, 2, 'FAC-CSE-001', 'Dr. Alan Turing', 'alan.turing@college.edu', 1, 'Professor & HOD', '+1 555-0101'),
(2, 3, 'FAC-CSE-002', 'Dr. Grace Hopper', 'grace.hopper@college.edu', 1, 'Associate Professor', '+1 555-0102'),
(3, 4, 'FAC-ECE-003', 'Dr. Claude Shannon', 'claude.shannon@college.edu', 2, 'Assistant Professor', '+1 555-0103');

-- 5. Student Profiles
INSERT INTO students (student_id, user_id, roll_number, full_name, email, dept_id, program, current_semester, phone) VALUES
(1, 5, 'CS-2024-001', 'Alex Rivera', 'alex.r@college.edu', 1, 'B.Tech Computer Science', 4, '+1 555-0201'),
(2, 6, 'CS-2024-002', 'Priya Patel', 'priya.p@college.edu', 1, 'B.Tech Computer Science', 4, '+1 555-0202'),
(3, 7, 'CS-2024-003', 'Marcus Vance', 'marcus.v@college.edu', 1, 'B.Tech Computer Science', 4, '+1 555-0203'),
(4, 8, 'CS-2024-004', 'Elena Rostova', 'elena.r@college.edu', 1, 'B.Tech Computer Science', 4, '+1 555-0204'),
(5, 9, 'EC-2024-010', 'David Kim', 'david.k@college.edu', 2, 'B.Tech Electronics & Comm', 4, '+1 555-0205'),
(6, 10, 'IT-2024-020', 'Sarah Connor', 'sarah.c@college.edu', 3, 'B.Tech Information Tech', 4, '+1 555-0206');

-- 6. Courses
INSERT INTO courses (course_id, course_code, course_title, credits, dept_id) VALUES
(1, 'CS301', 'Database Management Systems', 4, 1),
(2, 'CS302', 'Operating Systems', 4, 1),
(3, 'CS303', 'Computer Networks', 3, 1),
(4, 'EC301', 'Digital Signal Processing', 4, 2);

-- 7. Sections
INSERT INTO sections (section_id, course_id, faculty_id, section_name, academic_term, academic_year, classroom, max_capacity) VALUES
(1, 1, 1, 'CS301-A', 'Fall', '2026-2027', 'Lecture Hall 101', 60),
(2, 2, 2, 'CS302-A', 'Fall', '2026-2027', 'Lecture Hall 102', 60),
(3, 3, 1, 'CS303-A', 'Fall', '2026-2027', 'Networking Lab 2', 40),
(4, 4, 3, 'EC301-A', 'Fall', '2026-2027', 'Lecture Hall 205', 50);

-- 8. Enrollments
INSERT INTO enrollments (enrollment_id, student_id, section_id, status) VALUES
(1, 1, 1, 'enrolled'), -- Alex in CS301-A
(2, 2, 1, 'enrolled'), -- Priya in CS301-A
(3, 3, 1, 'enrolled'), -- Marcus in CS301-A
(4, 4, 1, 'enrolled'), -- Elena in CS301-A
(5, 1, 2, 'enrolled'), -- Alex in CS302-A
(6, 2, 2, 'enrolled'), -- Priya in CS302-A
(7, 3, 2, 'enrolled'), -- Marcus in CS302-A
(8, 4, 2, 'enrolled'), -- Elena in CS302-A
(9, 1, 3, 'enrolled'), -- Alex in CS303-A
(10, 2, 3, 'enrolled'), -- Priya in CS303-A
(11, 5, 4, 'enrolled'); -- David in EC301-A

-- 9. Class Sessions
INSERT INTO class_sessions (session_id, section_id, faculty_id, session_date, start_time, end_time, topic, session_type) VALUES
(1, 1, 1, '2026-10-01', '09:00:00', '10:00:00', 'Relational Model & Keys', 'regular'),
(2, 1, 1, '2026-10-02', '09:00:00', '10:00:00', 'Relational Algebra & Calculus', 'regular'),
(3, 1, 1, '2026-10-05', '09:00:00', '10:00:00', 'SQL DDL and DML Statements', 'regular'),
(4, 1, 1, '2026-10-06', '09:00:00', '10:00:00', 'SQL Joins & Aggregations', 'regular'),
(5, 1, 1, '2026-10-07', '09:00:00', '10:00:00', 'Subqueries & Nested Views', 'regular'),
(6, 1, 1, '2026-10-08', '09:00:00', '10:00:00', 'Functional Dependencies & 1NF/2NF', 'regular'),
(7, 1, 1, '2026-10-09', '09:00:00', '10:00:00', 'Third Normal Form (3NF) & BCNF', 'regular'),
(8, 1, 1, '2026-10-12', '09:00:00', '10:00:00', 'Transaction Processing & ACID', 'regular'),
(9, 2, 2, '2026-10-02', '10:30:00', '11:30:00', 'Process Management & PCB', 'regular'),
(10, 2, 2, '2026-10-05', '10:30:00', '11:30:00', 'CPU Scheduling Algorithms', 'regular'),
(11, 2, 2, '2026-10-07', '10:30:00', '11:30:00', 'Deadlock Detection & Recovery', 'regular'),
(12, 2, 2, '2026-10-09', '10:30:00', '11:30:00', 'Memory Management & Paging', 'regular');

-- 10. Attendance Records for CS301-A (8 Sessions)
-- Alex: 8/8 Present (100%)
-- Priya: 7 Present, 1 Leave on 2026-10-05 (87.5% present)
-- Marcus: 4 Present, 4 Absent (50% - Shortage!)
-- Elena: 6 Present, 2 Absent (75% - Borderline threshold)
INSERT INTO attendance (session_id, student_id, status, remarks, marked_by) VALUES
-- Session 1
(1, 1, 'present', 'On time', 2),
(1, 2, 'present', 'On time', 2),
(1, 3, 'present', 'On time', 2),
(1, 4, 'present', 'On time', 2),
-- Session 2
(2, 1, 'present', 'On time', 2),
(2, 2, 'present', 'On time', 2),
(2, 3, 'present', 'On time', 2),
(2, 4, 'present', 'On time', 2),
-- Session 3 (Priya on Medical Leave, Marcus Absent)
(3, 1, 'present', 'On time', 2),
(3, 2, 'leave', 'Approved Medical Leave #1', 2),
(3, 3, 'absent', 'Unexcused', 2),
(3, 4, 'present', 'On time', 2),
-- Session 4 (Marcus Absent)
(4, 1, 'present', 'On time', 2),
(4, 2, 'present', 'On time', 2),
(4, 3, 'absent', 'Unexcused', 2),
(4, 4, 'present', 'On time', 2),
-- Session 5 (Elena Absent, Marcus Absent)
(5, 1, 'present', 'On time', 2),
(5, 2, 'present', 'On time', 2),
(5, 3, 'absent', 'Unexcused', 2),
(5, 4, 'absent', 'Sick', 2),
-- Session 6
(6, 1, 'present', 'On time', 2),
(6, 2, 'present', 'On time', 2),
(6, 3, 'present', 'On time', 2),
(6, 4, 'present', 'On time', 2),
-- Session 7 (Marcus Absent, Elena Absent)
(7, 1, 'present', 'On time', 2),
(7, 2, 'present', 'On time', 2),
(7, 3, 'absent', 'Unexcused', 2),
(7, 4, 'absent', 'Unexcused', 2),
-- Session 8
(8, 1, 'present', 'On time', 2),
(8, 2, 'present', 'On time', 2),
(8, 3, 'present', 'On time', 2),
(8, 4, 'present', 'On time', 2);

-- 11. Leave Types
INSERT INTO leave_types (leave_type_id, type_name, max_days_per_term, description) VALUES
(1, 'Medical', 12, 'Illness, hospitalization, or medical appointments with valid doctor certificate'),
(2, 'Personal / Family', 5, 'Personal urgent matters or unavoidable family events'),
(3, 'Emergency', 7, 'Unforeseen urgent emergencies'),
(4, 'Academic / On-Duty', 10, 'Representing the college in seminars, hackathons, or official sports meets');

-- 12. Leave Applications
INSERT INTO leave_applications (application_id, student_id, leave_type_id, start_date, end_date, total_days, reason, status, applied_at) VALUES
(1, 2, 1, '2026-10-05', '2026-10-05', 1, 'Severe viral fever and flu symptoms. Prescribed doctor bed rest.', 'approved', '2026-10-04 18:30:00'),
(2, 3, 2, '2026-10-07', '2026-10-07', 1, 'Attending family function out of town.', 'rejected', '2026-10-06 20:15:00'),
(3, 1, 4, '2026-10-15', '2026-10-16', 2, 'Selected to represent college at National Inter-University Hackathon 2026.', 'pending', '2026-10-12 11:00:00');

-- 13. Leave Approvals Audit
INSERT INTO leave_approvals (approval_id, application_id, reviewed_by, decision, decision_notes, reviewed_at) VALUES
(1, 1, 2, 'approved', 'Medical certificate verified. Approved for 1 day.', '2026-10-05 08:00:00'),
(2, 2, 2, 'rejected', 'Critical 3NF lecture on this date and student attendance is already below standard threshold.', '2026-10-07 08:15:00');

-- 14. Makeup Sessions
INSERT INTO makeup_sessions (makeup_id, section_id, original_session_id, faculty_id, session_date, start_time, end_time, classroom, topic, status) VALUES
(1, 1, 3, 1, '2026-10-13', '15:00:00', '16:00:00', 'Lecture Hall 101', 'Extra Makeup: DDL/DML & Constraints Hands-on', 'completed'),
(2, 1, 7, 1, '2026-10-18', '14:00:00', '15:30:00', 'Lab 2', 'Makeup Tutorial: Normalization Decompositions & Lossless Join', 'scheduled');

-- 15. Makeup Attendance
INSERT INTO makeup_attendance (makeup_id, student_id, status, marked_by) VALUES
(1, 3, 'present', 2), -- Marcus Vance attended makeup session #1
(1, 4, 'present', 2); -- Elena Rostova attended makeup session #1

-- 16. Attendance Alerts
INSERT INTO attendance_alerts (alert_id, student_id, section_id, current_percentage, threshold_percentage, classes_attended, classes_missed, status) VALUES
(1, 3, 1, 50.00, 75.00, 4, 4, 'active');

-- 17. Initial Audit Logs
INSERT INTO audit_logs (user_id, action, entity_type, entity_id, details) VALUES
(1, 'DATABASE_SEED', 'SYSTEM', 1, 'System seeded with standard departments, courses, and fall term sections'),
(2, 'SESSION_CREATED', 'class_sessions', 1, 'Prof. Alan Turing created session for CS301-A'),
(2, 'ATTENDANCE_MARKED', 'attendance', 1, 'Attendance marked for 4 students in CS301-A'),
(2, 'LEAVE_DECISION', 'leave_applications', 1, 'Prof. Alan Turing APPROVED leave request #1 for Priya Patel'),
(2, 'LEAVE_DECISION', 'leave_applications', 2, 'Prof. Alan Turing REJECTED leave request #2 for Marcus Vance');
