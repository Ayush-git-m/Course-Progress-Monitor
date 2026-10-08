# Handles progress calculations and analysis.
# Pandas and NumPy based functions will be implemented here.
import pandas as pd
import numpy as np

from data_manager import load_students, load_progress


def student_progress(student_id):
    progress = load_progress()

    data = progress[
        progress["student_id"].astype(str) == str(student_id)
    ]

    if data.empty:
        return 0

    return round(data["completion"].mean(), 2)


def all_student_progress():
    students = load_students()
    progress = load_progress()

    if progress.empty:
        students["progress"] = 0
        return students

    result = progress.groupby("student_id")["completion"].mean().reset_index()

    result["completion"] = result["completion"].round(2)

    result = result.rename(
        columns={"completion": "progress"}
    )

    students["student_id"] = students["student_id"].astype(str)
    result["student_id"] = result["student_id"].astype(str)

    return students.merge(
        result,
        on="student_id",
        how="left"
    ).fillna({"progress": 0})


def unit_progress():
    progress = load_progress()

    if progress.empty:
        return pd.DataFrame(
            columns=["unit", "completion"]
        )

    result = progress.groupby("unit")["completion"].mean().reset_index()

    result["completion"] = result["completion"].round(2)

    return result


def incomplete_work(threshold=50):
    progress = load_progress()

    if progress.empty:
        return progress

    return progress[
        progress["completion"] < threshold
    ].sort_values("completion")


def top_students(n=5):
    data = all_student_progress()

    return data.sort_values(
        "progress",
        ascending=False
    ).head(n)


def slow_students(n=5):
    data = all_student_progress()

    return data.sort_values(
        "progress",
        ascending=True
    ).head(n)


def overall_progress():
    progress = load_progress()

    if progress.empty:
        return 0

    return round(
        progress["completion"].mean(),
        2
    )


def progress_trend(student_id):
    progress = load_progress()

    data = progress[
        progress["student_id"].astype(str) == str(student_id)
    ].copy()

    if data.empty:
        return {
            "average_change": 0,
            "status": "No Data"
        }

    data["date"] = pd.to_datetime(
        data["date"],
        errors="coerce"
    )

    data = data.sort_values("date")

    values = data["completion"].to_numpy()

    if len(values) < 2:
        return {
            "average_change": 0,
            "status": "Not Enough Data"
        }

    changes = np.diff(values)

    average_change = round(
        np.mean(changes),
        2
    )

    if np.all(changes >= 0):
        status = "Steady Progress"
    else:
        status = "Needs Attention"

    return {
        "average_change": average_change,
        "status": status
    }


def student_summary(student_id):
    students = load_students()

    student = students[
        students["student_id"].astype(str) == str(student_id)
    ]

    if student.empty:
        return None

    progress = student_progress(student_id)
    trend = progress_trend(student_id)

    return {
        "student_id": str(student.iloc[0]["student_id"]),
        "name": student.iloc[0]["name"],
        "email": student.iloc[0]["email"],
        "progress": progress,
        "average_change": trend["average_change"],
        "status": trend["status"]
    }