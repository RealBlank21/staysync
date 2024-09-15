import mysql.connector
import argon2
import os

with open("PEPPER.txt", 'r') as file:
    PEPPER = file.read().strip()

# Function to hash passwords with Argon2, salt, and pepper
def hash_password(password):
    # Create a new salt
    salt = os.urandom(16)
    # Hash the password with salt and pepper
    ph = argon2.PasswordHasher()
    hashed_password = ph.hash(password + PEPPER)
    return hashed_password

# Connect to MySQL and create the database and table
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password=''
)

cursor = mydb.cursor()

# Drop the database if it already exists and create a new one
cursor.execute("DROP DATABASE IF EXISTS stay_sync")
print("Database dropped successfully.")

cursor.execute("CREATE DATABASE stay_sync")
print("Database created successfully.")

# Use the newly created database
cursor.execute("USE stay_sync")

# Create the user_credentials table
cursor.execute("""
    CREATE TABLE user_credentials (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(100) NOT NULL
    )
""")
print("Table created successfully.")

# Insert credentials into the user_credentials table
users = [
    ('Admin', hash_password('Admin'), 'Admin'),
    ('Warden', hash_password('Warden'), 'Warden'),
    ('Student', hash_password('Student'), 'Student')
]

# Insert the user data
cursor.executemany("""
    INSERT INTO user_credentials (username, password, role)
    VALUES (%s, %s, %s)
""", users)

create_table_query = """
CREATE TABLE hostel_admissions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    gender ENUM('Male', 'Female') NOT NULL,
    student_id VARCHAR(50) NOT NULL,
    student_ic VARCHAR(50) NOT NULL,
    dob DATE NOT NULL,
    phone_self VARCHAR(15) NOT NULL,
    phone_guardian VARCHAR(15) NOT NULL,
    email VARCHAR(100) NOT NULL,
    address_line_1 VARCHAR(255) NOT NULL,
    address_line_2 VARCHAR(255),
    area VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,
    medical_condition_1 VARCHAR(255),
    medical_condition_2 VARCHAR(255),
    medical_condition_3 VARCHAR(255),
    status ENUM('Approve', 'Rejected', 'Pending') NOT NULL DEFAULT 'Pending'
)
"""

cursor.execute(create_table_query)

# Define the values to be inserted (these are placeholder values)
full_name = "MUHAMMAD ADLI BIN NAZLI"
gender = "Male"
student_id = "32DDT22F1030"
student_ic = "041121070023"
dob = "2004-11-21"
phone_self = "01159568937"
phone_guardian = "0124067929"
email = "realblank21@gmail.com"
address_line_1 = "24 Lorong Bendahara 13"
address_line_2 = ""
area = "Bertam Perdana 2"
city = "Kepala Batas"
state = "Pulau Pinang"
zip_code = "13200"
medical_condition_1 = "Asthma"
medical_condition_2 = "None"
medical_condition_3 = "None"
status = "Pending"  # Can be 'Approve', 'Rejected', or 'Pending'

# SQL query to insert values into the table
insert_query = """
INSERT INTO hostel_admissions (full_name, gender, student_id, student_ic, dob, phone_self, phone_guardian, email, address_line_1, address_line_2, area, city, state, zip_code, medical_condition_1, medical_condition_2, medical_condition_3, status)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Execute the query with the placeholder values
cursor.execute(insert_query, (full_name, gender, student_id, student_ic, dob, phone_self, phone_guardian, email, 
                              address_line_1, address_line_2, area, city, state, zip_code, 
                              medical_condition_1, medical_condition_2, medical_condition_3, status))

# Commit the transaction
mydb.commit()

# Close the cursor and connection
cursor.close()
mydb.close()

print("User credentials inserted and database setup completed successfully.")
