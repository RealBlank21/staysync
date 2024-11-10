import mysql.connector
from mysql.connector import Error

mysql_url = "mysql://root:cldWscwfzqrsQIsVFeEFSIvOPjwhWhfd@junction.proxy.rlwy.net:20548/railway"

try:
    db_config = mysql_url.split("://")[1].split("@")
    user_pass = db_config[0].split(":")
    host_port_db = db_config[1].split("/")
    host_port = host_port_db[0].split(":")

    # Establish connection to the Railway MySQL database
    mydb = mysql.connector.connect(
        host=host_port[0],
        user=user_pass[0],
        password=user_pass[1],
        port=host_port[1],
        database=host_port_db[1]
    )

    print("Database connection successful!")

except Exception as e:
    print(f"Error connecting to the database: {e}")

cursor = mydb.cursor()
cursorDict = mydb.cursor(dictionary=True)

def retrieve_credentials(ic):
    cursorDict.execute("SELECT * FROM admin WHERE admin_ic=%s", (ic,))
    val = cursorDict.fetchone()

    if not val:
        cursorDict.execute("SELECT * FROM warden WHERE warden_ic=%s", (ic,))
        val = cursorDict.fetchone()
    
    return val

def retrieve_role(ic):
    query = """
    SELECT 'admin' AS table_name FROM admin WHERE admin_ic = %s
    UNION
    SELECT 'warden' AS table_name FROM warden WHERE warden_ic = %s
    LIMIT 1;
    """

    cursor.execute(query, (ic, ic))

    result = cursor.fetchone()
    
    if result:
        return result[0].capitalize()  # Returns 'Admin' or 'Warden'
    else:
        return None
    
def retrieve_name(ic):
    query = """
    SELECT name AS table_name FROM admin WHERE admin_ic = %s
    UNION
    SELECT name AS table_name FROM warden WHERE warden_ic = %s
    LIMIT 1;
    """

    cursor.execute(query, (ic, ic))

    result = cursor.fetchone()
    
    if result:
        return result[0]
    else:
        return None
    
def ic_check(IC):
    query = """
    SELECT EXISTS(
        SELECT 1 FROM hostel_application WHERE student_ic = %s
        UNION
        SELECT 1 FROM student WHERE student_ic = %s
    ) AS ic_exists;
    """

    cursor.execute(query, (IC, IC))
    result = cursor.fetchone()

    ic_exists = result[0] == 1

    return ic_exists

def insert_student_admission(student_hostel_application_data : dict):
    try: 
        insert_query = """
        INSERT INTO hostel_application (
            name, student_ic, email, form_class, race, citizenship, family_members, 
            address, home_distance, guardian_status, guardian_contact
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        print(list(student_hostel_application_data.values()))

        cursor.execute(insert_query, list(student_hostel_application_data.values()))

        mydb.commit()

        return "[✔] Hostel Application records inserted successfully!"
    except Error as e:
        return (f"Error: {e}")
    
def update_hostel_application_status(action, ic):
    try:
        query = "UPDATE hostel_application SET status = %s WHERE student_ic = %s"

        print("Changing status...")
        cursor.execute(query, (action, ic))
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

def retrieve_hostel_application_record(IC):
    query = "SELECT * FROM hostel_application WHERE student_ic = %s"
    cursor.execute(query, (IC,))
    record = cursor.fetchone()
    return record