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
                    ss.interpersonal_skills
                FROM students s  
                join placements p on s.student_id = p.student_id
                join programming pr on s.student_id = pr.student_id
                join soft_skills ss on s.student_id = ss.student_id
                WHERE p.placement_status IN ('Ready', 'Not Ready')
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

st.title("Student Filter")

container = st.container(border=True)
container.text("Filter Students by Placement Status")

filter={}


student_data = get_students_data()

st.dataframe(student_data, use_container_width=True, hide_index=True)