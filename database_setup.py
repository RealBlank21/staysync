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
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(255) UNIQUE,
        email VARCHAR(255),
        password VARCHAR(255),
        user_role ENUM('Admin', 'Warden', 'Student')
    );
""")
print("Table created successfully.")

users = [
    ('Admin', "realblanket21@gmail.com" ,hash_password('Admin'), 'Admin'),
    ('Warden', "realblanket21@gmail.com" ,hash_password('Warden'), 'Warden'),
    ('Student', "realblanket21@gmail.com" ,hash_password('Student'), 'Student')
]

cursor.executemany("""
    INSERT INTO user_credentials (username, email, password, user_role)
    VALUES (%s, %s, %s, %s)
""", users)

create_table_query = """
CREATE TABLE IF NOT EXISTS hostel_applications (
    hostelApplicationID INT AUTO_INCREMENT PRIMARY KEY,
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


create_table_query = '''
CREATE TABLE IF NOT EXISTS student_outing_placeholder (
    studentID INTEGER PRIMARY KEY AUTO_INCREMENT,
    studentName TEXT NOT NULL,
    studentIC TEXT NOT NULL,
    formClass TEXT NOT NULL,
    banPeriod TEXT  -- You can use TEXT to store date ranges or specific dates, or use DATE type if available
);
'''

cursor.execute(create_table_query)

students = [
    ('Ahmad Firdaus', '990101-14-1234', 'Form 5A', ''),
    ('Siti Zulaikha', '970404-12-7890', 'Form 5C', ''),
    ('Aisyah Hasan', '951212-07-1234', 'Form 6B', ''),
    ('Muhammad Izzat', '940606-08-7654', 'Form 6A', ''),
    ('Nurul Iman', '980808-10-4321', 'Form 4A', '')
]

# Insert the data into the table
insert_query = '''
INSERT INTO student_outing_placeholder (studentName, studentIC, formClass, banPeriod)
VALUES (%s, %s, %s, %s);
'''

cursor.executemany(insert_query, students)

mydb.commit()

create_students_table_query = """
CREATE TABLE IF NOT EXISTS students (
    studentID INT AUTO_INCREMENT PRIMARY KEY,
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

cursor.execute(create_students_table_query)

students_data = [
    ('Ahmad Firdaus', '990101-14-1234', 'Form 5A', 'Science', 'Malay', 5, 2, 1, 0, 12.5, 'Active', 'Both Parents', 'Healthy', 
     'Hakim bin Ahmad', '760101-05-1234', 'Malaysian', 'No. 4, Jalan Tun Ismail, Kuala Lumpur', '03-12345678', '012-3456789', 
     'Engineer', 5000, 'KL Tower, Kuala Lumpur', 'Siti Aminah', '770202-10-9876', 'Malaysian', 'No. 4, Jalan Tun Ismail, Kuala Lumpur', 
     '03-87654321', '011-2345678', 'Teacher', 3500, 'School A, KL', '5As', '7As', '9As', 'Top 10', True, True, False, 
     'Scout', 'Leader', 'National', 'Science Club', 'President', 'State', 'Football', 'Captain', 'State'),
    
    ('Siti Zulaikha', '970404-12-7890', 'Form 5C', 'Arts', 'Malay', 6, 3, 1, 2, 15.0, 'Active', 'Both Parents', 'Healthy', 
     'Zul Ariffin', '731212-02-9876', 'Malaysian', 'No. 45, Jalan Sri Hartamas, KL', '03-98765432', '013-1234567', 'Policeman', 
     4000, 'Police HQ, KL', 'Salmah Ahmad', '741010-04-5432', 'Malaysian', 'No. 45, Jalan Sri Hartamas, KL', '03-76543234', 
     '011-2345678', 'Businesswoman', 5000, 'Sri Hartamas, KL', '3As', '5As', '7As', 'Improving', True, False, True, 
     'Girl Guides', 'Vice Leader', 'State', 'Drama Club', 'President', 'National', 'Netball', 'Player', 'District'),
    
    ('Aisyah Hasan', '951212-07-1234', 'Form 6B', 'Commerce', 'Malay', 2, 0, 0, 0, 25.3, 'Active', 'Single Parent', 'Asthma', 
     'Hasan Ali', '701212-09-4321', 'Malaysian', 'No. 90, Jalan Ampang, KL', '03-43210987', '019-1234567', 'Accountant', 
     6000, 'Ampang, KL', 'Nurul Aida', '721010-08-5432', 'Malaysian', 'No. 90, Jalan Ampang, KL', '03-54321098', '012-3456789', 
     'Nurse', 4500, 'Hospital Ampang', '7As', '9As', '10As', 'Excellent', True, False, True, 'Brass Band', 'Member', 'National', 
     'Dance Club', 'Member', 'State', 'Tennis', 'Player', 'District'),
    
    ('Muhammad Izzat', '940606-08-7654', 'Form 6A', 'Science', 'Malay', 4, 1, 1, 1, 20.0, 'Active', 'Both Parents', 'Healthy', 
     'Izzuddin Ahmad', '700101-08-2345', 'Malaysian', 'No. 1, Jalan Gombak, KL', '03-54321098', '014-9876543', 'Lecturer', 
     8000, 'University A, KL', 'Siti Noraini', '720202-05-6789', 'Malaysian', 'No. 1, Jalan Gombak, KL', '03-87654321', 
     '011-2345678', 'Housewife', 0, None, '6As', '8As', '10As', 'Top 5', True, True, False, 'Cadet', 'Leader', 'National', 
     'Debate Club', 'President', 'State', 'Rugby', 'Captain', 'State'),
    
    ('Nurul Iman', '980808-10-4321', 'Form 4A', 'Commerce', 'Malay', 3, 1, 0, 1, 22.1, 'Active', 'Both Parents', 'Healthy', 
     'Zainal Abidin', '740808-07-4321', 'Malaysian', 'No. 2, Jalan Damansara, KL', '03-65432109', '013-2345678', 'Businessman', 
     7000, 'Damansara, KL', 'Siti Khadijah', '750909-08-7654', 'Malaysian', 'No. 2, Jalan Damansara, KL', '03-54321098', 
     '012-8765432', 'Homemaker', 0, None, '4As', '6As', '8As', 'Good', True, False, False, 'Band', 'Vice President', 'District', 
     'Drama Club', 'Secretary', 'State', 'Hockey', 'Player', 'National')
]

insert_query = """
INSERT INTO students (
    studentName, studentIc, formClass, stream, race, familyMembers, familyStudying, siblingsSPBT, siblingsHostel, distance, 
    studentStatus, guardianStatus, healthStatus, fatherGuardianName, fatherGuardianIc, fatherCitizenship, fatherGuardianAddress, 
    fatherPhoneHome, fatherPhoneMobile, fatherOccupation, fatherIncome, fatherEmployerAddress, motherGuardianName, motherGuardianIc, 
    motherCitizenship, motherGuardianAddress, motherPhoneHome, motherPhoneMobile, motherOccupation, motherIncome, motherEmployerAddress, 
    upsrResults, pmrResults, spmResults, latestExamResults, spbt, scholarship, kwapm, uniformedUnit, uniformedUnitPosition, 
    uniformedUnitRepresenting, clubAssociation, clubPosition, clubRepresenting, sportsGames, sportsPosition, sportsRepresenting
) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

cursor.executemany(insert_query, students_data)

mydb.commit()

# Create the table for confiscated items
cursor.execute("""CREATE TABLE IF NOT EXISTS confiscated_items (
                confiscatedItemID INTEGER PRIMARY KEY AUTO_INCREMENT,
                itemName TEXT NOT NULL,
                studentID INTEGER NOT NULL,
                itemDescription TEXT,
                confiscationDate TEXT NOT NULL,
                confiscatedBy TEXT NOT NULL,
                itemStatus TEXT NOT NULL,
                confiscationReason TEXT,
                returnDate TEXT,
                notes TEXT,
                FOREIGN KEY (studentID) REFERENCES students(studentID)
            );""")

# Commit the creation of the table
mydb.commit()

# Example items to be added
confiscated_items_data = [
    ('Handphone', 1, 'Smartphone, brand XYZ', '2024-10-01', 'Warden Ali', 'Confiscated', 'Using during class', None, 'Needs to be returned after 1 month'),
    ('Sharp Object', 2, 'Scissors', '2024-10-02', 'Warden Zainab', 'Confiscated', 'Possession of dangerous item', None, 'To be returned after review'),
    ('Wireless Earbuds', 3, 'Bluetooth earbuds', '2024-10-03', 'Warden Ahmad', 'Confiscated', 'Using during exam', None, 'To be returned after exam'),
    ('Playing Cards', 4, 'Deck of playing cards', '2024-10-04', 'Warden Fatimah', 'Confiscated', 'Playing games in hostel', None, 'To be destroyed'),
    ('Video Game Console', 5, 'Portable gaming console', '2024-10-05', 'Warden Ismail', 'Confiscated', 'Brought to school without permission', None, 'To be returned after a month')
]

insert_confiscated_items_query = """
INSERT INTO confiscated_items (
    itemName, studentID, itemDescription, confiscationDate, confiscatedBy, itemStatus, confiscationReason, returnDate, notes
) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

cursor.executemany(insert_confiscated_items_query, confiscated_items_data)  

# Commit the insertions
mydb.commit()

warden_table = """
CREATE TABLE IF NOT EXISTS warden (
    warden_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone_number VARCHAR(15) NOT NULL,
    address TEXT,
    date_of_birth DATE,
    date_of_joining DATE,
    gender ENUM('Male', 'Female', 'Other')
);
"""

# Create Admin Table
admin_table = """
CREATE TABLE IF NOT EXISTS admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone_number VARCHAR(15) NOT NULL,
    address TEXT,
    date_of_birth DATE,
    date_of_joining DATE,
    gender ENUM('Male', 'Female', 'Other')
);
"""

cursor.execute(warden_table)
cursor.execute(admin_table)

warden_data = """
INSERT INTO warden (name, email, phone_number, address, date_of_birth, date_of_joining, gender)
VALUES
    ('Ahmad Firdaus', 'ahmad.firdaus@example.com', '0123456789', 'No. 12, Jalan Tun Razak, Kuala Lumpur', '1987-04-15', '2016-02-10', 'Male'),
    ('Nur Aisyah', 'nur.aisyah@example.com', '0198765432', 'No. 34, Taman Desa, Petaling Jaya', '1992-07-22', '2017-11-01', 'Female'),
    ('Lee Wei Ming', 'lee.weiming@example.com', '0112345678', 'No. 9, Jalan Bukit Bintang, Kuala Lumpur', '1985-09-10', '2014-09-15', 'Male');
"""

admin_data = """
INSERT INTO admin (name, email, phone_number, address, date_of_birth, date_of_joining, gender)
VALUES
    ('Siti Zulaikha', 'siti.zulaikha@example.com', '0176543210', 'No. 45, Jalan Sri Hartamas, Kuala Lumpur', '1980-12-05', '2011-03-12', 'Female');
"""

cursor.execute(warden_data)
cursor.execute(admin_data)

mydb.commit()

cursor.close()
mydb.close()

print("User credentials inserted and database setup completed successfully.")
