"""
main.py
Entry point of the Student Management System.
Responsible only for wiring the pieces together and starting the app.
"""

from database import Database
from student_service import StudentService
from menu import Menu
from config import APP_NAME


def main():
    print(f"Welcome to {APP_NAME}")

    db = Database()
    db.connect()
    db.create_tables()

    service = StudentService(db)
    menu = Menu(service)

    try:
        menu.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Exiting safely...")
    finally:
        db.close()


if __name__ == "__main__":
    main()
