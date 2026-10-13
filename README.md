# AttendEase — Student Attendance and Leave Approval Management System

> **Smart Attendance. Simple Leave Management.**
> A modern, full-stack college database management application built with **Python Flask**, **MySQL 8.0**, **HTML5/CSS3/JavaScript**, and **Chart.js**.

---

## 1. Project Overview

**AttendEase** is an end-to-end college attendance and leave approval management system designed to enforce academic compliance and eliminate attendance ambiguity. It provides role-based workspaces for:

- **Students:** Real-time attendance percentage tracking, course breakdown, official leave requests with supporting attachments, automated shortage warnings (< 75%), and makeup session schedules.
- **Faculty:** Course section management, class session creation, 3-state attendance marking (`Present`, `Absent`, `Leave`), atomic leave approvals/rejections with audit notes, and makeup class scheduling.
- **College Administrators / HODs:** Institutional statistics, department/course/section master allocation, student enrollment, institution-wide shortage lists, 8 analytical SQL reports with CSV exports, and system audit logs.

---

## 2. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript | Responsive dashboard, modals, real-time counters |
| **Styling** | Custom Design System (CSS3) | Navy & Indigo aesthetic, cards, badges, mobile drawer |
| **Visualizations**| Chart.js (v4.4 via CDN) | Monthly trends, course breakdowns, department distributions |
| **Backend** | Python 3.10+ with Flask (v3.1) | Modular routing (Blueprints), sessions, form validation |
| **Database** | MySQL Server 8.0 | Normalized 3NF relational schema, views, transactions |
| **DB Driver** | `mysql-connector-python` | Connection pooling, parameterized queries, atomic commits |
| **Security** | `Werkzeug` | Scrypt password hashing, session tokens, RBAC decorators |

---

## 3. Database Architecture (Target: 3NF Relational Model)

The database schema (`schema.sql`) implements 16 normalized tables and 2 reusable SQL views:

### Tables
1. `departments`: College branches (dept_id, dept_code, dept_name).
2. `users`: Unified authentication & role base (`admin`, `faculty`, `student`).
3. `students`: Student identity, roll numbers, department, program, semester.
4. `faculty`: Faculty employee records, designation, department affiliations.
5. `courses`: Course master records with credit hours and department keys.
6. `sections`: Course section batches, assigned faculty, classroom, term, capacity.
7. `enrollments`: Student-to-section enrollments with unique constraint (`uq_student_section`).
8. `class_sessions`: Conducted lectures with dates, times, topics, and session types (`regular`, `extra`, `lab`).
9. `attendance`: Verified session attendance (`present`, `absent`, `leave`) with unique constraint (`uq_session_student`).
10. `leave_types`: Leave categories (Medical, Personal, Emergency, Academic/On-Duty) with term day limits.
11. `leave_applications`: Submitted student leave requests with date validation (`end_date >= start_date`) and documents.
12. `leave_approvals`: Audit record of faculty decisions (`approved`, `rejected`) and decision notes.
13. `makeup_sessions`: Supplementary classes linked to sections and original sessions.
14. `makeup_attendance`: Verified student makeup participation (`uq_makeup_student`).
15. `attendance_alerts`: Active/resolved alerts for students dropping below the 75% threshold.
16. `audit_logs`: System audit trail recording actions, timestamps, and IP addresses.
17. `system_settings`: Key-value configuration for attendance threshold and term metadata.

### SQL Views
- `v_student_course_attendance`: Reusable view aggregating total sessions, presents, absents, leaves, and calculated attendance percentage.
- `v_section_summary`: Section performance summary calculating enrolled counts and conducted session counts.

---

## 4. Attendance Calculation & Policy

The official attendance percentage is strictly defined and documented:

$$\text{Attendance Percentage} = \left( \frac{\text{Present Count}}{\text{Total Counted Classes}} \right) \times 100$$

- **Total Counted Classes:** All conducted class sessions marked for the student (`Present + Absent + Leave`).
- **Approved Leave Policy:** Formally approved leaves are designated as `Leave` in the attendance register. They are separated from unexcused absences and factored into faculty condonation reviews.
- **Shortage Threshold:** Configured to **75.0%** by default. Students below 75% automatically trigger active shortage warnings in `attendance_alerts` and display banner notices on their dashboards.
- **Makeup Sessions:** Tracked independently in the makeup register to provide proof of attendance recovery.

---

## 5. Quick Setup & Execution Guide

### Prerequisites
- Python 3.10 or higher
- MySQL Server 8.0 (e.g. Windows Service `MySQL80` running)

