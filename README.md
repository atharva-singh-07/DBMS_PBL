# AttendEase — Student Attendance & Leave Approval Management System

> **Smart Attendance. Simple Leave Management.**
> A modern, full-stack college database management application built with **Python Flask**, **MySQL 8.0**, **HTML5/CSS3/JavaScript**, and **Chart.js**.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-black?logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?logo=mysql&logoColor=white)
![License](https://img.shields.io/badge/License-Academic-green)
![GitHub](https://img.shields.io/badge/GitHub-atvaholic%2FDBMS__PBL-181717?logo=github)

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

## 3. Database Architecture (3NF Relational Model)

The database schema (`schema.sql`) implements **16 normalized tables** and **2 reusable SQL views**:

### Tables
1. `departments` — College branches (dept_id, dept_code, dept_name).
2. `users` — Unified authentication & role base (`admin`, `faculty`, `student`).
3. `students` — Student identity, roll numbers, department, program, semester.
4. `faculty` — Faculty employee records, designation, department affiliations.
5. `courses` — Course master records with credit hours and department keys.
6. `sections` — Course section batches, assigned faculty, classroom, term, capacity.
7. `enrollments` — Student-to-section enrollments with unique constraint (`uq_student_section`).
8. `class_sessions` — Conducted lectures with dates, times, topics, and session types (`regular`, `extra`, `lab`).
9. `attendance` — Verified session attendance (`present`, `absent`, `leave`) with unique constraint (`uq_session_student`).
10. `leave_types` — Leave categories (Medical, Personal, Emergency, Academic/On-Duty) with term day limits.
11. `leave_applications` — Submitted student leave requests with date validation and document uploads.
12. `leave_approvals` — Audit record of faculty decisions (`approved`, `rejected`) and decision notes.
13. `makeup_sessions` — Supplementary classes linked to sections and original sessions.
14. `makeup_attendance` — Verified student makeup participation (`uq_makeup_student`).
15. `attendance_alerts` — Active/resolved alerts for students dropping below 75% threshold.
16. `audit_logs` — System audit trail recording actions, timestamps, and IP addresses.
17. `system_settings` — Key-value configuration for attendance threshold and term metadata.

### SQL Views
- `v_student_course_attendance` — Aggregates total sessions, presents, absents, leaves, and calculated attendance percentage.
- `v_section_summary` — Section performance summary calculating enrolled counts and conducted session counts.

---

## 4. Attendance Calculation & Policy

$$\text{Attendance \%} = \left( \frac{\text{Present Count}}{\text{Total Counted Classes}} \right) \times 100$$

- **Total Counted Classes:** All conducted sessions marked for the student (`Present + Absent + Leave`).
- **Approved Leave Policy:** Formally approved leaves are designated as `Leave`. They are separated from unexcused absences and factored into faculty condonation reviews.
- **Shortage Threshold:** Configured to **75.0%** by default. Students below 75% automatically trigger active shortage warnings in `attendance_alerts`.
- **Makeup Sessions:** Tracked independently in the makeup register to provide proof of attendance recovery.

---

## 5. Quick Setup & Execution Guide

### Prerequisites
- Python 3.10 or higher
- MySQL Server 8.0 running as a Windows service (`MySQL80`)

### Step 1: Clone the Repository
```powershell
git clone https://github.com/atvaholic/DBMS_PBL.git
cd DBMS_PBL
```

### Step 2: Install Python Dependencies
```powershell
python -m pip install -r requirements.txt
```

### Step 3: Configure Database Credentials
Copy `.env.example` to `.env` and fill in your MySQL credentials:
```powershell
copy .env.example .env
```
Then edit `.env`:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=attendease_db
SECRET_KEY=attendease_dev_secret_key_998877665544332211
ATTENDANCE_THRESHOLD=75.0
```

### Step 4: Initialize the Database (One-Click Setup)
```powershell
python init_db.py --password your_mysql_password
```
This script will:
1. Connect to your local MySQL server
2. Create the database `attendease_db`
3. Execute `schema.sql` (16 tables, constraints, views)
4. Seed realistic demo data from `seed.sql`
5. Verify all tables and records

### Step 5: Start the Application
```powershell
python app.py
```
The server will start at: **`http://127.0.0.1:5000`**

> **Tip:** You can also use the provided batch scripts:
> - `init_db.bat` — Initializes the database
> - `run.bat` — Starts the Flask server

---

## 6. Demo Logins

All demo accounts use the password: **`Password@123`**
(Quick-fill chips are available on the login screen)

| Role | Username | Email | Description |
|---|---|---|---|
| **Admin** | `admin` | `admin@college.edu` | Full college administrator, HOD controls, all 8 reports |
| **Faculty** | `prof_alan` | `alan.turing@college.edu` | CSE Professor — teaches CS301 (DBMS) & CS303 |
| **Faculty** | `prof_grace` | `grace.hopper@college.edu` | CSE Associate Professor — teaches CS302 (OS) |
| **Student** | `alex_rivera` | `alex.r@college.edu` | Good attendance record (100% in DBMS) |
| **Student** | `priya_patel` | `priya.p@college.edu` | 1 approved medical leave (87.5% attendance) |
| **Student** | `marcus_vance` | `marcus.v@college.edu` | ⚠️ Shortage Alert — 50% attendance (4/8 sessions) |

---

## 7. SQL Reports & Analytics Catalog

The **Reports Hub** (`/reports`) includes **8 analytical queries** demonstrating SQL best practices (JOINs, GROUP BY, HAVING, Subqueries, Views):

| # | Report | Key SQL Concepts |
|---|---|---|
| 1 | Student-wise Attendance Percentage | `v_student_course_attendance` view, GROUP BY |
| 2 | Course-wise Attendance Summary | Aggregated JOINs, AVG |
| 3 | Attendance Shortage Roster (< 75%) | HAVING clause, subquery |
| 4 | Leave Application History & Audit | Multi-table JOIN, audit trail |
| 5 | Pending Leave Queue | Filtered status query |
| 6 | Faculty Course Allocation Matrix | Workload analysis, COUNT DISTINCT |
| 7 | Makeup Session Participation | LEFT JOIN, makeup register |
| 8 | Monthly Attendance Trends | `DATE_FORMAT`, temporal aggregation |

> **CSV Export:** Every report features a 1-click **Export to CSV** button.

---

## 8. Project Structure

```
DBMS_PBL/
├── app.py                  # Flask app factory & blueprint registration
├── config.py               # Environment config loader
├── init_db.py              # One-click DB initialization script
├── schema.sql              # Full 3NF database schema (16 tables + 2 views)
├── seed.sql                # Realistic demo data
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── database/
│   └── connection.py       # MySQL connection pool
├── routes/
│   ├── auth.py             # Login / logout / session
│   ├── attendance.py       # Mark & view attendance
│   ├── courses.py          # Course & section management
│   ├── dashboard.py        # Role-based dashboards
│   ├── faculty.py          # Faculty management
│   ├── leaves.py           # Leave applications & approvals
│   ├── makeup.py           # Makeup sessions
│   ├── reports.py          # 8 analytical reports + CSV export
│   └── students.py         # Student management
├── templates/              # Jinja2 HTML templates (16 pages)
├── static/
│   ├── css/style.css       # Design system
│   └── js/app.js           # Frontend interactivity
└── test_attendease.py      # Automated test suite (9 categories)
```

---

## 9. Automated Testing

```powershell
python test_attendease.py
```

Tests cover 9 core categories:
- ✅ Password hashing & verification
- ✅ Attendance percentage formula correctness
- ✅ Shortage alert evaluation rules
- ✅ Leave date validation
- ✅ Unauthenticated access redirection
- ✅ Role-based authorization (Student vs Admin, Faculty vs Admin)
- ✅ Login UI structure
- ✅ CSV report streaming response format

---

## 10. Troubleshooting

| Error | Fix |
|---|---|
| **Error 1045** — Access denied for 'root' | Check password in `.env` or pass `--password` to `init_db.py` |
| **Error 2003** — Can't connect to MySQL | Run `net start MySQL80` in an admin PowerShell |
| **Port 5000 in use** | Add `PORT=5001` to `.env` and restart |
| **Module not found** | Run `pip install -r requirements.txt` |

---

## 11. License & Credits

**Developed for the College Database Management System (DBMS) Project**
**Author:** Atharva Singh
**Repository:** [github.com/atharva-singh-07/DBMS_PBL](https://github.com/atharva-singh-07/DBMS_PBL)
