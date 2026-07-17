"""
student.py
Defines the Student model — a simple data class representing
one row in the students table.
"""


class Student:
    def __init__(self, student_id=None, name="", age=0, gender="", department="",
                 year=0, email="", phone="", address="", admission_date="", cgpa=0.0):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.gender = gender
        self.department = department
        self.year = year
        self.email = email
        self.phone = phone
        self.address = address
        self.admission_date = admission_date
        self.cgpa = cgpa

    def to_tuple(self):
        """Return field values in the order the INSERT query expects
        (excludes student_id, which is auto-generated)."""
        return (
            self.name, self.age, self.gender, self.department, self.year,
            self.email, self.phone, self.address, self.admission_date, self.cgpa
        )

    @staticmethod
    def from_row(row):
        """Build a Student object from a full database row."""
        return Student(
            student_id=row[0], name=row[1], age=row[2], gender=row[3],
            department=row[4], year=row[5], email=row[6], phone=row[7],
            address=row[8], admission_date=row[9], cgpa=row[10]
        )

    def __str__(self):
        return f"[{self.student_id}] {self.name} - {self.department} - CGPA: {self.cgpa}"
