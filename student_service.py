"""
student_service.py
The business logic layer. Menu.py never talks to the database
directly — it always goes through StudentService, which validates
intent, builds queries safely, and delegates execution to Database.
"""

import csv
import shutil

import utils
from student import Student
from database import Database
from config import BACKUP_NAME, EXPORT_CSV_NAME, SEARCHABLE_FIELDS, SORTABLE_FIELDS, UPDATABLE_FIELDS

ALL_COLUMNS = ["student_id", "name", "age", "gender", "department", "year",
               "email", "phone", "address", "admission_date", "cgpa"]
ALL_HEADERS = ["ID", "Name", "Age", "Gender", "Department", "Year",
               "Email", "Phone", "Address", "Admission Date", "CGPA"]


class StudentService:
    def __init__(self, db: Database):
        self.db = db

    # ---------- CRUD ----------

    def add_student(self, student: Student):
        query = """
        INSERT INTO students
            (name, age, gender, department, year, email, phone, address, admission_date, cgpa)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.db.execute(query, student.to_tuple())
        utils.print_success("Student added successfully.")

    def view_students(self):
        rows = self.db.fetchall(
            "SELECT student_id, name, department, cgpa, phone FROM students ORDER BY student_id"
        )
        utils.print_table(rows, ["ID", "Name", "Department", "CGPA", "Phone"])

    def search_student(self, field, value):
        if field not in SEARCHABLE_FIELDS:
            utils.print_error("Invalid search field.")
            return

        if field == "student_id":
            query = "SELECT * FROM students WHERE student_id = ?"
            params = (value,)
        else:
            query = f"SELECT * FROM students WHERE {field} LIKE ?"
            params = (f"%{value}%",)

        rows = self.db.fetchall(query, params)
        utils.print_table(rows, ALL_HEADERS)

    def update_student(self, student_id, field, value):
        if field not in UPDATABLE_FIELDS:
            utils.print_error("That field cannot be updated.")
            return

        query = f"UPDATE students SET {field} = ? WHERE student_id = ?"
        cursor = self.db.execute(query, (value, student_id))
        if cursor.rowcount == 0:
            utils.print_error("Student not found.")
        else:
            utils.print_success("Student updated successfully.")

    def delete_student(self, student_id):
        cursor = self.db.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        if cursor.rowcount == 0:
            utils.print_error("Student not found.")
        else:
            utils.print_success("Student deleted successfully.")

    # ---------- Lookups used for validation ----------

    def student_exists(self, student_id):
        return self.db.fetchone(
            "SELECT 1 FROM students WHERE student_id = ?", (student_id,)
        ) is not None

    def email_exists(self, email):
        return self.db.fetchone(
            "SELECT 1 FROM students WHERE email = ?", (email,)
        ) is not None

    # ---------- Sorting & filtering ----------

    def sort_students(self, by="name"):
        if by not in SORTABLE_FIELDS:
            utils.print_error("Invalid sort field.")
            return
        order = "DESC" if by == "cgpa" else "ASC"
        query = f"SELECT student_id, name, department, cgpa FROM students ORDER BY {by} {order}"
        rows = self.db.fetchall(query)
        utils.print_table(rows, ["ID", "Name", "Department", "CGPA"])

    def filter_students(self, department=None, year=None, min_cgpa=None):
        query = "SELECT student_id, name, department, year, cgpa FROM students WHERE 1=1"
        params = []
        if department:
            query += " AND department = ?"
            params.append(department)
        if year:
            query += " AND year = ?"
            params.append(year)
        if min_cgpa is not None:
            query += " AND cgpa > ?"
            params.append(min_cgpa)

        rows = self.db.fetchall(query, tuple(params))
        utils.print_table(rows, ["ID", "Name", "Department", "Year", "CGPA"])

    # ---------- Reports ----------

    def generate_reports(self):
        total = self.db.fetchone("SELECT COUNT(*) FROM students")[0]
        dept_counts = self.db.fetchall(
            "SELECT department, COUNT(*) FROM students GROUP BY department"
        )
        highest = self.db.fetchone(
            "SELECT name, cgpa FROM students ORDER BY cgpa DESC LIMIT 1"
        )
        avg_cgpa = self.db.fetchone("SELECT AVG(cgpa) FROM students")[0]

        print("\n===== REPORT =====")
        print(f"Total Students: {total}")
        print("\nDepartment-wise Count:")
        for dept, count in dept_counts:
            print(f"  {dept} : {count}")
        if highest:
            print(f"\nHighest CGPA: {highest[0]} ({highest[1]})")
        print(f"Average CGPA: {round(avg_cgpa, 2) if avg_cgpa is not None else 0}")
        print("===================\n")

    # ---------- Export & backup ----------

    def export_to_csv(self, filename=EXPORT_CSV_NAME):
        rows = self.db.fetchall(f"SELECT {', '.join(ALL_COLUMNS)} FROM students")
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(ALL_HEADERS)
            writer.writerows(rows)
        utils.print_success(f"Data exported to {filename}")

    def backup_database(self, destination=BACKUP_NAME):
        shutil.copy(self.db.db_name, destination)
        utils.print_success(f"Database backed up to {destination}")
