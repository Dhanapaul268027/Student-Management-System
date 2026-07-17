"""
config.py
Centralized configuration for the Student Management System.
Keeping paths and constants here avoids magic numbers/strings
scattered across the codebase.
"""

import os

# ---- Paths ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "Database")

DATABASE_NAME = os.path.join(DATABASE_DIR, "students.db")
BACKUP_NAME = os.path.join(DATABASE_DIR, "students_backup.db")
EXPORT_CSV_NAME = os.path.join(DATABASE_DIR, "students_export.csv")

# Make sure the Database folder exists even on a fresh clone
os.makedirs(DATABASE_DIR, exist_ok=True)

# ---- App info ----
APP_NAME = "STUDENT MANAGEMENT SYSTEM"

# ---- Validation rules ----
MIN_AGE = 15
MAX_AGE = 60
MIN_CGPA = 0.0
MAX_CGPA = 10.0
PHONE_LENGTH = 10

# ---- Editable fields for update operations ----
UPDATABLE_FIELDS = {"name", "email", "phone", "department", "cgpa"}

# ---- Fields allowed in search/sort/filter to prevent SQL injection
#      via dynamically built column names ----
SEARCHABLE_FIELDS = {"student_id", "name", "department"}
SORTABLE_FIELDS = {"name", "cgpa", "department"}
