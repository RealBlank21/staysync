import mysql.connector
import argon2
import os

with open("PEPPER.txt", 'r') as file:
    PEPPER = file.read().strip()

def hash_password(password):
    salt = os.urandom(16)
    ph = argon2.PasswordHasher()
    hashed_password = ph.hash(password + PEPPER)
    return hashed_password

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password=''
)

cursor = mydb.cursor()

cursor.execute("DROP DATABASE IF EXISTS stay_sync")
print("Database dropped successfully.")

cursor.execute("CREATE DATABASE stay_sync")
print("Database created successfully.")

cursor.execute("USE stay_sync")

cursor.execute("""
    CREATE TABLE user_credentials (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(100) NOT NULL
    )
""")
print("Table created successfully.")

users = [
    ('Admin', hash_password('Admin'), 'Admin'),
    ('Warden', hash_password('Warden'), 'Warden'),
    ('Student', hash_password('Student'), 'Student')
]

cursor.executemany("""
    INSERT INTO user_credentials (username, password, role)
    VALUES (%s, %s, %s)
""", users)

create_table_query = """
CREATE TABLE IF NOT EXISTS hostel_applications (
    ID INT AUTO_INCREMENT PRIMARY KEY,
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
    sportsRepresenting VARCHAR(255),
    applicationStatus VARCHAR(50) DEFAULT 'Pending'
);
"""

cursor.execute(create_table_query)

placeholder_values = [(
    "MUHAMMAD ADLI BIN NAZLI", "041121070023", "4 Alhaitham", "Science", "Malay", 4, 2, 1, 1, 5.0, "Active", "Living with guardian", "Good", 
    "For better education", "Mr. Kaveh", "987654321098", "Malaysian", "123 Akademiya Street", "123-456789", "987-654321", 
    "Engineer", 5000.00, "Akademiya Corporation", "Mrs. Chiori", "876543210987", "Malaysian", "123 Akademiya Street", "123-456789", 
    "987-654321", "Teacher", 3000.00, "SMKA Sumeru", "A", "B", "C", "D", True, False, True, "Scout", "Leader", 
    "National Level", "Science Club", "President", "International Science Fair", "Football", "Captain", "State Level"
),
(
    "NUR AIN BINTI ABDULLAH", "041121070045", "3 Tighnari", "Commerce", "Malay", 3, 3, 2, 1, 4.8, "Active", "Living with parents", "Excellent", 
    "Scholarship opportunity", "Mr. Tighnari", "987654321199", "Malaysian", "456 Mawar Avenue", "111-222333", "999-888777", 
    "Doctor", 8000.00, "Mawar Clinic", "Mrs. Layla", "876543210888", "Malaysian", "456 Mawar Avenue", "111-222333", 
    "999-888777", "Nurse", 3500.00, "Mawar Clinic", "A", "A", "B", "C", True, True, False, "Debate", "Member", 
    "State Level", "Drama Club", "Vice President", "State Drama Competition", "Badminton", "Player", "District Level"
),
(
    "AHMAD BIN SULAIMAN", "041121070067", "2 Cyno", "Arts", "Malay", 2, 2, 1, 2, 4.2, "Active", "Living with guardian", "Fair", 
    "Better facilities", "Mr. Alhaitham", "987654321222", "Malaysian", "789 Sakura Road", "333-444555", "111-222333", 
    "Architect", 6500.00, "Sakura Designs", "Mrs. Nilou", "876543210666", "Malaysian", "789 Sakura Road", "333-444555", 
    "111-222333", "Interior Designer", 4000.00, "Sakura Designs", "B", "B", "C", "D", False, True, True, "Art", "Secretary", 
    "National Level", "Music Club", "Member", "National Art Exhibition", "Basketball", "Player", "National Level"
),
(
    "SITI FATIMAH BINTI HARIS", "041121070089", "1 Dehya", "Humanities", "Malay", 1, 1, 1, 1, 4.9, "Active", "Living with parents", "Good", 
    "Closer to home", "Mr. Nahida", "987654321333", "Malaysian", "111 Jasmine Lane", "777-888999", "444-555666", 
    "Lawyer", 9000.00, "Jasmine Law Firm", "Mrs. Niloufar", "876543210555", "Malaysian", "111 Jasmine Lane", "777-888999", 
    "444-555666", "Lecturer", 6000.00, "National University", "A", "B", "A", "B", True, False, False, "Chess", "Member", 
    "International Level", "Philosophy Club", "President", "National Debate Championship", "Tennis", "Player", "National Level"
),
(
    "FAIZ BIN RAZAK", "041121070121", "5 Collei", "Science", "Malay", 5, 3, 2, 1, 4.7, "Active", "Living with guardian", "Excellent", 
    "Better science labs", "Mr. Cyno", "987654321444", "Malaysian", "321 Moonlight Drive", "999-111222", "888-777666", 
    "Engineer", 7000.00, "Moonlight Engineering", "Mrs. Rosaria", "876543210444", "Malaysian", "321 Moonlight Drive", "999-111222", 
    "888-777666", "Accountant", 3500.00, "Moonlight Engineering", "B", "C", "B", "A", False, True, True, "Robotics", "Member", 
    "State Level", "Science Club", "President", "National Robotics Championship", "Swimming", "Captain", "State Level"
),
(
    "AISHA BINTI HAMZAH", "041121070143", "3 Yae", "Commerce", "Malay", 3, 2, 1, 2, 4.5, "Active", "Living with parents", "Fair", 
    "School reputation", "Mr. Ayato", "987654321555", "Malaysian", "654 Rose Garden", "222-333444", "555-666777", 
    "Businessman", 8000.00, "Rose Enterprises", "Mrs. Ei", "876543210333", "Malaysian", "654 Rose Garden", "222-333444", 
    "555-666777", "Bank Manager", 4500.00, "Rose Bank", "A", "A", "C", "B", True, False, True, "Business", "Member", 
    "National Level", "Economics Club", "Vice President", "National Business Competition", "Netball", "Player", "State Level"
),
(
    "ZAIN BIN FARHAN", "041121070165", "4 Tighnari", "Arts", "Malay", 4, 3, 2, 1, 4.3, "Active", "Living with guardian", "Good", 
    "Improved arts program", "Mr. Kaveh", "987654321666", "Malaysian", "987 Pine Street", "444-555666", "777-888999", 
    "Artist", 5000.00, "Pine Arts Studio", "Mrs. Collei", "876543210222", "Malaysian", "987 Pine Street", "444-555666", 
    "777-888999", "Art Teacher", 3000.00, "Pine Arts School", "C", "C", "A", "B", True, True, False, "Painting", "Leader", 
    "National Level", "Art Club", "Member", "National Art Festival", "Tennis", "Player", "District Level"
)]


insert_query = """
INSERT INTO hostel_applications (
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

cursor.executemany(insert_query, placeholder_values)

mydb.commit()

cursor.close()
mydb.close()

print("User credentials inserted and database setup completed successfully.")