### Step 1: Open the Project Directory
```powershell
cd "C:\Users\ATHARVA SINGH\.gemini\antigravity-ide\scratch\attendease"
```

### Step 2: Install Python Dependencies
```powershell
python -m pip install -r requirements.txt
```

### Step 3: Configure Database Credentials in `.env`
Open the `.env` file in the project folder and set your local MySQL root password:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=attendease_db
SECRET_KEY=attendease_dev_secret_key_998877665544332211
ATTENDANCE_THRESHOLD=75.0
```

### Step 4: Initialize the Database (Automatic 1-Click Setup)
Run the initialization script. You can pass your password directly on the command line:
```powershell
python init_db.py --password your_mysql_password
```
*What this script does:*
1. Connects to your local MySQL server.
2. Creates the database `attendease_db` if it doesn't exist.
3. Automatically executes `schema.sql` (creating all 16 tables, constraints, and views).
4. Seeds realistic demo data from `seed.sql`.
5. Verifies all tables and records.
6. Synchronizes credentials with your `.env` file.

### Step 5: Start the Flask Application
```powershell
python app.py
```
The server will start at: **`http://127.0.0.1:5000`**

### Step 6: Open the Application in your Browser
Navigate to **`http://127.0.0.1:5000`** in Google Chrome, Edge, or Firefox.

---

## 6. Documented Demo Logins

All demo accounts use the standard password: **`Password@123`** (You can also click the quick-fill chips on the login screen):

| Role | Username | Email | Description / Test Scenario |
|---|---|---|---|
| **Admin** | `admin` | `admin@college.edu` | Full college administrator, HOD controls, all 8 reports |
| **Faculty** | `prof_alan` | `alan.turing@college.edu` | CSE Professor, teaches CS301 (DBMS) & CS303 |
| **Faculty** | `prof_grace` | `grace.hopper@college.edu` | CSE Associate Professor, teaches CS302 (OS) |
| **Student** | `alex_rivera` | `alex.r@college.edu` | Good attendance record (100% in DBMS) |
| **Student** | `priya_patel` | `priya.p@college.edu` | Has 1 approved medical leave (87.5% attendance) |
| **Student** | `marcus_vance` | `marcus.v@college.edu` | **< 75% Shortage Alert:** 50% attendance (4 present / 4 absent) |

---

## 7. SQL Reports & Analytics Catalog

The **Reports Hub** (`/reports`) includes 8 analytical queries demonstrating SQL best practices (JOINs, GROUP BY, HAVING, Subqueries, and Views):

1. **Student-wise Attendance Percentage:** Detailed student attendance breakdown across courses using `v_student_course_attendance`.
2. **Course-wise Attendance Summary:** Aggregated lecture counts, total enrollments, and college-wide attendance rates per course.
3. **Attendance Shortage Roster (< 75%):** Uses SQL `HAVING current_pct < 75.0` to calculate class shortfall counts for students at risk of exam debarment.
4. **Leave Application History & Audit:** Audit trail of all student leaves, reviewer identity, and faculty decision notes.
5. **Pending Leave Queue:** Pending applications awaiting review.
6. **Faculty Course Allocation Matrix:** Workload analysis calculating assigned sections, distinct courses, and student load.
7. **Makeup Session Participation:** Attendance tracking for remedial classes.
8. **Monthly Attendance Trends:** Aggregation using `DATE_FORMAT(session_date, '%Y-%m')` tracking monthly institutional engagement.

> **CSV Export:** Every report features a 1-click **Export to CSV** button that dynamically generates and streams a formatted `.csv` file.

---

## 8. Automated Testing

Run the included automated test suite anytime:
```powershell
python test_attendease.py
```
Tests pass across 9 core test categories:
- Password hashing & verification
- Attendance percentage formula correctness
- Shortage alert evaluation rules
- Leave date validation (start date $\le$ end date)
- Unauthenticated access redirection
- Role-based authorization constraints (Student vs Admin, Faculty vs Admin)
- Login UI structure
- CSV report streaming response format

---

## 9. Troubleshooting & FAQ

- **Error 1045 (Access denied for user 'root'):**
  Ensure you entered your actual MySQL password in `.env` or ran:
  ```powershell
  python init_db.py --password your_actual_password
  ```
- **Error 2003 (Can't connect to MySQL server):**
  Check that the MySQL Windows service is running:
  ```powershell
  Get-Service -Name '*mysql*'
  # Or start it:
  net start MySQL80
  ```
- **Port 5000 is already in use:**
  Change `PORT=5001` in your `.env` file and restart `python app.py`.

---

**Developed for College Database Management System (DBMS) Project.**
