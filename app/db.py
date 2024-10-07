import mysql.connector
from mysql.connector import Error

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='stay_sync'
)

cursor = mydb.cursor()
cursorDict = mydb.cursor(dictionary=True)

def retrieve_credentials(username):
    cursor.execute("SELECT * FROM user_credentials WHERE username=%s", (username,))

    val = cursor.fetchone()
    
    return val

def retrieve_role(username):
    cursor.execute("SELECT * FROM user_credentials WHERE username=%s", (username,))

    val = cursor.fetchone()
    
    return val[3]

def insert_student_admission(student_hostel_application_data : dict):
    try: 
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

        cursor.execute(insert_query, list(student_hostel_application_data.values()))

        mydb.commit()

        return "Student admission record inserted successfully!"
    except Error as e:
        return (f"Error: {e}")
    
def retrieve_student_admissions():
    try:
        cursorDict.execute("SELECT * FROM hostel_applications")
        entries = cursorDict.fetchall()
        return entries
    except Error as e:
        return (f"Error: {e}")
    
def hostel_application_action(action, entryIndex):
    try:
        query = "UPDATE hostel_applications SET applicationStatus = %s WHERE ID = %s"

        cursor.execute(query, (action, entryIndex))
        mydb.commit()
    except Error as e:
        return (f"Error: {e}")