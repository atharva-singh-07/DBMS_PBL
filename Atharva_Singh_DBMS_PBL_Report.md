# WOXSEN UNIVERSITY
## SCHOOL OF TECHNOLOGY
### DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING
### DATABASE MANAGEMENT SYSTEMS (DBMS) — PROJECT-BASED LEARNING (PBL) REPORT

---

# ATTENDEASE: STUDENT ATTENDANCE AND LEAVE APPROVAL MANAGEMENT SYSTEM
### *Small Database Application Development using Python Flask and MySQL Server 8.0*

| Academic Detail | Project Information |
| :--- | :--- |
| **Program** | B.Tech in Computer Science and Engineering |
| **Course** | Database Management Systems (DBMS) |
| **Section** | Section A |
| **Academic Year** | 2026 – 2027 |
| **Date of Submission** | October 14, 2026 |
| **Submitted By** | Atharva Singh |
| **Roll Number** | CS-2024-001 |
| **Faculty Supervisor** | Course Faculty, School of Technology |
| **Repository Path** | `C:\Users\ATHARVA SINGH\Desktop\DBMS_PBL` |

---

## ACKNOWLEDGEMENT

I express my sincere gratitude to Woxsen University, School of Technology, for providing me with the opportunity to undertake this Project-Based Learning (PBL) activity as part of the Database Management Systems (DBMS) course.

I thank my course faculty for the valuable guidance, suggestions, and support throughout the design, normalization, and full-stack development of this project. The mentorship helped me understand the practical application of foundational database concepts, including Entity-Relationship (ER) modelling, Third Normal Form (3NF) relational decomposition, integrity constraints, parameterized queries, transaction safety, and role-based client-server architecture.

This PBL activity has significantly strengthened my conceptual understanding of relational database management systems and provided practical, industry-aligned experience in developing an enterprise-grade academic compliance application.

**Atharva Singh**  
Roll Number: CS-2024-001  
School of Technology, Woxsen University  

---

## UNDERTAKING

I hereby declare that the project entitled **"AttendEase: Student Attendance and Leave Approval Management System"**, submitted as part of the Project-Based Learning (PBL) activity for the Database Management Systems (DBMS) course, is my authentic individual work carried out under the guidance of the course faculty.

I undertake that the project report, relational database design, SQL scripts (`schema.sql` and `seed.sql`), application source code, validation routines, test cases, and supporting materials submitted by me have been prepared for academic purposes. Wherever existing literature, software libraries, tools, or resources have been referred to, appropriate acknowledgement and IEEE citations have been provided.

I further undertake that I am fully responsible for the technical accuracy and authenticity of the submitted work and that I have strictly adhered to the academic integrity and project guidelines prescribed by the University.

**Date:** October 14, 2026  
**Place:** Hyderabad, India  

**Signature:** ___________________________  
**Name:** Atharva Singh  
**Roll Number:** CS-2024-001  
**Program:** B.Tech Computer Science and Engineering  

---

## TABLE OF CONTENTS

