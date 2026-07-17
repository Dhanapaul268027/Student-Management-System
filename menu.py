"""
menu.py
The presentation layer. Displays the menu, collects and validates
raw user input, then hands clean data off to StudentService.
No SQL and no direct database access happens in this file.
"""

import utils
from student import Student
from student_service import StudentService
from config import APP_NAME


class Menu:
    def __init__(self, service: StudentService):
        self.service = service

    def display_main_menu(self):
        print("\n" + "=" * 30)
        print(f" {APP_NAME}")
        print("=" * 30)
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Sort / Filter Students")
        print("7. Reports")
        print("8. Export Data (CSV)")
        print("9. Backup Database")
        print("10. Exit")
        print("=" * 30)

    def run(self):
        actions = {
            "1": self.add_student_flow,
            "2": self.service.view_students,
            "3": self.search_student_flow,
            "4": self.update_student_flow,
            "5": self.delete_student_flow,
            "6": self.sort_filter_flow,
            "7": self.service.generate_reports,
            "8": self.service.export_to_csv,
            "9": self.service.backup_database,
        }

        while True:
            self.display_main_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "10":
                print("\nExiting Student Management System. Goodbye!\n")
                break

            action = actions.get(choice)
            if action:
                action()
            else:
                utils.print_error("Invalid choice. Please try again.")

    # ---------- Flows ----------

    def add_student_flow(self):
        print("\n--- Add New Student ---")

        name = input("Name: ").strip()
        if not utils.validate_name(name):
            utils.print_error("Invalid name.")
            return

        age = input("Age: ").strip()
        if not utils.validate_age(age):
            utils.print_error("Invalid age.")
            return

        gender = input("Gender: ").strip()
        department = input("Department: ").strip()

        year = input("Year: ").strip()
        if not year.isdigit():
            utils.print_error("Invalid year.")
            return

        email = input("Email: ").strip()
        if not utils.validate_email(email):
            utils.print_error("Invalid email format.")
            return
        if self.service.email_exists(email):
            utils.print_error("A student with this email already exists.")
            return

        phone = input("Phone: ").strip()
        if not utils.validate_phone(phone):
            utils.print_error("Phone number must be 10 digits.")
            return

        address = input("Address: ").strip()

        cgpa = input("CGPA: ").strip()
        if not utils.validate_cgpa(cgpa):
            utils.print_error("CGPA must be between 0 and 10.")
            return

        student = Student(
            name=name, age=int(age), gender=gender, department=department,
            year=int(year), email=email, phone=phone, address=address,
            admission_date=utils.get_current_date(), cgpa=float(cgpa)
        )
        self.service.add_student(student)

    def search_student_flow(self):
        print("\n--- Search Student ---")
        print("1. By ID   2. By Name   3. By Department")
        opt = input("Choose search type: ").strip()
        field_map = {"1": "student_id", "2": "name", "3": "department"}
        field = field_map.get(opt)
        if not field:
            utils.print_error("Invalid option.")
            return

        value = input("Enter search value: ").strip()
        self.service.search_student(field, value)

    def update_student_flow(self):
        print("\n--- Update Student ---")
        student_id = input("Enter Student ID to update: ").strip()
        if not student_id.isdigit() or not self.service.student_exists(student_id):
            utils.print_error("Student not found.")
            return

        print("Editable fields: name, email, phone, department, cgpa")
        field = input("Field to update: ").strip().lower()
        value = input("New value: ").strip()

        if field == "cgpa" and not utils.validate_cgpa(value):
            utils.print_error("Invalid CGPA.")
            return
        if field == "email" and not utils.validate_email(value):
            utils.print_error("Invalid email.")
            return
        if field == "phone" and not utils.validate_phone(value):
            utils.print_error("Invalid phone.")
            return

        self.service.update_student(student_id, field, value)

    def delete_student_flow(self):
        print("\n--- Delete Student ---")
        student_id = input("Enter Student ID to delete: ").strip()
        if not student_id.isdigit() or not self.service.student_exists(student_id):
            utils.print_error("Student not found.")
            return

        if utils.confirm_action(f"Are you sure you want to delete student {student_id}? (Y/N): "):
            self.service.delete_student(student_id)
        else:
            print("Deletion cancelled.")

    def sort_filter_flow(self):
        print("\n--- Sort / Filter Students ---")
        print("1. Sort by Name")
        print("2. Sort by CGPA")
        print("3. Sort by Department")
        print("4. Filter by Department")
        print("5. Filter by Year")
        print("6. Filter by CGPA greater than a value")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            self.service.sort_students("name")
        elif choice == "2":
            self.service.sort_students("cgpa")
        elif choice == "3":
            self.service.sort_students("department")
        elif choice == "4":
            dept = input("Enter department: ").strip()
            self.service.filter_students(department=dept)
        elif choice == "5":
            year = input("Enter year: ").strip()
            self.service.filter_students(year=year)
        elif choice == "6":
            min_cgpa = input("Enter minimum CGPA: ").strip()
            if utils.validate_cgpa(min_cgpa):
                self.service.filter_students(min_cgpa=float(min_cgpa))
            else:
                utils.print_error("Invalid CGPA value.")
        else:
            utils.print_error("Invalid choice.")
