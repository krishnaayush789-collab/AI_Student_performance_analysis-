import csv
import random
import os

random.seed(42)

os.makedirs("data", exist_ok=True)

first_names = [
    "Aarav", "Vivaan", "Aditya", "Arjun", "Reyansh",
    "Ananya", "Aanya", "Diya", "Priya", "Ishita",
    "Rahul", "Rohan", "Sneha", "Neha", "Karan",
    "Simran", "Aditi", "Kabir", "Meera", "Ishaan"
]

last_names = [
    "Sharma", "Verma", "Singh", "Gupta", "Kumar",
    "Patel", "Mishra", "Yadav", "Jain", "Das"
]

grades = ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5"]

subjects = [
    "Mathematics",
    "English",
    "Science",
    "Computer",
    "Social_Studies"
]

positive_feedback = [
    "I enjoy learning and understand my subjects well.",
    "My teachers explain every topic clearly.",
    "I am happy with my academic performance.",
    "I find my classes interesting and helpful."
]

negative_feedback = [
    "I find Mathematics very difficult.",
    "I need more practice to improve my marks.",
    "I have difficulty understanding Science topics.",
    "I need additional support from my teachers."
]

neutral_feedback = [
    "My classes are going normally.",
    "I want to improve my academic performance.",
    "Some subjects are easy and some are difficult.",
    "I am working on improving my attendance."
]

student_rows = []
feedback_rows = []

for i in range(1, 201):

    name = (
        random.choice(first_names) + " " +
        random.choice(last_names)
    )

    gender = random.choice(["Male", "Female"])
    grade = random.choice(grades)
    attendance = random.randint(45, 100)

    marks = {
        subject: random.randint(25, 100)
        for subject in subjects
    }

    average = round(sum(marks.values()) / len(subjects), 2)

    if average >= 85:
        grade_result = "A"
    elif average >= 70:
        grade_result = "B"
    elif average >= 55:
        grade_result = "C"
    elif average >= 40:
        grade_result = "D"
    else:
        grade_result = "F"

    result = "Pass" if min(marks.values()) >= 33 else "Fail"

    student_rows.append({
        "Student_ID": f"STU{i:03d}",
        "Name": name,
        "Gender": gender,
        "Grade": grade,
        "Attendance": attendance,
        **marks,
        "Average": average,
        "Grade_Result": grade_result,
        "Result": result
    })

    feedback = random.choice(
        positive_feedback +
        negative_feedback +
        neutral_feedback
    )

    feedback_rows.append({
        "Student_ID": f"STU{i:03d}",
        "Feedback": feedback
    })


# Save student dataset
with open("data/students.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=student_rows[0].keys()
    )
    writer.writeheader()
    writer.writerows(student_rows)


# Save feedback dataset
with open("data/feedback.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["Student_ID", "Feedback"]
    )
    writer.writeheader()
    writer.writerows(feedback_rows)


print("Dataset created successfully!")
print("Total Students:", len(student_rows))
print("Total Feedback:", len(feedback_rows))
print("Files saved inside data folder.")