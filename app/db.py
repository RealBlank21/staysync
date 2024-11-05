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
    
    return val[4]

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
    
def hostel_application_action(action, entryIndex):
    try:
        query = "UPDATE hostel_applications SET applicationStatus = %s WHERE ID = %s"

        cursor.execute(query, (action, entryIndex))
        mydb.commit()
    except Error as e:
        return (f"Error: {e}")

def retrieve_table_dict(tableName):
    try:
        query = f"SELECT * FROM {tableName}"
        cursorDict.execute(query)
        entries = cursorDict.fetchall()
        return entries
    except mysql.connector.Error as e:
        return f"Error: {e}"
    
def retrived_table_joined():
    try:
        fetch_confiscated_items_query = """
        SELECT ci.*, s.studentName 
        FROM confiscated_items ci
        JOIN students s ON ci.studentID = s.studentID
        """
        cursorDict.execute(fetch_confiscated_items_query)

        entries = cursorDict.fetchall()
        return entries
    except mysql.connector.Error as e:
        return f"Error: {e}"
    

def update_ban_period(student_id, outing_datetime):
    cursor.execute('''
        UPDATE student_outing_placeholder
        SET banPeriod = %s
        WHERE studentID = %s
    ''', (outing_datetime, student_id))
    mydb.commit()