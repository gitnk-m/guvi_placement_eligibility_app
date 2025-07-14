import streamlit as st
import pandas as pd
from database import mySqlDB
import altair as alt

class insight_obj:
    def __init__(self):
        pass

    def simple_bar_chart(self, query, title, legend, column):
        pip 
        placement_df = data.set_index(legend)
        with column:
            st.text(title)
            st.bar_chart(placement_df)

    def altair_bar_chart(self,query, title, x_axis, x_label, y_axis, y_label, legend, legend_title, tooltip):
        data = pd.read_sql(query, db.connection)
        
        df_melted = data.melt(id_vars=x_axis, 
                    value_vars=legend,
                    var_name=y_axis, value_name=y_label)
        
        # Create grouped bar chart
        chart = alt.Chart(df_melted).mark_bar().encode(
            x=alt.X(f'{x_axis}:N', title=x_label, sort=None),
            y=alt.Y(f'{y_label}:Q'),
            color=alt.Color(f'{y_axis}:N', legend=alt.Legend(title=legend_title)),
            tooltip=tooltip
        ).properties(
            width=600,
            height=400,
            title=title
        )

        st.altair_chart(chart, use_container_width=True)

    def display_table(self, query, title):
        # data = pd.read_sql(query, db.connection)
        st.text(f"Showing {title}")
        st.dataframe(pd.read_sql(query, db.connection), use_container_width=True, hide_index=True)

db = mySqlDB(
    host="gateway01.us-west-2.prod.aws.tidbcloud.com",
    user="UksibZcFRr6ENhp.root",
    password="4uUKLnlvaMNd1lda",
    port=4000
)
st.subheader("Insight Page")
# Use the database
db.use_database("placement_app")

# Columns for displaying different data
col1, col2, col3 = st.columns([2,1,2])

# calling the insight_obj class
insight=insight_obj()

# Displaying the number of students in each placement status
insight.simple_bar_chart('''
                         SELECT 
                            placement_status AS status, 
                            count(*) AS count 
                         FROM placements 
                         WHERE placement_status IN ('Ready','Not Ready','Placed') 
                         GROUP BY placement_status''', 
                         "Placement Status", "status", col1)

# Displaying the number of students in each language selection
insight.simple_bar_chart('''
                         SELECT 
                            language AS programming_language, 
                            count(*) AS count 
                         FROM programming 
                         WHERE language IN ('C++','Java','JavaScript','Python','SQL') 
                         GROUP BY language''', 
                         "Programming Languages", "programming_language", col3)

# Displaying the top 10 students based on submission of assessments, projects, and certifications
insight.altair_bar_chart('''
                            SELECT 
                                s.name AS Name,
                                p.assessments_completed AS assessments,
                                p.mini_projects AS mini_projects,
                                p.certifications_earned AS certifications
                            FROM programming p
                            JOIN students s ON s.student_id = p.student_id
                            ORDER BY (p.assessments_completed + p.mini_projects + p.certifications_earned) / 25.0 DESC
                            LIMIT 10;''',
                            "Top Students with submission of Assessments, Projects, and Certifications",
                            "Name", "Students", "Category", "Submissions", 
                            ["assessments", "mini_projects", "certifications"], 
                            "Metric", ['Name', 'Category', 'Submissions'])

# Displaying Tables
table_title = {
    "problem_solved_data":{
        "title":"Top 10 Students Based on Problems Solved",
        "query":'''SELECT 
                                    s.name, 
                                    s.email, 
                                    s.course_batch, 
                                    p.language, 
                                    p.problems_solved 
                                FROM students s 
                                JOIN programming p 
                                ON s.student_id = p.student_id 
                                order by p.problems_solved DESC 
                                limit 10''',
        },
    "mock_interview_data":{
        "title":"Top 10 Students Ready to Palcement Based on Mock Interview Scores",
        "query":'''select 
                    s.name,
                    s.email,
                    s.course_batch,
                    p.mock_interview_score
                from students s
                join placements p ON s.student_id = p.student_id
                where p.placement_status IN ('Ready')
                order by p.mock_interview_score DESC
                limit 10;''',
        },
    "package_data":{
        "title":"Top 10 Students Placed and Their Packages",
        "query":'''select 
                        s.name as Name,
                        s.course_batch as Course,
                        p.placement_date as Placement_Date,
                        p.company_name as Company_Name,
                        p.placement_package as Package
                    from students s
                    join placements p ON s.student_id = p.student_id
                    order by p.placement_package DESC
                    limit 10;''',
        },
    "latest_project_data":{
        "title":"Top 10 Students with High Score on Latest Project",
        "query":'''select 
                        s.name as Name,
                        s.course_batch as Course,
                        p.language as Language,
                        p.latest_project_score as Latest_Project_Score
                    from students s
                    join programming p ON s.student_id = p.student_id
                    order by p.latest_project_score DESC
                    limit 10;''',
        },
    "soft_skills_data":{
            "title":"Top 10 Students with High Average Soft Skills",
            "query":'''select 
                            s.name as Name,
                            s.course_batch as Course,
                            (soft.communication + soft.teamwork + soft.presentation + soft.leadership + soft.critical_thinking + soft.interpersonal_skills) / 6 as Average_Soft_Skills
                        from students s
                        join soft_skills soft ON s.student_id = soft.student_id
                        order by Average_Soft_Skills DESC
                        limit 10;''',
        },
    "studetns_placed_soft_skills_data":{
        "title":"Top 10 Students Placed with Soft Skills",
        "query":'''select 
                        s.name as Name,
                        s.course_batch as Course,
                        p.placement_date as Placement_Date,
                        p.company_name as Company_Name,
                        p.placement_package as Package,
                        (soft.communication + soft.teamwork + soft.presentation + soft.leadership + soft.critical_thinking + soft.interpersonal_skills) / 6 as Average_Soft_Skills
                    from students s
                    join placements p ON s.student_id = p.student_id
                    join soft_skills soft ON s.student_id = soft.student_id
                    where p.placement_status = 'Placed'
                    order by Average_Soft_Skills DESC
                    limit 10;''',
        },
    "students_course_data":{
        "title":"Top Courses Students Got Placed",
        "query":'''select 
                        s.course_batch as Course,
                        count(*) as Students_Placed
                    from students s
                    join placements p ON s.student_id = p.student_id
                    where p.placement_status = 'Placed'
                    group by s.course_batch
                    order by Students_Placed DESC;''',
        }
}
# Selectbox for table selection
table_selected = st.selectbox(
    "Select Table to View",
    options=list(table_title.keys()),
    format_func=lambda x: table_title[x]["title"] if x in table_title else "Select a table"
)

if table_selected:
    insight.display_table(table_title[table_selected]["query"], table_title[table_selected]["title"])