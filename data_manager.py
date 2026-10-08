from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

STUDENTS_FILE = DATA_DIR / "students.csv"
PROGRESS_FILE = DATA_DIR / "progress.csv"


def _ensure_data_files():
    DATA_DIR.mkdir(exist_ok=True)

    if not STUDENTS_FILE.exists():
        pd.DataFrame(
            columns=["student_id", "name", "email"]
        ).to_csv(STUDENTS_FILE, index=False)

    if not PROGRESS_FILE.exists():
        pd.DataFrame(
            columns=[
                "student_id",
                "unit",
                "activity",
                "completion",
                "date"
            ]
        ).to_csv(PROGRESS_FILE, index=False)


def load_students():
    _ensure_data_files()

    try:
        return pd.read_csv(
            STUDENTS_FILE,
            dtype={"student_id": str}
        )
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame(
            columns=["student_id", "name", "email"]
        )


def load_progress():
    _ensure_data_files()

    try:
        return pd.read_csv(
            PROGRESS_FILE,
            dtype={
                "student_id": str,
                "completion": float
            }
        )
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame(
            columns=[
                "student_id",
                "unit",
                "activity",
                "completion",
                "date"
            ]
        )


def add_student(student_id, name, email):
    _ensure_data_files()

    student_id = str(student_id).strip()
    name = str(name).strip()
    email = str(email).strip()

    try:
        students = load_students()

        if student_id in students["student_id"].astype(str).values:
            return False, "Student ID already exists."

        new_student = pd.DataFrame([
            {
                "student_id": student_id,
                "name": name,
                "email": email
            }
        ])

        students = pd.concat(
            [students, new_student],
            ignore_index=True
        )

        students.to_csv(STUDENTS_FILE, index=False)

        return True, "Student added successfully."

    except (OSError, PermissionError) as e:
        return False, f"Unable to save student data: {e}"


def update_student(old_student_id, new_student_id, name, email):
    _ensure_data_files()

    old_student_id = str(old_student_id).strip()
    new_student_id = str(new_student_id).strip()
    name = str(name).strip()
    email = str(email).strip()

    try:
        students = load_students()
        progress = load_progress()

        if old_student_id not in students["student_id"].astype(str).values:
            return False, "Student ID not found."

        if old_student_id != new_student_id:
            if new_student_id in students["student_id"].astype(str).values:
                return False, "New Student ID already exists."

        students.loc[
            students["student_id"].astype(str) == old_student_id,
            "student_id"
        ] = new_student_id

        students.loc[
            students["student_id"].astype(str) == new_student_id,
            "name"
        ] = name

        students.loc[
            students["student_id"].astype(str) == new_student_id,
            "email"
        ] = email

        progress.loc[
            progress["student_id"].astype(str) == old_student_id,
            "student_id"
        ] = new_student_id

        students.to_csv(STUDENTS_FILE, index=False)
        progress.to_csv(PROGRESS_FILE, index=False)

        return True, "Student details updated successfully."

    except (OSError, PermissionError) as e:
        return False, f"Unable to update student data: {e}"


def update_progress(student_id, unit, activity, completion, date):
    _ensure_data_files()

    student_id = str(student_id).strip()
    unit = str(unit).strip()
    activity = str(activity).strip()

    try:
        completion = float(completion)

        if not 0 <= completion <= 100:
            return False, "Completion must be between 0 and 100."

        students = load_students()

        if student_id not in students["student_id"].astype(str).values:
            return False, "Student ID does not exist."

        progress = load_progress()

        new_record = pd.DataFrame([
            {
                "student_id": student_id,
                "unit": unit,
                "activity": activity,
                "completion": completion,
                "date": date
            }
        ])

        progress = pd.concat(
            [progress, new_record],
            ignore_index=True
        )

        progress.to_csv(PROGRESS_FILE, index=False)

        return True, "Progress updated successfully."

    except ValueError:
        return False, "Completion must be a valid number."

    except (OSError, PermissionError) as e:
        return False, f"Unable to save progress data: {e}"


def delete_student(student_id):
    _ensure_data_files()

    student_id = str(student_id).strip()

    try:
        students = load_students()
        progress = load_progress()

        if student_id not in students["student_id"].astype(str).values:
            return False, "Student ID not found."

        students = students[
            students["student_id"].astype(str) != student_id
        ]

        progress = progress[
            progress["student_id"].astype(str) != student_id
        ]

        students.to_csv(STUDENTS_FILE, index=False)
        progress.to_csv(PROGRESS_FILE, index=False)

        return True, "Student and associated progress deleted."

    except (OSError, PermissionError) as e:
        return False, f"Unable to delete data: {e}"


def get_student_progress(student_id):
    progress = load_progress()

    return progress[
        progress["student_id"].astype(str)
        == str(student_id).strip()
    ].copy()


if __name__ == "__main__":
    print(load_students())
    print(load_progress())