# 🧑‍💼 Simple HRM – Attendance & Payroll System

## Overview

This project is a **lightweight Human Resource Management (HRM) system** designed to track employee attendance, working hours, overtime, late hours, and salary deductions.
It is built as a **basic internal web application** focused on **progress tracking and reporting**, rather than a full-scale enterprise HR platform.

The system uses **Flask** as the backend API, **SQLite** as the database, and **Streamlit** as a simple frontend/dashboard layer.

---

## Key Features

### Employee Features

* User registration and login
* Daily check-in and check-out
* Automatic calculation of:

  * Total working hours
  * Overtime hours
  * Late hours
  * Salary deductions (per-hour basis)
* View personal attendance history and monthly summaries

### Admin Features

* View all employees
* Access attendance logs for all users
* Monthly attendance and salary reports
* Export reports (CSV/Excel-ready)
* Centralized control of attendance and payroll data

---

## Tech Stack

### Backend

* **Flask** – REST API and business logic
* **Flask-JWT** – Authentication
* **SQLAlchemy** – ORM
* **SQLite** – Database (MVP)

### Frontend

* **Streamlit** – Dashboard UI and reporting interface

---

## Architecture

```
Streamlit UI (Dashboard)
        |
        | REST APIs (JWT Auth)
        |
Flask Backend (Business Logic)
        |
        | ORM
        |
SQLite Database
```

* All authentication and calculations are handled by **Flask**
* Streamlit acts only as a **presentation layer**
* No direct database access from the frontend

---

## Core Functional Logic

* **Check-in / Check-out** based on server time
* Configurable office start time and grace period
* Automatic calculation of:

  * Late hours
  * Overtime
  * Salary deductions based on hourly rate
* One attendance record per user per day

---

## Project Structure (Suggested)

```
hrm-system/
│
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── attendance.py
│   │   └── reports.py
│   └── database.db
│
├── frontend/
│   └── streamlit_app.py
│
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/hrm-system.git
cd hrm-system
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Backend (Flask)

```bash
python backend/app.py
```

### 4. Run Frontend (Streamlit)

```bash
streamlit run frontend/streamlit_app.py
```

---

## Use Cases

* Small teams
* Internal company tools
* Attendance tracking prototypes
* Payroll logic validation
* Reporting and analytics demos

---

## Limitations

* Not intended for large-scale or public production use
* Limited concurrent user handling
* Streamlit UI is functional, not enterprise-grade

---

## Future Enhancements

* Role-based permissions
* Leave and holiday management
* Email notifications
* PostgreSQL migration
* Frontend upgrade (React/Next.js)
* Face recognition or biometric check-in

---

## License

This project is intended for educational and internal use.
You may adapt and extend it as needed.

---

---
