"""
utils.py
Shared helper functions: input validation, table printing,
date formatting, and consistent error/success messages.
"""

import re
from datetime import datetime
from config import MIN_AGE, MAX_AGE, MIN_CGPA, MAX_CGPA, PHONE_LENGTH

EMAIL_PATTERN = r"^[\w\.-]+@[\w\.-]+\.\w+$"


def validate_name(name):
    return bool(name) and all(part.isalpha() for part in name.split(" ") if part)


def validate_email(email):
    return re.match(EMAIL_PATTERN, email) is not None


def validate_phone(phone):
    return phone.isdigit() and len(phone) == PHONE_LENGTH


def validate_age(age_str, min_age=MIN_AGE, max_age=MAX_AGE):
    if not age_str.isdigit():
        return False
    return min_age <= int(age_str) <= max_age


def validate_cgpa(cgpa_str, min_cgpa=MIN_CGPA, max_cgpa=MAX_CGPA):
    try:
        cgpa = float(cgpa_str)
    except ValueError:
        return False
    return min_cgpa <= cgpa <= max_cgpa


def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")


def print_table(rows, headers):
    """Pretty-print rows in an aligned, readable table."""
    if not rows:
        print("\nNo records found.\n")
        return

    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)))

    header_line = " | ".join(str(h).ljust(col_widths[i]) for i, h in enumerate(headers))
    print("\n" + header_line)
    print("-" * len(header_line))
    for row in rows:
        print(" | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row)))
    print()


def print_error(message):
    print(f"\n[ERROR] {message}\n")


def print_success(message):
    print(f"\n[SUCCESS] {message}\n")


def confirm_action(prompt="Are you sure? (Y/N): "):
    choice = input(prompt).strip().lower()
    return choice == "y"
