# Handles Matplotlib visual reports.
# At least two meaningful reports will be implemented here.
import matplotlib.pyplot as plt
import pandas as pd

from analytics import all_student_progress, unit_progress
from data_manager import load_progress


def student_progress_report():
    data = all_student_progress()

    if data.empty:
        return

    plt.figure(figsize=(8, 5))
    plt.bar(data["name"], data["progress"])
    plt.xlabel("Students")
    plt.ylabel("Progress (%)")
    plt.title("Student-wise Course Progress")
    plt.ylim(0, 100)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def unit_progress_report():
    data = unit_progress()

    if data.empty:
        return

    plt.figure(figsize=(8, 5))
    plt.bar(data["unit"], data["completion"])
    plt.xlabel("Units")
    plt.ylabel("Completion (%)")
    plt.title("Unit-wise Completion")
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.show()


def student_trend_report(student_id):
    progress = load_progress()

    data = progress[
        progress["student_id"].astype(str) == str(student_id)
    ].copy()

    if data.empty:
        return

    data["date"] = pd.to_datetime(
        data["date"],
        errors="coerce"
    )

    data = data.sort_values("date")

    plt.figure(figsize=(8, 5))
    plt.plot(
        data["date"],
        data["completion"],
        marker="o"
    )
    plt.xlabel("Date")
    plt.ylabel("Completion (%)")
    plt.title(f"Progress Trend - Student {student_id}")
    plt.ylim(0, 100)
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()