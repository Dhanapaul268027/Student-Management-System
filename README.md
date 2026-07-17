# Student Management System

A console-based Student Management System built with **Python** and **SQLite**.
It lets an administrator add, view, search, update, delete, sort, filter, and
report on student records, following a clean, modular architecture.

## Features

- Add, view, search, update, and delete students
- Input validation (name, email, phone, age, CGPA, duplicate email)
- Sort students by name, CGPA, or department
- Filter students by department, year, or CGPA threshold
- Reports: total students, department-wise count, highest CGPA, average CGPA
- Export all records to CSV
- One-command database backup

## Project Structure

```
StudentManagementSystem/
├── Database/                # SQLite DB file, CSV export, backups live here
├── main.py                  # Entry point — starts the app
├── menu.py                  # Menu display and user input handling
├── student.py                # Student model (OOP data class)
├── database.py               # SQLite connection and query execution
├── student_service.py        # Business logic (CRUD, sort, filter, reports)
├── config.py                  # Paths and app-wide constants
├── utils.py                   # Validation, formatting, printing helpers
├── requirements.txt
├── .gitignore
└── README.md
```

## Architecture

```
User → Main Module → Menu Controller → Business Logic → Database Layer → SQLite
                              │
                              └──→ Utility Functions
```

Each module has one job:

- **main.py** — starts the app, wires everything together
- **menu.py** — talks to the user, never touches SQL directly
- **student_service.py** — all business rules, talks to the database layer
- **database.py** — the only file that knows about SQLite specifics
- **student.py** — a plain data model
- **utils.py** — validation, formatting, and console printing helpers
- **config.py** — shared constants and file paths

## Getting Started

### Requirements

- Python 3.8+
- No external packages required (uses only the standard library)

### Run it

```bash
git clone <your-repo-url>
cd StudentManagementSystem
python main.py
```

The database file is created automatically inside `Database/` on first run.

## Example Menu

```
==============================
 STUDENT MANAGEMENT SYSTEM
==============================
1. Add Student
2. View Students
3. Search Student
4. Update Student
5. Delete Student
6. Sort / Filter Students
7. Reports
8. Export Data (CSV)
9. Backup Database
10. Exit
==============================
```

## Database Schema

| Column          | Type    |
|-----------------|---------|
| student_id      | INTEGER PRIMARY KEY AUTOINCREMENT |
| name            | TEXT    |
| age             | INTEGER |
| gender          | TEXT    |
| department      | TEXT    |
| year            | INTEGER |
| email           | TEXT (UNIQUE) |
| phone           | TEXT    |
| address         | TEXT    |
| admission_date  | TEXT    |
| cgpa            | REAL    |

## Future Enhancements

- Login system with username/password and role-based access
- Attendance and marks management
- REST API with Flask or FastAPI
- Web interface
- Docker deployment
- Export reports to PDF
- Automated tests

## License

This is a learning project — feel free to use it as a template for your own.
