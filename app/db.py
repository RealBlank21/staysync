import mysql.connector
from mysql.connector import Error

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='stay_sync'
)

cursor = mydb.cursor()

def retrieve_credentials(username):
    cursor.execute("SELECT * FROM user_credentials WHERE username=%s", (username,))

    val = cursor.fetchone()
    
    return val

def retrieve_role(username):
    cursor.execute("SELECT * FROM user_credentials WHERE username=%s", (username,))

    val = cursor.fetchone()
    
    return val[3]

def insert_student_admission(id, full_name, gender, student_id, student_ic, dob, phone_self, phone_guardian, email, address_line_1, address_line_2, area, city, state, zip_code, medical_condition_1, medical_condition_2, medical_condition_3, status):
    try: 
        insert_query = """
        INSERT INTO hostel_admissions 
        (id, full_name, gender, student_id, student_ic, dob, phone_self, phone_guardian, email, 
        address_line_1, address_line_2, area, city, state, zip_code, 
        medical_condition_1, medical_condition_2, medical_condition_3, status) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (id, full_name, gender, student_id, student_ic, dob, phone_self, phone_guardian, email,
                                    address_line_1, address_line_2, area, city, state, zip_code, 
                                    medical_condition_1, medical_condition_2, medical_condition_3, status))

        cursor.commit()

        return "Student admission record inserted successfully!"
    except Error as e:
        return (f"Error: {e}")