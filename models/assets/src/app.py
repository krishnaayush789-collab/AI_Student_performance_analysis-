import joblib
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

# ---------------- LOAD DATA ----------------

@st.cache_data
def load_data():
    return pd.read_csv("data/students.csv")

df = load_data()

# Load trained ML model
model_path = "models/performance_model.pkl"

if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    model = None

# Load NLP sentiment results
sentiment_path = "data/sentiment_results.csv"

if os.path.exists(sentiment_path):
    sentiment_df = pd.read_csv(sentiment_path)
else:
    sentiment_df = pd.DataFrame()

st.markdown("""
<style>
.stApp {
    background: #F3F2FC !important;
    color: #302B40;
    font-family: Arial, sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.main .block-container {
    max-width: 1500px;
    padding: 1.5rem 2rem;
}

.topbar {
    background: linear-gradient(110deg, #26005C, #4B16A3);
    color: white;
    padding: 20px 26px;
    border-radius: 12px;
    margin-bottom: 22px;
    box-shadow: 0 4px 15px #26005C20;
}

.topbar h2 {
    margin: 0;
    font-size: 25px;
    font-weight: 700;
}

.topbar p {
    margin: 5px 0 0;
    color: #DCCBFF;
    font-size: 12px;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #E7E0F4;
    box-shadow: 0 3px 12px #3920640D;
    min-height: 110px;
    transition: 0.2s;
}

.metric-title {
    color: #777187;
    font-size: 13px;
}

.metric-value {
    color: #351078;
    font-size: 28px;
    font-weight: 700;
    margin-top: 10px;
}

.section-card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #E7E0F4;
    box-shadow: 0 3px 12px #3920640D;
    margin-bottom: 18px;
}

.student-card {
    background: white;
    border: 1px solid #E7E0F4;
    padding: 16px;
    border-radius: 14px;
    text-align: center;
}

h1, h2, h3 {
    color: #33254B;
}

div[data-testid="stSelectbox"] {
    background: white;
    border-radius: 8px;
}

div[data-testid="stDataFrame"] {
    background: white;
    border-radius: 12px;
    padding: 5px;
}

.stButton > button,
.stDownloadButton > button {
    background: #42118D;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 18px;
    font-weight: 600;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #6127B9;
    color: white;
    border: none;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown("""
<div class="topbar">
    <h2>🎓 Jasper Elite School</h2>
    <p>Student Performance Dashboard</p>
</div>
""", unsafe_allow_html=True)

# ---------------- FILTERS ----------------

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    selected_year = st.selectbox(
        "Select Year",
        ["2026-27"]
    )

with col2:
    grades = ["All Grades"] + sorted(
        df["Grade"].unique().tolist()
    )

    selected_grade = st.selectbox(
        "Select Grade",
        grades
    )

with col3:
    genders = ["All", "Male", "Female"]

    selected_gender = st.selectbox(
        "Select Gender",
        genders
    )

with col4:
    st.markdown("### 📊 Academic Overview")

# ---------------- FILTER DATA ----------------

filtered_df = df.copy()

if selected_grade != "All Grades":
    filtered_df = filtered_df[
        filtered_df["Grade"] == selected_grade
    ]

if selected_gender != "All":
    filtered_df = filtered_df[
        filtered_df["Gender"] == selected_gender
    ]

# ---------------- CALCULATIONS ----------------

total_students = len(filtered_df)

attendance = (
    filtered_df["Attendance"].mean()
    if total_students else 0
)

average_score = (
    filtered_df["Average"].mean()
    if total_students else 0
)

pass_rate = (
    (filtered_df["Result"] == "Pass").mean() * 100
    if total_students else 0
)

# ---------------- KPI CARDS ----------------

st.markdown("### 📌 School Statistics")

c1, c2, c3, c4 = st.columns(4)

metrics = [
    ("👨‍🎓 Total Students", total_students),
    ("📅 Attendance", f"{attendance:.1f}%"),
    ("📚 Average Score", f"{average_score:.1f}%"),
    ("🏆 Pass Rate", f"{pass_rate:.1f}%")
]

for col, (title, value) in zip(
    [c1, c2, c3, c4], metrics
):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("")

# ---------------- MAIN LAYOUT ----------------

left, right = st.columns([1.7, 1])

# ---------------- STUDENT COUNT ----------------

with left:

    st.markdown(
        '<div class="section-card">',
        unsafe_allow_html=True
    )

    st.subheader("👥 Student Count")

    grade_count = (
        filtered_df["Grade"]
        .value_counts()
        .reset_index()
    )

    grade_count.columns = ["Grade", "Students"]

    if not grade_count.empty:

        fig = px.pie(
            grade_count,
            names="Grade",
            values="Students",
            hole=0.65,
            color_discrete_sequence=[
                "#3F00A5",
                "#29C6DB",
                "#D638E8",
                "#49D8B8",
                "#E7C72B"
            ]
        )

        fig.update_layout(
            height=310,
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(orientation="v"),
            paper_bgcolor="white"
        )

        fig.update_traces(
            textinfo="percent"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- EXAMINATION RESULTS ----------------

    st.markdown(
        '<div class="section-card">',
        unsafe_allow_html=True
    )

    st.subheader("📊 Examination Results")

    subjects = [
        "Mathematics",
        "English",
        "Science",
        "Computer",
        "Social_Studies"
    ]

    chart_data = []

    for subject in subjects:
        chart_data.append({
            "Subject": subject,
            "Average": filtered_df[subject].mean()
            if total_students else 0
        })

    chart_df = pd.DataFrame(chart_data)

    fig2 = go.Figure()

    fig2.add_trace(go.Bar(
        x=chart_df["Subject"],
        y=chart_df["Average"],
        name="Average Marks",
        marker_color="#3900A5"
    ))

    fig2.update_layout(
        height=330,
        yaxis_title="Marks",
        yaxis=dict(range=[0, 100]),
        margin=dict(t=20, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- RIGHT SECTION ----------------

with right:

    # BEST STUDENTS

    st.markdown(
        '<div class="section-card">',
        unsafe_allow_html=True
    )

    st.subheader("🏆 Best in Marks")

    if total_students:

        top_students = filtered_df.nlargest(
            3, "Average"
        )

        for _, student in top_students.iterrows():

            st.markdown(
                f"**{student['Name']}** "
                f"— {student['Average']:.1f}%"
            )

            st.progress(
                float(student["Average"]) / 100
            )

    else:
        st.info("No student records found.")

    st.markdown("</div>", unsafe_allow_html=True)

    # BEST ATTENDANCE

    st.markdown(
        '<div class="section-card">',
        unsafe_allow_html=True
    )

    st.subheader("📅 Best in Attendance")

    if total_students:

        top_attendance = filtered_df.nlargest(
            3, "Attendance"
        )

        for _, student in top_attendance.iterrows():

            st.markdown(
                f"**{student['Name']}** "
                f"— {student['Attendance']}%"
            )

    st.markdown("</div>", unsafe_allow_html=True)

    # STUDENT DETAILS

    st.markdown(
        '<div class="section-card">',
        unsafe_allow_html=True
    )

    st.subheader("👨‍🎓 Student Details")

    if total_students:

        st.dataframe(
            filtered_df[
                ["Name", "Grade", "Average", "Attendance"]
            ].head(5),
            hide_index=True,
            use_container_width=True
        )

    else:
        st.info("No students available.")

    st.markdown("</div>", unsafe_allow_html=True)

    # AVERAGE SCORE

    st.markdown(
        '<div class="section-card">',
        unsafe_allow_html=True
    )

    st.subheader("📈 Average Score")

    score_cols = st.columns(2)

    with score_cols[0]:
        st.metric(
            "Academic Score",
            f"{average_score:.1f}%"
        )

    with score_cols[1]:
        st.metric(
            "Attendance",
            f"{attendance:.1f}%"
        )

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------

st.markdown("""
<center>
    <p style="color:gray;font-size:12px;">
    AI-Based Student Performance Analysis System |
    Powered by Python, Streamlit and Plotly
    </p>
</center>
""", unsafe_allow_html=True)
# ================= AI PERFORMANCE PREDICTION =================

st.markdown("---")
st.header("🤖 AI-Based Student Performance Prediction")

if model is not None and not filtered_df.empty:

    selected_id = st.selectbox(
        "Select Student for AI Analysis",
        filtered_df["Student_ID"].tolist()
    )

    student = filtered_df[
        filtered_df["Student_ID"] == selected_id
    ].iloc[0]

    features = [
        "Attendance",
        "Average",
        "Mathematics",
        "English",
        "Science",
        "Computer",
        "Social_Studies"
    ]

    input_data = pd.DataFrame(
        [student[features].to_dict()]
    )

    prediction = model.predict(input_data)[0]

    a, b, c = st.columns(3)

    with a:
        st.metric("Student", student["Name"])

    with b:
        st.metric("Average Score", f"{student['Average']:.1f}%")

    with c:
        st.metric("Attendance", f"{student['Attendance']}%")

    st.subheader("AI Predicted Academic Risk")

    if prediction == "High Risk":
        st.error("High Risk: Student needs immediate academic support.")

    elif prediction == "Moderate Risk":
        st.warning("Moderate Risk: Student needs improvement.")

    else:
        st.success("Low Risk: Student performance is satisfactory.")

else:
    st.info("ML model or student data is unavailable.")


# ================= NLP FEEDBACK ANALYSIS =================

st.markdown("---")
st.header("🧠 NLP Student Feedback Analysis")

if not sentiment_df.empty:

    sentiment_counts = (
        sentiment_df["Sentiment"].value_counts()
        .reset_index()
    )

    sentiment_counts.columns = ["Sentiment", "Count"]

    col1, col2 = st.columns(2)

    with col1:

        fig = px.pie(
            sentiment_counts,
            names="Sentiment",
            values="Count",
            hole=0.6,
            title="Student Feedback Sentiment",
            color="Sentiment",
            color_discrete_map={
                "Positive": "#20B486",
                "Negative": "#EF5350",
                "Neutral": "#F5B942"
            }
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        st.subheader("Sentiment Summary")

        for _, row in sentiment_counts.iterrows():

            st.metric(
                row["Sentiment"] + " Feedback",
                int(row["Count"])
            )

    st.subheader("Student Feedback Records")

    st.dataframe(
        sentiment_df[
            ["Student_ID", "Feedback", "Sentiment"]
        ],
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("Please run the NLP analysis module first.")
    # Load trained ML model
model_path = "models/performance_model.pkl"

if os.path.exists(model_path):
    model = joblib.load(model_path)
else:
    model = None

# Load NLP sentiment results
sentiment_path = "data/sentiment_results.csv"

if os.path.exists(sentiment_path):
    sentiment_df = pd.read_csv(sentiment_path)
else:
    sentiment_df = pd.DataFrame()
    # ---------------- FOOTER ----------------
    # ================= AI STUDENT INSIGHTS =================

st.markdown("---")
st.header("🧠 AI-Based Student Insights & Recommendations")

if not filtered_df.empty:

    # Identify weak students
    weak_students = filtered_df[
        (filtered_df["Average"] < 50) |
        (filtered_df["Attendance"] < 60)
    ].copy()

    # Identify low attendance students
    low_attendance = filtered_df[
        filtered_df["Attendance"] < 75
    ].copy()

    # Calculate subject averages
    subjects = [
        "Mathematics",
        "English",
        "Science",
        "Computer",
        "Social_Studies"
    ]

    subject_averages = filtered_df[subjects].mean()

    weakest_subject = subject_averages.idxmin()
    highest_subject = subject_averages.idxmax()

    # Summary cards
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Weak Students",
            len(weak_students)
        )

    with c2:
        st.metric(
            "Low Attendance",
            len(low_attendance)
        )

    with c3:
        st.metric(
            "Students Analysed",
            len(filtered_df)
        )

    st.subheader("📚 Subject Performance Analysis")

    subject_df = subject_averages.reset_index()
    subject_df.columns = ["Subject", "Average Marks"]

    fig = px.bar(
        subject_df,
        x="Subject",
        y="Average Marks",
        color="Average Marks",
        title="Subject-wise Average Performance",
        color_continuous_scale="Purples"
    )

    fig.update_layout(
        yaxis=dict(range=[0, 100]),
        height=350
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # AI recommendations
    st.subheader("💡 AI Recommendations")

    if len(weak_students) > 0:

        st.warning(
            f"{len(weak_students)} students need additional academic support."
        )

    else:
        st.success(
            "No students currently meet the weak-student criteria."
        )

    st.info(
        f"Students need more academic practice in "
        f"{weakest_subject}. Average score: "
        f"{subject_averages[weakest_subject]:.1f}%"
    )

    st.success(
        f"Best performing subject is {highest_subject} "
        f"with an average score of "
        f"{subject_averages[highest_subject]:.1f}%."
    )

    if len(low_attendance) > 0:

        st.warning(
            "Attendance improvement is recommended for "
            f"{len(low_attendance)} students."
        )

    # Weak student details
    st.subheader("⚠️ Students Requiring Attention")

    if not weak_students.empty:

        st.dataframe(
            weak_students[
                [
                    "Student_ID",
                    "Name",
                    "Grade",
                    "Attendance",
                    "Average",
                    "Grade_Result"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No weak students found.")

    # Individual improvement suggestions
    st.subheader("🎯 Individual Student Suggestions")

    if not weak_students.empty:

        selected_student = st.selectbox(
            "Select a student",
            weak_students["Student_ID"].tolist(),
            key="insight_student"
        )

        student = weak_students[
            weak_students["Student_ID"] == selected_student
        ].iloc[0]

        st.markdown(
            f"### {student['Name']}"
        )

        st.write(
            f"**Average Score:** {student['Average']}%"
        )

        st.write(
            f"**Attendance:** {student['Attendance']}%"
        )

        student_weak_subjects = [
            subject for subject in subjects
            if student[subject] < 50
        ]

        if student_weak_subjects:

            st.write(
                "**Subjects requiring improvement:**"
            )

            for subject in student_weak_subjects:

                st.write(
                    f"- {subject}: {student[subject]} marks"
                )

        if student["Attendance"] < 75:

            st.warning(
                "Suggestion: Improve attendance and attend regular classes."
            )

        if student["Average"] < 50:

            st.info(
                "Suggestion: Follow a daily study schedule "
                "and practise previous questions."
            )

        if student_weak_subjects:

            st.success(
                "Suggestion: Give additional attention to "
                + ", ".join(student_weak_subjects)
            )

else:

    st.info("No student data available for analysis.")


# ================= END AI INSIGHTS =================
# ================= STUDENT PROFILE CARDS =================

st.markdown("---")
st.header("👨‍🎓 Student Profiles")

if not filtered_df.empty:

    profile_students = filtered_df.nlargest(
        3, "Average"
    )

    profile_cols = st.columns(3)

    for col, (_, student) in zip(
        profile_cols,
        profile_students.iterrows()
    ):

        with col:

            st.markdown(
                f"""
                <div style="
                    background:white;
                    padding:20px;
                    border-radius:15px;
                    border:1px solid #E6E1F1;
                    text-align:center;
                ">
                    <div style="font-size:35px;">🎓</div>
                    <h4>{student['Name']}</h4>
                    <p style="color:#777;">{student['Student_ID']}</p>
                    <h2 style="color:#673AB7;">
                        {student['Average']:.1f}%
                    </h2>
                    <p>Attendance: {student['Attendance']}%</p>
                    <p>Grade: {student['Grade_Result']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

else:
    st.info("No student profiles available.")


# ================= END STUDENT PROFILES =================
# ================= TOP 5 PERFORMERS =================

st.markdown("---")
st.header("🏆 Top 5 Student Performers")

if not filtered_df.empty:

    top_five = filtered_df.nlargest(5, "Average")

    st.dataframe(
        top_five[
            [
                "Student_ID",
                "Name",
                "Grade",
                "Average",
                "Attendance",
                "Grade_Result"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No student records available.")


# ================= END TOP 5 =================
# ================= DOWNLOAD REPORT =================

st.markdown("---")
st.header("📥 Download Student Report")

if not filtered_df.empty:

    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Student Report (CSV)",
        data=csv_data,
        file_name="student_performance_report.csv",
        mime="text/csv"
    )

else:
    st.info("No data available to download.")

# ================= END DOWNLOAD =================