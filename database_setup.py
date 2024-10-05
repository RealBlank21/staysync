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
CREATE TABLE IF NOT EXISTS students (
    studentName VARCHAR(255),
    studentIc VARCHAR(255),
    formClass VARCHAR(50),
    stream VARCHAR(50),
    race VARCHAR(50),
    familyMembers INT,
    familyStudying INT,
    siblingsSPBT INT,
    siblingsHostel INT,
    distance FLOAT,
    studentStatus VARCHAR(50),
    guardianStatus VARCHAR(50),
    healthStatus VARCHAR(255),
    hostelReason VARCHAR(255),
    fatherGuardianName VARCHAR(255),
    fatherGuardianIc VARCHAR(255),
    fatherCitizenship VARCHAR(50),
    fatherGuardianAddress VARCHAR(255),
    fatherPhoneHome VARCHAR(50),
    fatherPhoneMobile VARCHAR(50),
    fatherOccupation VARCHAR(100),
    fatherIncome FLOAT,
    fatherEmployerAddress VARCHAR(255),
    motherGuardianName VARCHAR(255),
    motherGuardianIc VARCHAR(255),
    motherCitizenship VARCHAR(50),
    motherGuardianAddress VARCHAR(255),
    motherPhoneHome VARCHAR(50),
    motherPhoneMobile VARCHAR(50),
    motherOccupation VARCHAR(100),
    motherIncome FLOAT,
    motherEmployerAddress VARCHAR(255),
    upsrResults VARCHAR(50),
    pmrResults VARCHAR(50),
    spmResults VARCHAR(50),
    latestExamResults VARCHAR(50),
    spbt BOOLEAN,
    scholarship BOOLEAN,
    kwapm BOOLEAN,
    uniformedUnit VARCHAR(100),
    uniformedUnitPosition VARCHAR(100),
    uniformedUnitRepresenting VARCHAR(255),
    clubAssociation VARCHAR(100),
    clubPosition VARCHAR(100),
    clubRepresenting VARCHAR(255),
    sportsGames VARCHAR(100),
    sportsPosition VARCHAR(100),
    sportsRepresenting VARCHAR(255)
);
"""

cursor.execute(create_table_query)

# Define the values to be inserted (these are placeholder values)
placeholder_values = (
    "John Doe", "123456789012", "Form 4", "Science", "Malay", 4, 2, 1, 1, 5.0, "Active", "Living with guardian", "Good", 
    "For better education", "Mr. Doe", "987654321098", "Malaysian", "123 Doe Street", "123-456789", "987-654321", 
    "Engineer", 5000.00, "Doe Corporation", "Mrs. Doe", "876543210987", "Malaysian", "123 Doe Street", "123-456789", 
    "987-654321", "Teacher", 3000.00, "School Name", "A", "B", "C", "D", True, False, True, "Scout", "Leader", 
    "National Level", "Science Club", "President", "International Science Fair", "Football", "Captain", "State Level"
)

# SQL query to insert values into the table (no duplicate columns)
insert_query = """
INSERT INTO students (
    studentName, studentIc, formClass, stream, race, familyMembers, familyStudying, siblingsSPBT, siblingsHostel, 
    distance, studentStatus, guardianStatus, healthStatus, hostelReason, fatherGuardianName, fatherGuardianIc, 
    fatherCitizenship, fatherGuardianAddress, fatherPhoneHome, fatherPhoneMobile, fatherOccupation, fatherIncome, 
    fatherEmployerAddress, motherGuardianName, motherGuardianIc, motherCitizenship, motherGuardianAddress, 
    motherPhoneHome, motherPhoneMobile, motherOccupation, motherIncome, motherEmployerAddress, upsrResults, pmrResults, 
    spmResults, latestExamResults, spbt, scholarship, kwapm, uniformedUnit, uniformedUnitPosition, 
    uniformedUnitRepresenting, clubAssociation, clubPosition, clubRepresenting, sportsGames, sportsPosition, sportsRepresenting
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
);
"""

# Execute the query with the placeholder values
cursor.execute(insert_query, placeholder_values)

# Commit the transaction
mydb.commit()

# Close the cursor and connection
cursor.close()
mydb.close()

print("User credentials inserted and database setup completed successfully.")
