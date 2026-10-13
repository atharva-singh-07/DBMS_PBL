-- ============================================================================
-- AttendEase: Student Attendance and Leave Approval Management System
-- Database Schema Definition (Target: 3NF Relational Model)
-- Compatible with MySQL 8.0+
-- ============================================================================

CREATE DATABASE IF NOT EXISTS attendease_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE attendease_db;

-- Disable foreign key checks during schema creation/reset
SET FOREIGN_KEY_CHECKS = 0;

-- Drop existing views and tables if rebuilding
DROP VIEW IF EXISTS v_student_course_attendance;
DROP VIEW IF EXISTS v_section_summary;
DROP TABLE IF EXISTS audit_logs;
DROP TABLE IF EXISTS attendance_alerts;
DROP TABLE IF EXISTS makeup_attendance;
DROP TABLE IF EXISTS makeup_sessions;
DROP TABLE IF EXISTS leave_approvals;
DROP TABLE IF EXISTS leave_applications;
DROP TABLE IF EXISTS leave_types;
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS class_sessions;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS sections;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS faculty;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS system_settings;

SET FOREIGN_KEY_CHECKS = 1;

-- ----------------------------------------------------------------------------
-- 1. SYSTEM SETTINGS
-- ----------------------------------------------------------------------------
CREATE TABLE system_settings (
    setting_id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(50) NOT NULL UNIQUE,
    setting_value VARCHAR(255) NOT NULL,
    description VARCHAR(255) NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- 2. DEPARTMENTS
-- ----------------------------------------------------------------------------
CREATE TABLE departments (
    dept_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_code VARCHAR(20) NOT NULL UNIQUE,
    dept_name VARCHAR(150) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- 3. USERS (Authentication & Role Base)
-- ----------------------------------------------------------------------------
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'faculty', 'student') NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_role (role),
    INDEX idx_user_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- 4. STUDENTS
-- ----------------------------------------------------------------------------
CREATE TABLE students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    roll_number VARCHAR(50) NOT NULL UNIQUE,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    dept_id INT NOT NULL,
    program VARCHAR(100) NOT NULL,
    current_semester INT NOT NULL DEFAULT 1,
    phone VARCHAR(25) NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_students_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_students_dept FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON DELETE RESTRICT,
    INDEX idx_student_dept (dept_id),
    INDEX idx_student_roll (roll_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- 5. FACULTY
-- ----------------------------------------------------------------------------
CREATE TABLE faculty (
    faculty_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    employee_id VARCHAR(50) NOT NULL UNIQUE,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    dept_id INT NOT NULL,
    designation VARCHAR(100) NOT NULL DEFAULT 'Assistant Professor',
    phone VARCHAR(25) NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_faculty_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_faculty_dept FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON DELETE RESTRICT,
    INDEX idx_faculty_dept (dept_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- 6. COURSES
-- ----------------------------------------------------------------------------
CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(30) NOT NULL UNIQUE,
    course_title VARCHAR(150) NOT NULL,
    credits INT NOT NULL DEFAULT 3,
    dept_id INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_courses_dept FOREIGN KEY (dept_id) REFERENCES departments(dept_id) ON DELETE RESTRICT,
    INDEX idx_course_dept (dept_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- 7. SECTIONS
-- ----------------------------------------------------------------------------
CREATE TABLE sections (
    section_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    faculty_id INT NOT NULL,
    section_name VARCHAR(50) NOT NULL,
    academic_term VARCHAR(30) NOT NULL,
    academic_year VARCHAR(20) NOT NULL,
    classroom VARCHAR(50) NOT NULL,
    max_capacity INT NOT NULL DEFAULT 60,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sections_course FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE RESTRICT,
    CONSTRAINT fk_sections_faculty FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id) ON DELETE RESTRICT,
    CONSTRAINT uq_course_section_term UNIQUE (course_id, section_name, academic_term, academic_year),
    INDEX idx_sections_faculty (faculty_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- 8. ENROLLMENTS
-- ----------------------------------------------------------------------------
CREATE TABLE enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    section_id INT NOT NULL,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('enrolled', 'dropped', 'completed') NOT NULL DEFAULT 'enrolled',
    CONSTRAINT fk_enrollments_student FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    CONSTRAINT fk_enrollments_section FOREIGN KEY (section_id) REFERENCES sections(section_id) ON DELETE CASCADE,
    CONSTRAINT uq_student_section UNIQUE (student_id, section_id),
    INDEX idx_enrollment_section (section_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- 9. CLASS SESSIONS
-- ----------------------------------------------------------------------------
CREATE TABLE class_sessions (
    session_id INT AUTO_INCREMENT PRIMARY KEY,
    section_id INT NOT NULL,
    faculty_id INT NOT NULL,
    session_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    topic VARCHAR(255) NULL,
    session_type ENUM('regular', 'extra', 'lab') NOT NULL DEFAULT 'regular',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sessions_section FOREIGN KEY (section_id) REFERENCES sections(section_id) ON DELETE CASCADE,
    CONSTRAINT fk_sessions_faculty FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id) ON DELETE RESTRICT,
    INDEX idx_session_date (session_date),
    INDEX idx_session_section (section_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- 10. ATTENDANCE
-- ----------------------------------------------------------------------------
CREATE TABLE attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    student_id INT NOT NULL,
    status ENUM('present', 'absent', 'leave') NOT NULL,
    remarks VARCHAR(255) NULL,
    marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    marked_by INT NOT NULL,
    CONSTRAINT fk_attendance_session FOREIGN KEY (session_id) REFERENCES class_sessions(session_id) ON DELETE CASCADE,
    CONSTRAINT fk_attendance_student FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    CONSTRAINT fk_attendance_marker FOREIGN KEY (marked_by) REFERENCES users(user_id) ON DELETE RESTRICT,
    CONSTRAINT uq_session_student UNIQUE (session_id, student_id),
    INDEX idx_att_student (student_id),
    INDEX idx_att_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- 11. LEAVE TYPES
-- ----------------------------------------------------------------------------
CREATE TABLE leave_types (
    leave_type_id INT AUTO_INCREMENT PRIMARY KEY,
    type_name VARCHAR(50) NOT NULL UNIQUE,
    max_days_per_term INT NOT NULL DEFAULT 10,
    description VARCHAR(255) NULL,
    is_active BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- 12. LEAVE APPLICATIONS
-- ----------------------------------------------------------------------------
CREATE TABLE leave_applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    leave_type_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_days INT NOT NULL DEFAULT 1,
    reason TEXT NOT NULL,
    document_url VARCHAR(255) NULL,
    status ENUM('pending', 'approved', 'rejected') NOT NULL DEFAULT 'pending',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_leave_student FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    CONSTRAINT fk_leave_type FOREIGN KEY (leave_type_id) REFERENCES leave_types(leave_type_id) ON DELETE RESTRICT,
    CONSTRAINT chk_leave_dates CHECK (end_date >= start_date),
    INDEX idx_leave_student (student_id),
    INDEX idx_leave_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- 13. LEAVE APPROVALS (Decision Audit)
-- ----------------------------------------------------------------------------
CREATE TABLE leave_approvals (
    approval_id INT AUTO_INCREMENT PRIMARY KEY,
    application_id INT NOT NULL,
    reviewed_by INT NOT NULL,
    decision ENUM('approved', 'rejected') NOT NULL,
    decision_notes TEXT NULL,
    reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_approvals_app FOREIGN KEY (application_id) REFERENCES leave_applications(application_id) ON DELETE CASCADE,
    CONSTRAINT fk_approvals_reviewer FOREIGN KEY (reviewed_by) REFERENCES users(user_id) ON DELETE RESTRICT,
    INDEX idx_approvals_app (application_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- 14. MAKEUP SESSIONS
-- ----------------------------------------------------------------------------
CREATE TABLE makeup_sessions (
    makeup_id INT AUTO_INCREMENT PRIMARY KEY,
    section_id INT NOT NULL,
    original_session_id INT NULL,
    faculty_id INT NOT NULL,
    session_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    classroom VARCHAR(50) NOT NULL,
    topic VARCHAR(255) NOT NULL,
    status ENUM('scheduled', 'completed', 'cancelled') NOT NULL DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_makeup_section FOREIGN KEY (section_id) REFERENCES sections(section_id) ON DELETE CASCADE,
    CONSTRAINT fk_makeup_orig_session FOREIGN KEY (original_session_id) REFERENCES class_sessions(session_id) ON DELETE SET NULL,
    CONSTRAINT fk_makeup_faculty FOREIGN KEY (faculty_id) REFERENCES faculty(faculty_id) ON DELETE RESTRICT,
    INDEX idx_makeup_section (section_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- 15. MAKEUP ATTENDANCE
-- ----------------------------------------------------------------------------
CREATE TABLE makeup_attendance (
    makeup_att_id INT AUTO_INCREMENT PRIMARY KEY,
    makeup_id INT NOT NULL,
    student_id INT NOT NULL,
    status ENUM('present', 'absent') NOT NULL DEFAULT 'present',
    marked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    marked_by INT NOT NULL,
    CONSTRAINT fk_makeup_att_session FOREIGN KEY (makeup_id) REFERENCES makeup_sessions(makeup_id) ON DELETE CASCADE,
    CONSTRAINT fk_makeup_att_student FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    CONSTRAINT fk_makeup_att_marker FOREIGN KEY (marked_by) REFERENCES users(user_id) ON DELETE RESTRICT,
    CONSTRAINT uq_makeup_student UNIQUE (makeup_id, student_id),
    INDEX idx_makeup_att_student (student_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- 16. ATTENDANCE ALERTS
-- ----------------------------------------------------------------------------
CREATE TABLE attendance_alerts (
    alert_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    section_id INT NOT NULL,
    current_percentage DECIMAL(5,2) NOT NULL,
    threshold_percentage DECIMAL(5,2) NOT NULL DEFAULT 75.00,
    classes_attended INT NOT NULL,
    classes_missed INT NOT NULL,
    status ENUM('active', 'resolved', 'acknowledged') NOT NULL DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_alerts_student FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    CONSTRAINT fk_alerts_section FOREIGN KEY (section_id) REFERENCES sections(section_id) ON DELETE CASCADE,
    INDEX idx_alerts_student (student_id),
    INDEX idx_alerts_section (section_id),
    INDEX idx_alerts_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------------------------------------------------------
-- 17. AUDIT LOGS
-- ----------------------------------------------------------------------------
CREATE TABLE audit_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id INT NULL,
    details TEXT NULL,
    ip_address VARCHAR(45) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_audit_user FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL,
    INDEX idx_audit_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- SQL VIEWS FOR REUSABLE REPORTING AND AGGREGATION
-- ============================================================================

-- View 1: Student-wise Course Attendance Summary with Percentage
CREATE OR REPLACE VIEW v_student_course_attendance AS
SELECT 
    e.enrollment_id,
    e.student_id,
    s.roll_number,
    s.full_name AS student_name,
    s.dept_id,
    d.dept_code,
    d.dept_name,
    e.section_id,
    sec.section_name,
    sec.academic_term,
    sec.academic_year,
    c.course_id,
    c.course_code,
    c.course_title,
    c.credits,
    f.faculty_id,
    f.full_name AS faculty_name,
    COUNT(cs.session_id) AS total_sessions_conducted,
    COUNT(a.attendance_id) AS total_counted_classes,
    SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) AS present_count,
    SUM(CASE WHEN a.status = 'absent' THEN 1 ELSE 0 END) AS absent_count,
    SUM(CASE WHEN a.status = 'leave' THEN 1 ELSE 0 END) AS leave_count,
    COALESCE(
        ROUND(
            (SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) / 
             NULLIF(COUNT(a.attendance_id), 0)) * 100, 
            2
        ), 
        0.00
    ) AS attendance_percentage
FROM enrollments e
JOIN students s ON e.student_id = s.student_id
JOIN departments d ON s.dept_id = d.dept_id
JOIN sections sec ON e.section_id = sec.section_id
JOIN courses c ON sec.course_id = c.course_id
JOIN faculty f ON sec.faculty_id = f.faculty_id
LEFT JOIN class_sessions cs ON cs.section_id = sec.section_id
LEFT JOIN attendance a ON a.session_id = cs.session_id AND a.student_id = s.student_id
WHERE e.status = 'enrolled'
GROUP BY 
    e.enrollment_id, e.student_id, s.roll_number, s.full_name, s.dept_id,
    d.dept_code, d.dept_name, e.section_id, sec.section_name, sec.academic_term,
    sec.academic_year, c.course_id, c.course_code, c.course_title, c.credits,
    f.faculty_id, f.full_name;

-- View 2: Section Overview Summary
CREATE OR REPLACE VIEW v_section_summary AS
SELECT 
    sec.section_id,
    sec.section_name,
    sec.classroom,
    sec.academic_term,
    sec.academic_year,
    c.course_code,
    c.course_title,
    f.full_name AS faculty_name,
    COUNT(DISTINCT e.student_id) AS enrolled_students_count,
    COUNT(DISTINCT cs.session_id) AS total_sessions_conducted
FROM sections sec
JOIN courses c ON sec.course_id = c.course_id
JOIN faculty f ON sec.faculty_id = f.faculty_id
LEFT JOIN enrollments e ON sec.section_id = e.section_id AND e.status = 'enrolled'
LEFT JOIN class_sessions cs ON sec.section_id = cs.section_id
GROUP BY 
    sec.section_id, sec.section_name, sec.classroom, sec.academic_term,
    sec.academic_year, c.course_code, c.course_title, f.full_name;
