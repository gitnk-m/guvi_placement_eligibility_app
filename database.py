import mysql.connector
from faker import Faker

fake = Faker("en_IN")

dbSetUP = False  # Set to True to create the database and tables

class mySqlDB:
    def __init__(self, host, user, password, port):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            port=port
        )
        self.cursor = self.connection.cursor()

    def create_database(self, db_name):
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        self.connection.commit()
    
    def use_database(self, db_name):
        self.cursor.execute(f"USE {db_name}")
    
    def create_table(self, table_name, columns, constraints=None):
        columns_with_types = ', '.join([f"{col} {dtype}" for col, dtype in columns.items()])
        constraints_sql = ""
        for constraint, details in constraints.items():
            if constraint == "PRIMARY KEY":
                constraints_sql+=f", CONSTRAINT {details[0]} PRIMARY KEY ({details[1]})"
            elif constraint == "FOREIGN KEY":
                constraints_sql+=f", CONSTRAINT {details[0]} FOREIGN KEY ({details[1]}) REFERENCES {details[2]} ON UPDATE CASCADE ON DELETE RESTRICT"
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types} {constraints_sql})")
        self.connection.commit()
        # print(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types} {constraints_sql})")
    
    def insert_data(self, table_name, data):
        columns = ', '.join(data[0].keys())
        values = ', '.join(['%s'] * len(data[0]))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
        values_list = [tuple(item.values()) for item in data]
        self.cursor.executemany(sql, values_list)
        self.connection.commit()
        
    def select_data(self, table_name, columns='*', where=None):
        sql = f"SELECT {columns} FROM {table_name}"
        if where:
            sql += f" WHERE {where}"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def drop_table(self, table_name):
        self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def query(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

db = mySqlDB(
    host="gateway01.us-west-2.prod.aws.tidbcloud.com",
    user="UksibZcFRr6ENhp.root",
    password="4uUKLnlvaMNd1lda",
    port=4000
)

if dbSetUP:
    try:
        # Create and use the database
        db.create_database("placement_app")

        # Use the database
        db.use_database("placement_app")

        # Create the students table
        db.create_table("students", {
            "student_id": "INT",
            "name": "VARCHAR(100)",
            "age": "INT",
            "gender": "VARCHAR(10)",
            "email": "VARCHAR(100)",
            "phone": "VARCHAR(15)",
            "enrollment_year": "YEAR",
            "course_batch": "VARCHAR(50)",
            "city": "VARCHAR(50)",
            "graduation_year": "YEAR"
        }, {
            "PRIMARY KEY": ["pk_student_id", "student_id"],
        })

        # Create Programming table
        db.create_table("programming",{
            "programming_id": "INT",
            "student_id": "INT",
            "language": "VARCHAR(50)",
            "problems_solved": "INT",
            "assessments_completed": "INT",
            "mini_projects": "INT",
            "certifications_earned": "INT",
            "latest_project_score": "FLOAT",
        },{
            "PRIMARY KEY": ["pk_programming_id", "programming_id"],
            "FOREIGN KEY": ["fk_student_id", "student_id", "students(student_id)"]
        })

        # Create the soft skills table
        db.create_table("soft_skills", {
            "soft_skill_id": "INT",
            "student_id": "INT",
            "communication": "FLOAT",
            "teamwork": "FLOAT",
            "presentation": "FLOAT",
            "leadership": "FLOAT",
            "critical_thinking": "FLOAT",
            "interpersonal_skills": "FLOAT",
        }, {
            "PRIMARY KEY": ["pk_soft_skill_id", "soft_skill_id"],
            "FOREIGN KEY": ["fk_student_id", "student_id", "students(student_id)"]
        })

        # Create the placements table
        db.create_table("placements", {
            "placement_id": "INT",
            "student_id": "INT",
            "mock_interview_score": "FLOAT",
            "internships_completed": "INT",
            "placement_status": "VARCHAR(50)",
            "company_name": "VARCHAR(100)",
            "placement_package": "FLOAT",
            "interview_rounds_cleared": "INT",
            "placement_date": "DATE"
        }, {
            "PRIMARY KEY": ["pk_placement_id", "placement_id"],
            "FOREIGN KEY": ["fk_student_id", "student_id", "students(student_id)"]
        })

    # Insert sample data into the students table
        students_data = []
        for i in range(500):
            year = fake.random_int(min=2020, max=2025)
            student = {
                "student_id": i + 1,
                "name": fake.name(),
                "age": fake.random_int(min=18, max=25),
                "gender": fake.random_element(elements=["Male","Female","Other"]),
                "email": fake.email(),
                "phone": fake.phone_number(),
                "enrollment_year": year,
                "course_batch": fake.random_element(elements=["Data Science","Web Development","Digital Marketing"]),
                "city": fake.city(),
                "graduation_year": year+1
                }
            students_data.append(student)  
        db.insert_data("students", students_data)

    # Insert sample data into the programming table
        programming_data = []
        for i in range(500):
            programming = {
                "programming_id": i + 1,
                "student_id": i + 1,
                "language": fake.random_element(elements=["Python", "Java", "C++", "JavaScript", "SQL"]),
                "problems_solved": fake.random_int(min=0, max=500),
                "assessments_completed": fake.random_int(min=0, max=10),
                "mini_projects": fake.random_int(min=0, max=10),
                "certifications_earned": fake.random_int(min=0, max=5),
                "latest_project_score": round(fake.random.uniform(0, 100), 2)
            }
            programming_data.append(programming)
        db.insert_data("programming", programming_data)
        
    # Insert sample data into the soft skills table
        soft_skills_data = []
        for i in range(500):
            soft_skills = {
                "soft_skill_id": i + 1,
                "student_id": i + 1,
                "communication": round(fake.random.uniform(0, 100), 2),
                "teamwork": round(fake.random.uniform(0, 100), 2),
                "presentation": round(fake.random.uniform(0, 100), 2),
                "leadership": round(fake.random.uniform(0, 100), 2),
                "critical_thinking": round(fake.random.uniform(0, 100), 2),
                "interpersonal_skills": round(fake.random.uniform(0, 100), 2)
            }
            soft_skills_data.append(soft_skills)
        db.insert_data("soft_skills", soft_skills_data)

    # Insert sample data into the placements table
        placements_data = []
        for i in range(500):
            placed=fake.random_element(elements=["Ready", "Placed", "Not Ready"])
            placement = {
                "placement_id": i + 1,
                "student_id": i + 1,
                "mock_interview_score": round(fake.random.uniform(0, 100), 2),
                "internships_completed": fake.random_int(min=0, max=5),
                "placement_status": placed,
                "company_name": fake.company() if placed == "Placed" else None,
                "placement_package": round(fake.random.uniform(3, 20), 2) if placed == "Placed" else None,
                "interview_rounds_cleared": fake.random_int(min=1, max=5) if placed == "Placed" else None,
                "placement_date": fake.date_between(start_date='-2y', end_date='today') if placed == "Placed" else None
            }
            placements_data.append(placement)
        db.insert_data("placements", placements_data)
    except(mysql.connector.Error, mysql.connector.Warning) as e:
        print(f"An error occurred: {e}")
        db.connection.rollback()
    finally:
        db.close()
        print("Database operations completed.")

# db.query("SELECT co* FROM placements")