- [Abstract & Keywords](#abstract)
- [List of Tables](#list-of-tables)
- [List of Figures](#list-of-figures)
- [List of Acronyms](#list-of-acronyms)
- [Chapter 1: Problem Statement, Solution Strategy and ER Diagram](#chapter-1-problem-statement-solution-strategy-and-er-diagram)
  - [1.1 Problem Statement](#11-problem-statement)
  - [1.2 Objectives](#12-objectives)
  - [1.3 Scope and Assumptions](#13-scope-and-assumptions)
  - [1.4 Proposed Solution Strategy](#14-proposed-solution-strategy)
  - [1.5 Functional Requirements](#15-functional-requirements)
  - [1.6 Entity-Relationship Diagram (ERD)](#16-entity-relationship-diagram-erd)
  - [1.7 Entity and Relationship Summary](#17-entity-and-relationship-summary)
- [Chapter 2: Logical Database Design](#chapter-2-logical-database-design)
  - [2.1 Relational Schema](#21-relational-schema)
  - [2.2 Keys and Integrity Constraints](#22-keys-and-integrity-constraints)
  - [2.3 Functional Dependencies](#23-functional-dependencies)
  - [2.4 Normalization up to Third Normal Form (3NF)](#24-normalization-up-to-third-normal-form-3nf)
  - [2.5 Data Dictionary](#25-data-dictionary)
  - [2.6 Implementation of Logical Design: DDL and Sample Data](#26-implementation-of-logical-design-ddl-and-sample-data)
- [Chapter 3: Application Development Using Logical Database Design](#chapter-3-application-development-using-logical-database-design)
  - [3.1 Application Overview](#31-application-overview)
  - [3.2 Development Environment and Database Connectivity](#32-development-environment-and-database-connectivity)
  - [3.3 Application Modules and Database Mapping](#33-application-modules-and-database-mapping)
  - [3.4 CRUD Operations](#34-crud-operations)
  - [3.5 Business Rules, Validation and Error Handling](#35-business-rules-validation-and-error-handling)
  - [3.6 Reports and Database Operations](#36-reports-and-database-operations)
  - [3.7 Application Screens](#37-application-screens)
  - [3.8 Testing and Results](#38-testing-and-results)
- [Chapter 4: Conclusion](#chapter-4-conclusion)
  - [4.1 Limitations and Future Enhancements](#41-limitations-and-future-enhancements)
- [References](#references)
- [Appendices](#appendices)
  - [Appendix A: Complete Database Script](#appendix-a---complete-database-script)
  - [Appendix B: Application Source Code Architecture](#appendix-b---application-source-code-architecture)
  - [Appendix C: Additional Test Data and Outputs](#appendix-c---additional-test-data-and-outputs)

---

## LIST OF TABLES

- **Table 1:** Scope and Assumptions
- **Table 2:** Proposed Solution Strategy
- **Table 3:** Functional Requirements Specification
- **Table 4:** Entity and Relationship Structural Summary
- **Table 5:** Relational Schema Mapping
- **Table 6:** Keys and Referential Integrity Constraints
- **Table 7:** Normalization Status up to 3NF and BCNF
- **Table 8:** Comprehensive Data Dictionary
- **Table 9:** Database Implementation Environment
- **Table 10:** Application Development Environment
- **Table 11:** Application Module-to-Database Mapping
- **Table 12:** Matrix of Implemented CRUD Operations
- **Table 13:** Business Rules, Validation and Error Handling
- **Table 14:** Analytical Reports and SQL Database Operations
- **Table 15:** System Test Cases and Execution Results

---

## LIST OF FIGURES

- **Figure 1:** Entity-Relationship (ER) Diagram of AttendEase
- **Figure 2:** Role-Aware Sign-In Portal with Instant Autofill Controls
- **Figure 3:** Interactive Administrator Analytics Dashboard
- **Figure 4:** Faculty Attendance Marking Matrix with Live Counters
- **Figure 5:** Student Attendance Portal & Shortage Warning Notification
- **Figure 6:** SQL Analytical Reporting Hub with 1-Click CSV Export

---

## LIST OF ACRONYMS

| Acronym | Expansion |
| :--- | :--- |
| **1NF** | First Normal Form |
| **2NF** | Second Normal Form |
| **3NF** | Third Normal Form |
| **ACID** | Atomicity, Consistency, Isolation, Durability |
| **API** | Application Programming Interface |
| **BCNF** | Boyce-Codd Normal Form |
| **CRUD** | Create, Read, Update, Delete |
| **CSV** | Comma-Separated Values |
| **DBMS** | Database Management System |
| **DDL** | Data Definition Language |
| **DML** | Data Manipulation Language |
| **ERD** | Entity-Relationship Diagram |
| **FD** | Functional Dependency |
| **FK** | Foreign Key |
| **HOD** | Head of Department |
| **HTTP** | Hypertext Transfer Protocol |
| **IDE** | Integrated Development Environment |
| **KPI** | Key Performance Indicator |
| **PK** | Primary Key |
| **RBAC** | Role-Based Access Control |
| **SQL** | Structured Query Language |
| **UI** | User Interface |
| **UQ** | Unique Constraint |
| **UX** | User Experience |
| **VIEW** | Virtual Table Derived from SQL Query |

---

## ABSTRACT

Traditional student attendance tracking and leave management in tertiary academic institutions frequently rely on paper registers or disconnected spreadsheets, resulting in data redundancy, unauthorized manual alterations, proxy attendance, and delayed detection of mandatory attendance shortages. This project presents AttendEase, a robust, full-stack database-driven management system designed to automate attendance recording, enforce leave approval auditability, and provide analytical compliance reporting. The system incorporates a normalized relational database targeting Third Normal Form (3NF) comprising sixteen interrelated tables and two SQL views implemented on MySQL Server 8.0. A modular Python Flask web application connects to the database via connection pooling and parameterized execution, implementing strict role-based access control for Administrators, Faculty, and Students. The system provides atomic three-state attendance marking (Present, Absent, Leave), automatic evaluation of the statutory seventy-five percent attendance shortage threshold, transactional leave approval workflows with document attachment support, makeup session tracking, and eight specialized SQL analytical reports exportable to CSV. Automated testing validates password hashing, foreign key referential integrity, and business logic, confirming that AttendEase delivers a dependable, scalable, and audit-compliant solution for college administration.

**Keywords:** Relational Database, Entity-Relationship Diagram, Database Normalization (3NF), SQL Analytical Reports, Python Flask, Student Attendance Management.

---

# CHAPTER 1
# PROBLEM STATEMENT, SOLUTION STRATEGY AND ER DIAGRAM

### 1.1 Problem Statement
In modern collegiate and university environments, tracking student lecture attendance and managing leave approvals are critical administrative functions directly governing examination eligibility, student accreditation, and academic discipline [1]. However, the vast majority of academic departments continue to employ conventional paper registers, standalone spreadsheets, or isolated web forms. These manual and decentralized workflows exhibit profound systemic deficiencies: lecture attendance is vulnerable to manual tampering, human clerical calculation errors, and proxy signatures; approved medical and duty leaves remain disconnected from attendance rosters, penalizing legitimate absences; and calculation of attendance percentages occurs retrospectively at the end of the academic term rather than continuously [2]. Consequently, students falling below the mandatory seventy-five percent institutional attendance threshold are notified only when examination debarment is imminent, precluding remedial action.

Furthermore, academic administrators lack real-time visibility into faculty teaching loads, room utilization, and departmental trends. The absence of a centralized, transactional relational database creates information silos, inconsistent records across departments, and an inability to conduct audit trails for leave decisions. There is an urgent operational requirement for a secure, multi-tier database management system that unifies course allocations, student enrollments, lecture sessions, granular attendance marking, audited leave approvals, and makeup sessions under a standardized relational model [3].

### 1.2 Objectives
To address the identified limitations, the specific, measurable objectives of this Project-Based Learning activity are to:
1. **Design** a normalized relational database schema targeting Third Normal Form (3NF) that completely models departments, users, faculty, students, courses, sections, enrollments, class sessions, attendance, leaves, makeup sessions, alerts, and audit logs.
2. **Implement** robust entity, domain, and referential integrity constraints using primary keys, foreign keys, unique constraints, and check constraints to guarantee database consistency under concurrent operations.
3. **Develop** a secure, modular Python Flask backend utilizing connection pooling, parameterized SQL queries, and role-based access control (RBAC) enforcing distinct privilege boundaries for Students, Faculty, and Administrators.
4. **Automate** transactional attendance recording with verified status choices (Present, Absent, Leave) and dynamic threshold evaluation generating automated shortage alerts for students with attendance below 75%.
5. **Implement** an audited multi-tier leave application workflow featuring document attachments and atomic review decisions linked with attendance histories.
6. **Construct** eight complex analytical SQL reports demonstrating multi-table JOINs, aggregations (`COUNT`, `SUM`, `AVG`), `GROUP BY`, `HAVING`, nested subqueries, reusable SQL `VIEW`s, and streaming CSV export capabilities.

### 1.3 Scope and Assumptions

#### Table 1. Scope and Assumptions
| Item | Description |
| :--- | :--- |
| **In Scope** | Relational database design and implementation on MySQL 8.0; role-based web interface for Administrator, Faculty, and Student; course section creation and faculty allocation; student section enrollment; lecture session scheduling; attendance recording and updating; leave application and review; makeup class management; threshold alert computation; 8 analytical reports with CSV export. |
| **Out of Scope / Exclusions** | Hardware biometric fingerprint/RFID scanning devices; automated SMS/WhatsApp gateway integration; payment gateway for examination condonation fee processing; native mobile application development (mobile responsiveness is supported through responsive web CSS). |
| **Assumptions** | 1. Each academic year is divided into distinct terms (e.g., Fall, Spring).<br>2. A minimum attendance threshold of 75.0% is mandated by university regulations.<br>3. Each enrolled student can possess at most one attendance status per class session.<br>4. Approved leaves represent excused absences and are formally audited.<br>5. Instructors are authorized to create class sessions and mark attendance only for their allocated course sections. |

### 1.4 Proposed Solution Strategy

The proposed solution, AttendEase, is conceptualized as a centralized, three-tier database management application. At the persistence tier, MySQL Server 8.0 manages data storage, constraint enforcement, and query execution. At the application tier, Python with Flask coordinates business logic, session security, and database connection pooling. At the presentation tier, a clean, professional web dashboard built with HTML5, CSS3, JavaScript, and Chart.js delivers intuitive role-specific interfaces [4].

#### Table 2. Proposed Solution Strategy
| Solution Element | Project-Specific Description |
| :--- | :--- |
| **Primary Users / Roles** | **Administrator (HOD/Dean):** Full college administration, master catalogs, institutional reports.<br>**Faculty:** Section teaching roster, lecture creation, attendance marking, leave reviews.<br>**Student:** Attendance tracking, course breakdown, leave submission, shortage alerts. |
| **Major Application Modules** | 1. Authentication & Session Module (RBAC, password hashing)<br>2. Student & Faculty Management Module<br>3. Course, Section & Enrollment Management Module<br>4. Class Attendance Marking & Correction Module<br>5. Leave Application & Approval Audit Module<br>6. Makeup Class Scheduling & Participation Module<br>7. Shortage Alert & Notification Module<br>8. SQL Reporting & Analytics Hub |
| **Proposed Workflow** | Admin assigns faculty to course sections and enrolls students &rarr; Faculty creates lecture session &rarr; Faculty marks student attendance (Present/Absent/Leave) &rarr; Database automatically updates student percentage and evaluates 75% shortage threshold &rarr; Students below 75% receive alert banners &rarr; Students submit leave applications &rarr; Faculty reviews and approves/rejects with audit notes &rarr; Admin generates institution-wide reports. |
| **Important Business Rules** | 1. Unique enrollment: A student can enroll in a section only once.<br>2. Unique attendance: Exactly one attendance record per student per lecture session.<br>3. Strict RBAC: Faculty cannot record attendance for sections assigned to other instructors.<br>4. Date validation: Leave end date must be greater than or equal to start date.<br>5. Transaction safety: Multi-table state changes execute within atomic database transactions with rollback on failure. |
| **Expected Reports / Outputs** | 1. Student-wise Attendance Percentage<br>2. Course-wise Attendance Summary<br>3. Shortage List (< 75% Threshold)<br>4. Leave Application History & Audit<br>5. Pending Leave Applications<br>6. Faculty Allocation Matrix<br>7. Makeup Class Participation<br>8. Monthly Attendance Trends |

### 1.5 Functional Requirements

#### Table 3. Functional Requirements
| Req. ID | Functional Requirement | Description | Remarks / Priority |
| :--- | :--- | :--- | :--- |
| **FR-01** | Secure Role-Based Authentication | Enforce secure login via username/email and hashed passwords; establish session privileges for Admin, Faculty, and Student. | High |
| **FR-02** | Academic Master Catalog Management | Enable Admin to perform CRUD operations on departments, courses, faculty, students, and sections. | High |
| **FR-03** | Section Allocation and Student Enrollment | Permit allocation of faculty to sections and enrollment of students up to classroom capacity limit. | High |
| **FR-04** | Class Session Creation & Attendance Marking | Allow instructors to schedule lectures and record three-state attendance (Present, Absent, Leave) with remarks. | High |
| **FR-05** | Dynamic Attendance Percentage Calculation | Compute attendance strictly as `(Present / Total Counted) * 100` in real time via database views and queries. | High |
| **FR-06** | Automated Attendance Shortage Detection | Detect students dropping below the 75% threshold and record active alerts without duplicates. | High |
| **FR-07** | Leave Application & Audit Approval Workflow | Enable students to apply for leave with optional proof documents; enable faculty to approve/reject with notes. | High |
| **FR-08** | Makeup Class Scheduling & Participation | Allow faculty to conduct remedial sessions and record student makeup attendance. | Medium |
| **FR-09** | SQL Analytical Reporting & CSV Data Export | Generate 8 complex analytical reports with multi-criteria filtering and streaming CSV export. | High |
| **FR-10** | System Audit Logging & Traceability | Record critical database modifications, timestamps, entity IDs, and client IP addresses in `audit_logs`. | Medium |

### 1.6 Entity-Relationship Diagram (ERD)

Figure 1 illustrates the conceptual Entity-Relationship Diagram of AttendEase. The model represents the academic structure beginning with departments offering courses and employing faculty members. Sections are created for courses and assigned to faculty, with students enrolled through the enrollments relationship. Faculty conduct class sessions, for which individual attendance entries are marked. Students submit leave applications reviewed by faculty, and attend makeup sessions. Attendance alerts and audit logs maintain compliance and system integrity [5].

```
+---------------------------------------------------------------------------------------------------------+
|                                     ENTITY-RELATIONSHIP ARCHITECTURE                                    |
+---------------------------------------------------------------------------------------------------------+
 [departments] 1 -----< M [faculty] 1 -----< M [sections] M >----- 1 [courses]                            
       |                        |                    |                     |                              
       | 1                      | 1                  | 1                   | 1                            
       |                        |                    |                     |                              
       v M                      v M                  v M                   v M                            
  [students] <============= [users]          [class_sessions] 1 ---< M [attendance] >--- 1 [students]     
       |                                             |                                       |            
       | 1                                           | 0..1                                  | 1          
       v M                                           v 1                                     v M          
 [enrollments] >----------------------------- [sections]                              [leave_applications]
       ^                                             |                                       | 1          
       |                                             | 1                                     v 1          
 [attendance_alerts]                                 v M                              [leave_approvals]   
                                              [makeup_sessions] 1 ---< M [makeup_attendance]              
+---------------------------------------------------------------------------------------------------------+
```
*Figure 1. Entity-Relationship Diagram of the Proposed System*

### 1.7 Entity and Relationship Summary

#### Table 4. Entity and Relationship Summary
| Entity / Relationship | Major Attributes / Cardinality | Purpose / Business Rule |
| :--- | :--- | :--- |
| **departments** | `dept_id` (PK), `dept_code`, `dept_name` | 1:N with students, faculty, and courses; organizes college academic structure. |
| **users** | `user_id` (PK), `username`, `email`, `password_hash`, `role` | 1:1 with students and faculty; provides unified credential store and RBAC. |
| **students** | `student_id` (PK), `user_id` (FK), `roll_number`, `full_name`, `email`, `dept_id` (FK) | M:N with sections through enrollments; child of users and departments. |
| **faculty** | `faculty_id` (PK), `user_id` (FK), `employee_id`, `full_name`, `dept_id` (FK) | 1:N with sections and class_sessions; child of users and departments. |
| **courses** | `course_id` (PK), `course_code`, `course_title`, `credits`, `dept_id` (FK) | 1:N with sections; represents master syllabus units. |
| **sections** | `section_id` (PK), `course_id` (FK), `faculty_id` (FK), `section_name`, `classroom` | M:N link between courses, faculty, and students; host of class sessions. |
| **enrollments** | `enrollment_id` (PK), `student_id` (FK), `section_id` (FK), `status` | Associative entity linking students to sections with unique enrollment rule. |
| **class_sessions** | `session_id` (PK), `section_id` (FK), `faculty_id` (FK), `session_date`, `times` | 1:N with attendance; represents individual lecture occurrences. |
| **attendance** | `attendance_id` (PK), `session_id` (FK), `student_id` (FK), `status`, `marked_by` | Granular record of student status (present/absent/leave) for a lecture. |
| **leave_types** | `leave_type_id` (PK), `type_name`, `max_days_per_term` | 1:N with leave_applications; categorizes approved absence limits. |
| **leave_applications** | `application_id` (PK), `student_id` (FK), `leave_type_id` (FK), `dates`, `reason` | 1:1 with leave_approvals; captures student absence requests. |
| **leave_approvals** | `approval_id` (PK), `application_id` (FK), `reviewed_by` (FK), `decision` | Audit trail of faculty decisions on submitted leave requests. |
| **makeup_sessions** | `makeup_id` (PK), `section_id` (FK), `faculty_id` (FK), `session_date`, `topic` | 1:N with makeup_attendance; remedial lecture scheduling. |
| **makeup_attendance** | `makeup_att_id` (PK), `makeup_id` (FK), `student_id` (FK), `status` | Associative entity tracking student participation in makeup classes. |
| **attendance_alerts** | `alert_id` (PK), `student_id` (FK), `section_id` (FK), `current_percentage` | Active shortage tracker for students below the 75% threshold. |
| **audit_logs** | `log_id` (PK), `user_id` (FK), `action`, `entity_type`, `details`, `ip_address` | System security log capturing data manipulation events. |

---

# CHAPTER 2
# LOGICAL DATABASE DESIGN

### 2.1 Relational Schema

The conceptual ER diagram was transformed into a normalized relational schema according to standard relational mapping principles. Primary keys are underlined and foreign keys are designated with an asterisk (`*`). All many-to-many relationships are decomposed into associative relations with foreign key constraints [6].

#### Table 5. Relational Schema
| S.No. | Table / View Name | Attributes (PK underlined, FK*) | Purpose |
| :--- | :--- | :--- | :--- |
| 1 | **system_settings** | `setting_id` (PK), `setting_key`, `setting_value`, `description`, `updated_at` | System configuration parameters |
| 2 | **departments** | `dept_id` (PK), `dept_code`, `dept_name`, `created_at` | Academic branches |
| 3 | **users** | `user_id` (PK), `username`, `email`, `password_hash`, `role`, `is_active`, `created_at` | Authentication base and credentials |
| 4 | **students** | `student_id` (PK), `user_id`* (FK), `roll_number`, `full_name`, `email`, `dept_id`* (FK), `program`, `current_semester`, `phone`, `is_active` | Student identity records |
| 5 | **faculty** | `faculty_id` (PK), `user_id`* (FK), `employee_id`, `full_name`, `email`, `dept_id`* (FK), `designation`, `phone`, `is_active` | Teaching personnel profiles |
| 6 | **courses** | `course_id` (PK), `course_code`, `course_title`, `credits`, `dept_id`* (FK), `is_active` | Academic course catalog |
| 7 | **sections** | `section_id` (PK), `course_id`* (FK), `faculty_id`* (FK), `section_name`, `academic_term`, `academic_year`, `classroom`, `max_capacity` | Section allocations |
| 8 | **enrollments** | `enrollment_id` (PK), `student_id`* (FK), `section_id`* (FK), `enrolled_at`, `status` | Student section enrollments |
| 9 | **class_sessions** | `session_id` (PK), `section_id`* (FK), `faculty_id`* (FK), `session_date`, `start_time`, `end_time`, `topic`, `session_type` | Conducted lectures |
| 10 | **attendance** | `attendance_id` (PK), `session_id`* (FK), `student_id`* (FK), `status`, `remarks`, `marked_at`, `marked_by`* (FK) | Lecture attendance entries |
| 11 | **leave_types** | `leave_type_id` (PK), `type_name`, `max_days_per_term`, `description`, `is_active` | Categories of permitted leaves |
| 12 | **leave_applications** | `application_id` (PK), `student_id`* (FK), `leave_type_id`* (FK), `start_date`, `end_date`, `total_days`, `reason`, `status` | Student absence requests |
| 13 | **leave_approvals** | `approval_id` (PK), `application_id`* (FK), `reviewed_by`* (FK), `decision`, `decision_notes`, `reviewed_at` | Decision audit trail |
| 14 | **makeup_sessions** | `makeup_id` (PK), `section_id`* (FK), `original_session_id`* (FK), `faculty_id`* (FK), `session_date`, `times`, `topic`, `status` | Makeup session roster |
| 15 | **makeup_attendance** | `makeup_att_id` (PK), `makeup_id`* (FK), `student_id`* (FK), `status`, `marked_at`, `marked_by`* (FK) | Makeup class attendance |
| 16 | **attendance_alerts** | `alert_id` (PK), `student_id`* (FK), `section_id`* (FK), `current_percentage`, `threshold_percentage`, `attended`, `missed`, `status` | Shortage tracking warnings |
| 17 | **audit_logs** | `log_id` (PK), `user_id`* (FK), `action`, `entity_type`, `entity_id`, `details`, `ip_address`, `created_at` | Administrative audit trail |
| 18 | **v_student_course_attendance** | VIEW on `enrollments`, `students`, `sections`, `courses`, `class_sessions`, `attendance` | Aggregated student % view |
| 19 | **v_section_summary** | VIEW on `sections`, `courses`, `faculty`, `enrollments`, `class_sessions` | Section overview summary view |

### 2.2 Keys and Integrity Constraints

#### Table 6. Keys and Integrity Constraints
| Table Name | Key / Constraint Type | Attribute(s) & Referential Actions | Business Rule Enforced |
| :--- | :--- | :--- | :--- |
| **users** | Primary Key<br>Unique Key<br>Check Constraint<br>Not Null | `user_id`<br>`username`, `email`<br>`role IN ('admin', 'faculty', 'student')`<br>`password_hash` | Surrogate identifier; unique user identity; valid role domain; credential presence. |
| **students** | Primary Key<br>Foreign Key<br>Foreign Key<br>Unique Key | `student_id`<br>`user_id` -> `users(user_id)` ON DELETE CASCADE<br>`dept_id` -> `departments(dept_id)` ON DELETE RESTRICT<br>`roll_number`, `email` | Unique student identity; user account linkage; valid department parent; duplicate prevention. |
| **faculty** | Primary Key<br>Foreign Key<br>Foreign Key<br>Unique Key | `faculty_id`<br>`user_id` -> `users(user_id)` ON DELETE CASCADE<br>`dept_id` -> `departments(dept_id)` ON DELETE RESTRICT<br>`employee_id`, `email` | Unique faculty identity; user account linkage; valid department parent; duplicate prevention. |
| **sections** | Primary Key<br>Foreign Key<br>Foreign Key<br>Unique Key | `section_id`<br>`course_id` -> `courses(course_id)`<br>`faculty_id` -> `faculty(faculty_id)`<br>`(course_id, section_name, academic_term, academic_year)` | Section identifier; valid course parent; valid instructor parent; prevent duplicate section batches. |
| **enrollments** | Primary Key<br>Foreign Key<br>Foreign Key<br>Unique Key | `enrollment_id`<br>`student_id` -> `students(student_id)` ON DELETE CASCADE<br>`section_id` -> `sections(section_id)` ON DELETE CASCADE<br>`(student_id, section_id)` | Enrollment identifier; student parent; section parent; enforce single active enrollment per student per section. |
| **attendance** | Primary Key<br>Foreign Key<br>Foreign Key<br>Unique Key<br>Domain Check | `attendance_id`<br>`session_id` -> `class_sessions(session_id)` ON DELETE CASCADE<br>`student_id` -> `students(student_id)` ON DELETE CASCADE<br>`(session_id, student_id)`<br>`status IN ('present', 'absent', 'leave')` | Attendance entry; parent session; parent student; enforce exactly one attendance mark per lecture session. |
| **leave_applications** | Primary Key<br>Foreign Key<br>Foreign Key<br>Check Constraint | `application_id`<br>`student_id` -> `students(student_id)`<br>`leave_type_id` -> `leave_types(leave_type_id)`<br>`end_date >= start_date` | Leave application key; student applicant; valid category; ensure non-inverted calendar date range. |
| **leave_approvals** | Primary Key<br>Foreign Key<br>Foreign Key<br>Domain Check | `approval_id`<br>`application_id` -> `leave_applications(application_id)` ON DELETE CASCADE<br>`reviewed_by` -> `users(user_id)`<br>`decision IN ('approved', 'rejected')` | Approval audit key; target application; reviewer credential; enforce explicit binary decision. |

### 2.3 Functional Dependencies

The fundamental functional dependencies governing the primary relations are listed below:

```sql
1. users: user_id -> username, email, password_hash, role, is_active
   username -> user_id, email, password_hash, role

2. students: student_id -> user_id, roll_number, full_name, email, dept_id, program, current_semester
   roll_number -> student_id, user_id, full_name, email, dept_id

3. faculty: faculty_id -> user_id, employee_id, full_name, email, dept_id, designation

4. courses: course_id -> course_code, course_title, credits, dept_id

5. sections: section_id -> course_id, faculty_id, section_name, academic_term, academic_year, classroom

6. enrollments: enrollment_id -> student_id, section_id, enrolled_at, status

7. class_sessions: session_id -> section_id, faculty_id, session_date, start_time, end_time, topic

8. attendance: attendance_id -> session_id, student_id, status, remarks, marked_at, marked_by
   {session_id, student_id} -> attendance_id, status, remarks, marked_at, marked_by

9. leave_applications: application_id -> student_id, leave_type_id, start_date, end_date, total_days, reason, status
```

### 2.4 Normalization up to Third Normal Form (3NF)

#### Table 7. Normalization Status up to 3NF
| Relation Name | 1NF | 2NF | 3NF | BCNF | Remarks / Decomposition Justification |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **departments** | Yes | Yes | Yes | Yes | All non-key attributes depend strictly on `dept_id`. |
| **users** | Yes | Yes | Yes | Yes | `username` and `email` are candidate keys; no transitive dependencies. |
| **students** | Yes | Yes | Yes | Yes | `dept_id` is a foreign key referencing `departments`; `dept_name` not stored. |
| **faculty** | Yes | Yes | Yes | Yes | `dept_id` is a foreign key; no transitive dependencies. |
| **courses** | Yes | Yes | Yes | Yes | `course_code` is candidate key; credits depends directly on `course_id`. |
| **sections** | Yes | Yes | Yes | Yes | Foreign keys `course_id` and `faculty_id` prevent embedding course/faculty details. |
| **enrollments** | Yes | Yes | Yes | Yes | Surrogate PK `enrollment_id`; status depends on enrollment instance. |
| **class_sessions** | Yes | Yes | Yes | Yes | All lecture details depend strictly on `session_id`. |
| **attendance** | Yes | Yes | Yes | Yes | Composite candidate key `{session_id, student_id}`; no transitive dependencies. |
| **leave_applications** | Yes | Yes | Yes | Yes | `leave_type_id` foreign key references `leave_types`; no transitive attributes. |
| **leave_approvals** | Yes | Yes | Yes | Yes | `approval_id` surrogate PK; decision and notes depend on approval instance. |
| **makeup_sessions** | Yes | Yes | Yes | Yes | Section and faculty foreign keys prevent transitive dependencies. |

### 2.5 Data Dictionary

#### Table 8. Comprehensive Data Dictionary
| Table | Attribute | Data Type | Key / Constraint | Description |
| :--- | :--- | :--- | :--- | :--- |
| **departments** | `dept_id` | INT | PK, AUTO_INCREMENT | Surrogate primary key for department |
| **departments** | `dept_code` | VARCHAR(20) | UNIQUE, NOT NULL | Unique short code (e.g., 'CSE', 'ECE') |
| **departments** | `dept_name` | VARCHAR(150) | NOT NULL | Full departmental title |
| **users** | `user_id` | INT | PK, AUTO_INCREMENT | Surrogate primary key for user account |
| **users** | `username` | VARCHAR(50) | UNIQUE, NOT NULL | Unique login identifier |
| **users** | `email` | VARCHAR(120) | UNIQUE, NOT NULL | Unique institutional email address |
| **users** | `password_hash` | VARCHAR(255) | NOT NULL | Cryptographic Scrypt password digest |
| **users** | `role` | ENUM | NOT NULL, ('admin', 'faculty', 'student') | System role determining RBAC permissions |
| **students** | `student_id` | INT | PK, AUTO_INCREMENT | Surrogate primary key for student |
| **students** | `roll_number` | VARCHAR(50) | UNIQUE, NOT NULL | Unique institutional student roll number |
| **students** | `full_name` | VARCHAR(120) | NOT NULL | Full legal name of the student |
| **faculty** | `faculty_id` | INT | PK, AUTO_INCREMENT | Surrogate primary key for faculty member |
| **faculty** | `employee_id` | VARCHAR(50) | UNIQUE, NOT NULL | Institutional employee identifier |
| **courses** | `course_id` | INT | PK, AUTO_INCREMENT | Surrogate primary key for course |
| **courses** | `course_code` | VARCHAR(30) | UNIQUE, NOT NULL | Unique course catalogue code (e.g., 'CS301') |
| **sections** | `section_id` | INT | PK, AUTO_INCREMENT | Surrogate primary key for section batch |
| **sections** | `section_name` | VARCHAR(50) | NOT NULL | Section batch label (e.g., 'CS301-A') |
| **enrollments** | `enrollment_id` | INT | PK, AUTO_INCREMENT | Surrogate primary key for enrollment |
| **class_sessions** | `session_id` | INT | PK, AUTO_INCREMENT | Surrogate primary key for class lecture |
| **attendance** | `attendance_id` | INT | PK, AUTO_INCREMENT | Surrogate primary key for attendance mark |
| **attendance** | `status` | ENUM | NOT NULL, ('present', 'absent', 'leave') | Recorded verified attendance state |
| **leave_applications** | `application_id` | INT | PK, AUTO_INCREMENT | Surrogate primary key for leave request |
| **leave_approvals** | `approval_id` | INT | PK, AUTO_INCREMENT | Surrogate primary key for leave decision |
| **attendance_alerts** | `alert_id` | INT | PK, AUTO_INCREMENT | Surrogate primary key for shortage alert |
| **audit_logs** | `log_id` | INT | PK, AUTO_INCREMENT | Surrogate primary key for security log |

### 2.6 Implementation of Logical Design: DDL and Sample Data

#### Table 9. Database Implementation Environment
| Environment Metric | Technical Specification |
| :--- | :--- |
| **Database Management System** | MySQL Community Server (GPL) |
| **DBMS Engine & Version** | InnoDB Storage Engine, Version 8.0.46 for Win64 |
| **Character Set & Collation** | `utf8mb4`, `utf8mb4_unicode_ci` |
| **Total Number of Tables** | 17 physical tables (including `system_settings`) |
| **Total Number of SQL Views** | 2 reusable reporting views (`v_student_course_attendance`, `v_section_summary`) |
| **Database Connection Driver** | `mysql-connector-python` (v26.7.0 C-extension pooling) |
| **Sample Seed Data Population** | 32 attendance records, 12 sessions, 11 enrollments, 10 users, 6 students, 3 faculty, 4 courses |

---

# CHAPTER 3
# APPLICATION DEVELOPMENT USING LOGICAL DATABASE DESIGN

### 3.1 Application Overview
AttendEase is implemented as a modular, three-tier Python Flask application that dynamically queries and manipulates the underlying MySQL relational database. The application enforces server-side Role-Based Access Control (RBAC), parameterizes every database transaction to prevent SQL injection vulnerabilities, and uses atomic commits and rollbacks to guarantee ACID properties. Through interactive dashboards, real-time Chart.js visual analytics, and live attendance calculation engines, the application directly manifests the logical database design in concrete academic workflows [8].

### 3.2 Development Environment and Database Connectivity

#### Table 10. Application Development Environment
| Development Item | Specification / Tool Utilized |
| :--- | :--- |
| **Programming Language** | Python 3.14.3 (64-bit) |
| **Backend Framework** | Flask 3.1.3 (WSGI Web Application Framework) |
| **Database Management System** | MySQL Server 8.0 (Community Edition) |
| **Database Connector Driver** | `mysql-connector-python` 26.7.0 (with C-Extension pooling) |
| **Security & Hashing** | Werkzeug 3.1.9 (Scrypt cryptographic password digests) |
| **Frontend Technologies** | HTML5 Semantic Markup, Vanilla CSS3 Design System, JavaScript (ES6+), Chart.js 4.4.1 |
| **Integrated Development Environment** | Visual Studio Code with Python & MySQL Extensions |
| **Operating Environment** | Microsoft Windows 11 (x64) |
| **Repository & Workspace** | `C:\Users\ATHARVA SINGH\Desktop\DBMS_PBL` |

### 3.3 Application Modules and Database Mapping

#### Table 11. Application Module-to-Database Mapping
| Module Name | Primary Purpose | Underlying Tables Used | Main SQL Operations |
| :--- | :--- | :--- | :--- |
| **Authentication (`routes/auth.py`)** | Authenticates credentials; establishes session `user_id` and role; controls password changes. | `users`, `students`, `faculty`, `audit_logs` | `SELECT`, `UPDATE`, `INSERT` |
| **Dashboard (`routes/dashboard.py`)** | Generates role-tailored KPIs, trend graphs, and recent activity streams. | `users`, `students`, `faculty`, `sections`, `attendance`, `attendance_alerts`, `audit_logs` | `SELECT` with `COUNT`, `SUM`, `AVG`, `GROUP BY` |
| **Student Management (`routes/students.py`)** | Manages student catalog; performs multi-criteria searches; toggles account active states. | `students`, `users`, `departments`, `audit_logs` | `INSERT` (atomic 2-table), `SELECT`, `UPDATE` |
| **Faculty Management (`routes/faculty.py`)** | Maintains teaching roster, academic ranks, and departmental affiliations. | `faculty`, `users`, `departments`, `sections`, `audit_logs` | `INSERT`, `SELECT`, `UPDATE` |
| **Course & Sections (`routes/courses.py`)** | Configures courses, sections, room allocations, and student enrollments. | `courses`, `sections`, `enrollments`, `students`, `faculty` | `INSERT`, `SELECT`, `UPDATE` with capacity check |
| **Attendance Hub (`routes/attendance.py`)** | Creates class sessions; records/updates granular attendance; computes shortage warnings. | `class_sessions`, `attendance`, `enrollments`, `attendance_alerts` | `INSERT`, `SELECT`, `ON DUPLICATE KEY UPDATE` |
| **Leave Workflow (`routes/leaves.py`)** | Submits student leaves with attachments; executes atomic approvals with review notes. | `leave_applications`, `leave_types`, `leave_approvals`, `students` | `INSERT`, `SELECT`, `UPDATE` with Transaction |
| **Makeup Classes (`routes/makeup.py`)** | Schedules remedial lectures; records student makeup participation. | `makeup_sessions`, `makeup_attendance`, `enrollments` | `INSERT`, `SELECT`, `UPDATE` with Transaction |
| **SQL Reports (`routes/reports.py`)** | Executes 8 complex analytical queries; filters by criteria; streams CSV exports. | `v_student_course_attendance`, `v_section_summary`, all base tables | `SELECT` with `JOIN`, `GROUP BY`, `HAVING`, subqueries |

### 3.4 CRUD Operations

#### Table 12. CRUD Operations
| CRUD Operation | Application Feature / Screen | Table(s) Affected | Implementation Evidence |
| :--- | :--- | :--- | :--- |
| **Create (C)** | 1. Add Student / Faculty account (`routes/students.py`, `routes/faculty.py`)<br>2. Create Class Session (`routes/attendance.py`)<br>3. Submit Leave Application (`routes/leaves.py`)<br>4. Schedule Makeup Class (`routes/makeup.py`) | `users`, `students`, `faculty`, `class_sessions`, `leave_applications`, `makeup_sessions` | `INSERT INTO users ...; INSERT INTO students ...` executed within atomic database transaction. |
| **Read / Search (R)** | 1. Dynamic Dashboard KPI metrics & monthly trends<br>2. Filter students by department and search by roll number<br>3. View enrolled courses and individual percentage in student portal<br>4. 8 Analytical SQL Reports | All 16 tables, `v_student_course_attendance`, `v_section_summary` | `SELECT` with multi-table `INNER`/`LEFT JOIN`s, pattern matching (`LIKE %s`), `GROUP BY`, `HAVING`. |
| **Update (U)** | 1. Edit Student / Faculty profiles<br>2. Modify Class Attendance marks<br>3. Review & Approve/Reject Leave Application<br>4. Resolve Shortage Alerts | `students`, `faculty`, `attendance`, `leave_applications`, `leave_approvals`, `attendance_alerts` | `UPDATE attendance ... ON DUPLICATE KEY UPDATE; UPDATE leave_applications SET status = %s;` |
| **Delete / Controlled Removal (D)** | 1. Drop student from section enrollment<br>2. Deactivate student or faculty account<br>3. Soft removal via status toggles (`is_active = FALSE`) | `enrollments`, `students`, `users` | `UPDATE enrollments SET status = 'dropped' WHERE ...; UPDATE users SET is_active = FALSE WHERE ...;` |

### 3.5 Business Rules, Validation and Error Handling

#### Table 13. Business Rules, Validation and Error Handling
| Business Rule / Validation | Implementation Mechanism | Observed Outcome / Protection |
| :--- | :--- | :--- |
| **SQL Injection Prevention** | All database access uses parameterized placeholders (`%s`) exclusively via `mysql-connector-python`. No string formatting or SQL concatenation is permitted. | Zero SQL injection vulnerability across all 25+ application endpoints. |
| **Single Attendance Entry Rule** | Enforced at database level via `UNIQUE KEY uq_session_student (session_id, student_id)` and handled in Python via `ON DUPLICATE KEY UPDATE`. | Prevents accidental or malicious double-recording of attendance for the same student in a lecture. |
| **Leave Calendar Range Validation** | Enforced via Python datetime validation and MySQL `CHECK (end_date >= start_date)`. Total days calculated strictly as `(end - start).days + 1`. | Rejects inverted date ranges with informative flash alert: *"End date cannot be earlier than start date"*. |
| **Attendance Shortage Detection (< 75%)** | Automatically triggered after attendance recording in `update_attendance_alerts_for_section()`. Evaluates percentage against configured 75% threshold. | Inserts active alert in `attendance_alerts` and displays prominent red alert banner on student dashboard. |
| **Role-Based Access Control (RBAC)** | Enforced via Python decorators `@login_required` and `@role_required(['admin', 'faculty'])`. Unauthorized route access is intercepted and redirected. | Students attempting to access `/faculty` or `/students` are blocked and redirected with *"Access Denied"*. |
| **Atomic Multi-Table Transactions** | Coordinated multi-table operations (such as creating user + student, or updating leave application + inserting approval audit) execute via `execute_transaction()`. | Automatic `conn.rollback()` on exception prevents orphaned records in the database. |

### 3.6 Reports and Database Operations

#### Table 14. Reports and Database Operations
| Report Title | SQL / Database Concept Utilized | Generated Application Output |
| :--- | :--- | :--- |
| **Report 1: Student-wise Attendance Percentage** | Queries reusable SQL VIEW `v_student_course_attendance`, performing joins across `enrollments`, `students`, `courses`, `sections`, and `attendance`. | Tabular roster of student roll number, course code, attended classes, leaves, and computed attendance percentage. |
| **Report 2: Course-wise Attendance Summary** | Performs `INNER JOIN courses, departments` and `LEFT JOIN sections, class_sessions, attendance`. Aggregates via `COUNT(DISTINCT)` and `SUM(CASE)`. | Institutional overview showing total sections, sessions conducted, total presents, and average course attendance rate. |
| **Report 3: Attendance Shortage List (< 75%)** | Employs `HAVING` clause: `COUNT(a.attendance_id) >= 2 AND current_pct < 75.0`. Computes shortfall classes needed via `CEIL((75 * total / 100) - attended)`. | Official debarment risk roster showing students below 75%, their current percentage, and exact class shortfall count. |
| **Report 4: Leave Application History & Audit** | Joins `leave_applications`, `students`, `leave_types`, `leave_approvals`, and `users` to present full audit trail of approvals, reviewers, and remarks. | Comprehensive administrative history tracking leave dates, reviewer identities, and faculty decision notes. |
| **Report 5: Pending Leave Queue** | Filters `leave_applications WHERE status = 'pending'` ordered by submission timestamp `applied_at ASC`. | Prioritized faculty inbox of pending student requests awaiting decision. |
| **Report 6: Faculty Course Allocation Matrix** | Joins `faculty`, `departments`, `sections`, and `class_sessions` with subquery calculating student enrollment load. | Faculty teaching workload report displaying allocated sections, distinct courses, and total student counts. |
| **Report 7: Makeup Session Participation** | Aggregates `makeup_sessions`, `sections`, `courses`, and `makeup_attendance` to measure remedial attendance recovery. | Remedial class participation matrix tracking date, room, topic, and attending student counts. |
| **Report 8: Monthly Attendance Trends** | Applies `DATE_FORMAT(cs.session_date, '%Y-%m')` grouping over temporal intervals to measure institutional attendance trajectory. | Chronological monthly analysis displaying sessions held, present marks, and average institutional attendance rate over time. |

### 3.7 Application Screens

The application screens validate the functional implementation of the logical database design across all user workflows:

1. **Figure 2: Role-Aware Sign-In Portal** — Features responsive branding, Scrypt hash verification, pre-filled default credentials, role selector tabs (Admin, Faculty, Student), and 1-click instant login chips for streamlined demonstration.  
   *Figure 2. Role-Aware Sign-In Portal with Instant Autofill Controls*

2. **Figure 3: Interactive Administrator Analytics Dashboard** — Displays real-time KPI metrics derived from SQL COUNT/SUM queries, monthly attendance trends plotted via Chart.js, quick navigation shortcuts, and recent audit activity logs.  
   *Figure 3. Interactive Administrator Analytics Dashboard*

3. **Figure 4: Faculty Attendance Marking Matrix** — Interactive attendance sheet featuring live counters (Present, Absent, Leave), bulk selection buttons ("Mark All Present", "Mark All Absent"), individual status toggle buttons, and optional remarks fields with atomic database submission.  
   *Figure 4. Faculty Attendance Marking Matrix with Live Counters*

4. **Figure 5: Student Attendance Portal & Shortage Warning** — Visual progress bars for each enrolled course, statistical breakdown (Total, Present, Absent, Leave), chronological lecture history log, and prominent red shortage warning banner for students below the 75% threshold.  
   *Figure 5. Student Attendance Portal & Shortage Warning Notification*

5. **Figure 6: SQL Analytical Reporting Hub** — Tabbed navigation across the eight SQL reports, dynamic department and course filter dropdowns, custom threshold controls, and streaming 1-click Export to CSV functionality.  
   *Figure 6. SQL Analytical Reporting Hub with 1-Click CSV Export*

### 3.8 Testing and Results

#### Table 15. System Test Cases and Execution Results
| Test ID | Feature Tested | Input / Simulated Action | Expected Database / System Result | Observed Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-01** | User Authentication | Submit valid credentials (`admin` / `Password@123`) | HTTP 302 redirect to `/dashboard`; establish authenticated session `user_id` | Redirected to dashboard; session established | **Passed** |
| **TC-02** | Invalid Authentication | Submit invalid credentials (`admin` / `WrongPassword`) | Reject authentication; render error message; keep user at `/login` | Error flash displayed: *"Invalid username/email or password"* | **Passed** |
| **TC-03** | RBAC Route Protection | Unauthenticated request to protected route `/students` | HTTP 302 redirect to `/login` with next parameter | Redirected to `/login?next=%2Fstudents` | **Passed** |
| **TC-04** | Role Authorization Privilege | Authenticated Student attempts to access `/faculty` or `/students/add` | Intercept unauthorized action; redirect to `/dashboard` with danger flash | Redirected to dashboard with *"Access denied: Permission required"* | **Passed** |
| **TC-05** | Attendance % Formula | Student with 4 present and 4 absent classes out of 8 total | Calculate strictly as `(4 / 8) * 100 = 50.0%` | Exact percentage computed: 50.00% | **Passed** |
| **TC-06** | Shortage Alert Detection | Student attendance drops to 50.0% (< 75.0% threshold) | Trigger active shortage alert record in `attendance_alerts` table | Active alert created in `attendance_alerts`; banner shown | **Passed** |
| **TC-07** | Shortage Recovery | Student attendance reaches 75.0% (6 present / 8 total) | Evaluate percentage >= 75.0; update alert status to 'resolved' | Alert status updated to 'resolved' in database | **Passed** |
| **TC-08** | Leave Date Validation | Submit leave with `start_date='2026-10-15'` and `end_date='2026-10-12'` | Reject input; trigger date range validation error; prevent database write | Validation triggered: *"End date cannot be earlier than start date"* | **Passed** |
| **TC-09** | Duplicate Attendance Block | Attempt duplicate attendance insertion for same (`session_id`, `student_id`) | Enforce `uq_session_student` unique constraint; execute `ON DUPLICATE KEY UPDATE` | Existing record updated; zero duplicate rows inserted | **Passed** |
| **TC-10** | CSV Report Data Streaming | Request `/reports?report=student_wise&export=csv` | Stream formatted `text/csv` HTTP response with `Content-Disposition` header | HTTP 200 OK; valid CSV stream received with headers and rows | **Passed** |

**Summary of Testing Observations:** All ten test cases completed successfully with zero failures. The test execution confirms that AttendEase strictly enforces all relational integrity constraints, adheres to role-based access control boundaries, calculates statutory attendance percentages accurately, and reliably logs administrative actions.

---

# CHAPTER 4
# CONCLUSION

The AttendEase project demonstrates the successful design, normalization, implementation, and empirical testing of a comprehensive Student Attendance and Leave Approval Management System. Beginning from an analysis of real-world academic record-keeping deficiencies, the project translated institutional requirements into an approved Entity-Relationship model comprising sixteen normalized relations and two analytical SQL views adhering to Third Normal Form (3NF). The schema was realized on MySQL Server 8.0, fortified with primary and foreign keys, unique constraints, domain check rules, and cascaded referential actions.

The Python Flask web application integrates seamlessly with the database tier through connection pooling and parameterized query execution, ensuring zero exposure to SQL injection vulnerabilities and guaranteeing ACID transactional compliance. Role-based dashboards provide tailored utility for Students, Faculty, and Administrators, featuring three-state attendance recording, automatic seventy-five percent shortage alerts, multi-tier leave approval workflows, makeup session management, and eight analytical SQL reports with CSV streaming. The project demonstrates how fundamental relational database principles directly resolve operational challenges in tertiary education.

### 4.1 Limitations and Future Enhancements
Genuine limitations of the current implementation and proposed future enhancements include:
1. **Biometric and RFID Hardware Integration:** The current application requires faculty to mark attendance via the responsive web interface. Future iterations could interface with IoT biometric fingerprint scanners or RFID smartcard readers placed at classroom doorways to stream automated entrance logs directly into `class_sessions`.
2. **Automated Multi-Channel Notification Dispatch:** While shortage alerts are prominently rendered on the web dashboard, integrating external messaging gateways (such as Twilio SMS, WhatsApp Business API, and automated SMTP email notifications) would alert parents and students immediately upon attendance dropping below 75%.
3. **Automated Examination Debarment Condonation Workflow:** Future versions could incorporate an administrative condonation module allowing students with legitimate approved medical leaves between 65% and 75% to submit condonation petitions with online university fee gateway processing.
4. **Timetable and Academic Calendar Integration:** Linking class sessions with master college timetable scheduling tables would automatically populate recurring weekly class slots, eliminating manual session creation by instructors.

---

# REFERENCES

[1] A. Silberschatz, H. F. Korth, and S. Sudarshan, *Database System Concepts*, 7th ed. New York, NY, USA: McGraw-Hill Education, 2020.  
[2] R. Elmasri and S. B. Navathe, *Fundamentals of Database Systems*, 7th ed. Boston, MA, USA: Pearson, 2017.  
[3] C. J. Date, *An Introduction to Database Systems*, 8th ed. Boston, MA, USA: Addison-Wesley, 2004.  
[4] M. Grinberg, *Flask Web Development: Developing Web Applications with Python*, 2nd ed. Sebastopol, CA, USA: O'Reilly Media, 2018.  
[5] P. P. Chen, "The entity-relationship model—toward a unified view of data," *ACM Transactions on Database Systems (TODS)*, vol. 1, no. 1, pp. 9-36, Mar. 1976, doi: 10.1145/320434.320440.  
[6] E. F. Codd, "A relational model of data for large shared data banks," *Communications of the ACM*, vol. 13, no. 6, pp. 377-387, Jun. 1970, doi: 10.1145/362384.362685.  
[7] Oracle Corporation, *MySQL 8.0 Reference Manual*. Accessed: Oct. 14, 2026. [Online]. Available: https://dev.mysql.com/doc/refman/8.0/en/  
[8] World Wide Web Consortium (W3C), *Web Application Security Guidelines*, W3C Working Group Note, 2024. [Online]. Available: https://www.w3.org/TR/webappsec/  

---

# APPENDICES

### APPENDIX A - COMPLETE DATABASE SCRIPT
The complete Data Definition Language (`schema.sql`) and sample data seeding script (`seed.sql`) are stored in the project repository. The script creates the database `attendease_db`, all 16 normalized tables, 2 SQL views, foreign key constraints, indexes, and demo records.

- **DDL Script:** `C:\Users\ATHARVA SINGH\Desktop\DBMS_PBL\schema.sql` (18 KB, 16 tables, 2 views, checks, indexes)
- **DML Seed Script:** `C:\Users\ATHARVA SINGH\Desktop\DBMS_PBL\seed.sql` (12 KB, 32 attendance entries, 12 sessions, 10 users)

### APPENDIX B - APPLICATION SOURCE CODE ARCHITECTURE
The complete application codebase is organized modularly as follows:

```
C:\Users\ATHARVA SINGH\Desktop\DBMS_PBL\
├── app.py                      # Flask Application Factory & Jinja Filters
├── config.py                   # Central Configuration & Environment Parsing
├── init_db.py                  # Automated Database Setup & Seeding Script
├── test_attendease.py          # Automated Test Suite (10 Test Cases)
├── run.bat                     # Windows Server Launcher
├── database/
│   └── connection.py           # MySQL Connection Pool & Transaction Execution
├── routes/
│   ├── auth.py                 # RBAC Login, Logout & Profile Routing
│   ├── dashboard.py            # Role-Tailored Dashboards (Admin, Faculty, Student)
│   ├── students.py             # Student CRUD & Directory Management
│   ├── faculty.py              # Faculty Roster & Teaching Allocations
│   ├── courses.py              # Courses, Sections & Student Enrollments
│   ├── attendance.py           # Class Sessions & Attendance Marking Sheet
│   ├── leaves.py               # Leave Applications & Audited Faculty Approvals
│   ├── makeup.py               # Remedial Class Scheduling & Attendance
│   └── reports.py              # 8 Analytical SQL Reports with CSV Export
├── templates/                  # 14 Responsive Jinja2 HTML Templates
└── static/                     # CSS Design System & Chart.js Application Scripts
```

### APPENDIX C - ADDITIONAL TEST DATA AND OUTPUTS

**Documented Demo Credentials for Project Evaluation:**
- **Administrator:** username `admin`, email `admin@college.edu`, password `Password@123`
- **Faculty Member:** username `prof_alan`, email `alan.turing@college.edu`, password `Password@123`
- **Student (Good Standing):** username `alex_rivera`, email `alex.r@college.edu`, password `Password@123` (100% Attendance)
- **Student (Shortage Case):** username `marcus_vance`, email `marcus.v@college.edu`, password `Password@123` (50.0% Attendance - Active Shortage Alert)
