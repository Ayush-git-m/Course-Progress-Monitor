# Handles input validation and reusable validation helpers.
import re
from datetime import datetime


def validate_student_id(student_id):
    student_id = str(student_id).strip()

    if not student_id:
        return False

    return student_id.isdigit()


def validate_name(name):
    name = str(name).strip()

    if not name:
        return False

    return all(char.isalpha() or char.isspace() for char in name)


def validate_email(email):
    email = str(email).strip()

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    return bool(re.match(pattern, email))


def validate_completion(completion):
    try:
        value = float(completion)
        return 0 <= value <= 100
    except (ValueError, TypeError):
        return False


def validate_date(date):
    try:
        datetime.strptime(str(date), "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_student(student_id, name, email):
    if not validate_student_id(student_id):
        return False, "Invalid Student ID."

    if not validate_name(name):
        return False, "Invalid name."

    if not validate_email(email):
        return False, "Invalid email."

    return True, "Valid student data."


def validate_progress(student_id, unit, activity, completion, date):
    if not validate_student_id(student_id):
        return False, "Invalid Student ID."

    if not str(unit).strip():
        return False, "Unit is required."

    if not str(activity).strip():
        return False, "Activity is required."

    if not validate_completion(completion):
        return False, "Completion must be between 0 and 100."

    if not validate_date(date):
        return False, "Date must be in YYYY-MM-DD format."

    return True, "Valid progress data."