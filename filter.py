import streamlit as st
import pandas as pd
from database import mySqlDB

# Function to get students data
def get_students_data():
    query = f'''SELECT
                    s.name,
                    s.phone,
                    s.email,
                    s.course_batch,
                    pr.language,
                    p.placement_status,
                    s.graduation_year,
                    p.mock_interview_score,
                    p.internships_completed,
                    pr.problems_solved,
                    pr.assessments_completed,
                    pr.mini_projects,
                    pr.certifications_earned,
                    pr.latest_project_score,
                    ss.communication,
                    ss.teamwork,
                    ss.presentation,
                    ss.leadership,
                    ss.critical_thinking,
                    ss.interpersonal_skills,
                    p.company_name,
                    p.placement_package
                FROM students s  
                join placements p on s.student_id = p.student_id
                join programming pr on s.student_id = pr.student_id
                join soft_skills ss on s.student_id = ss.student_id
                ORDER BY s.name;'''
    data = pd.read_sql(query, db.connection)
    return data

# Database connection
db = mySqlDB(
    host="gateway01.us-west-2.prod.aws.tidbcloud.com",
    user="UksibZcFRr6ENhp.root",
    password="4uUKLnlvaMNd1lda",
    port=4000
)
# Use the database
db.use_database("placement_app")

# Title
st.text("Student Placement Track Data")

# Topbar for filtering options
options = ["Placed", "Not Ready", "Ready"]
with st.container( border=True):
    col1, col2 = st.columns(2)
    with col1:
        selected_options = st.pills("Select Placement Status", options, selection_mode="multi")
        problem_solved = st.number_input(
            "Minimum Problems Solved",
            min_value=0,
            max_value=500)
    with col2:   
        mock_interview_score = st.number_input(
            "Minimum Mock Interview Score",
            min_value=0,
            max_value=100)
        intenship_completed = st.number_input(
            "Minimum Internships Completed",
            min_value=0,
            max_value=5)

# Filter data based on user input
filter={
    "placement_status": selected_options if selected_options else ["Placed", "Not Ready", "Ready"],
    "mock_interview_score": mock_interview_score if mock_interview_score else 0,
    "internships_completed": intenship_completed if intenship_completed else 0,
    "problems_solved": problem_solved if problem_solved else 0
}

#fetching Students data
student_data = get_students_data()

# Filter the data based on user input using pandas
filter_data = student_data[student_data["placement_status"].isin(filter["placement_status"]) & 
                            (student_data["mock_interview_score"] >= filter["mock_interview_score"]) & 
                            (student_data["internships_completed"] >= filter["internships_completed"]) & 
                            (student_data["problems_solved"] >= filter["problems_solved"])]

# Display the filtered data
st.dataframe(filter_data, use_container_width=True, hide_index=True)