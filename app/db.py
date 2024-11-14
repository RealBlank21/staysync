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

def retrieve_mail(ic):
    # Query to search for email in the warden table
    query_warden = "SELECT email FROM warden WHERE warden_ic = %s"
    cursor.execute(query_warden, (ic,))
    result = cursor.fetchone()

    if result:
        return result[0]  # Return the email if found in warden

    # Query to search for email in the admin table if not found in warden
    query_admin = "SELECT email FROM admin WHERE admin_ic = %s"
    cursor.execute(query_admin, (ic,))
    result = cursor.fetchone()

    if result:
        return result[0]  # Return the email if found in admin

    return None  # Return None if email not found in either table

def get_user_by_email(user_email):
    query = """
    SELECT 'warden' AS role, name, warden_ic AS ic FROM warden WHERE email = %s
    UNION
    SELECT 'admin' AS role, name, admin_ic AS ic FROM admin WHERE email = %s
    """
    
    cursorDict.execute(query, (user_email, user_email))
    user = cursorDict.fetchone()  # Fetch one result (None if not found)
    
    return user

def retrieve_admin(ic):
    cursorDict.execute("SELECT * FROM admin WHERE admin_ic = %s", (ic,))
    val = cursorDict.fetchone()

    return val

def retrieve_warden(ic):
    cursorDict.execute("SELECT * FROM warden WHERE warden_ic = %s", (ic,))
    val = cursorDict.fetchone()

    return val

def retrieve_student(ic):
    cursorDict.execute("SELECT * FROM student WHERE student_ic = %s", (ic,))
    val = cursorDict.fetchone()

    return val

def retrieve_hostel_application(ic):
    cursorDict.execute("SELECT * FROM hostel_application WHERE student_ic = %s", (ic,))
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
            name, student_ic, email, gender, form_class, race, citizenship, family_members, 
            address, home_distance, guardian_status, guardian_contact
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

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
    
def save_pdf_to_db(ic, pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf_data = f.read()

    # Insert the PDF data into the database
    query = "INSERT INTO hostel_applications (student_email, pdf_data) VALUES (%s, %s)"
    cursor.execute(query, (ic, pdf_data))

def insert_student_data(data):
    # Remove the 'status' field from the data
    try:
        if 'status' in data:
            del data['status']

        columns = ', '.join(data.keys())  # Column names
        values = ', '.join(['%s'] * len(data))  # Placeholders for values

        insert_query = f"INSERT INTO student ({columns}) VALUES ({values})"

        cursor.execute(insert_query, tuple(data.values()))

        mydb.commit()

        return "Student data inserted successfully."

    except mysql.connector.Error as err:
        return "Error: {err}"
    
def update_admin_data(data):
    admin_ic = data.get('admin_ic')
    if not admin_ic:
        raise ValueError("admin_ic is required to update admin data.")

    update_fields = ", ".join(f"{key} = %s" for key in data.keys() if key != "admin_ic")
    sql = f"UPDATE admin SET {update_fields} WHERE admin_ic = %s"
    values = tuple(data[key] for key in data if key != "admin_ic") + (admin_ic,)

    try:
        # Execute the update query
        cursor.execute(sql, values)
        mydb.commit()
        print("Admin data updated successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()

    
def update_warden_data(data):
    warden_ic = data.get('warden_ic')
    if not warden_ic:
        raise ValueError("warden_ic is required to update warden data.")

    update_fields = ", ".join(f"{key} = %s" for key in data.keys() if key != "warden_ic")
    sql = f"UPDATE warden SET {update_fields} WHERE warden_ic = %s"
    values = tuple(data[key] for key in data if key != "warden_ic") + (warden_ic,)

    try:
        # Execute the update query
        cursor.execute(sql, values)
        mydb.commit()
        print("Warden data updated successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()
    
def update_student_data(data):
    student_ic = data.get('student_ic')
    if not student_ic:
        raise ValueError("student_ic is required to update student data.")

    update_fields = ", ".join(f"{key} = %s" for key in data.keys() if key != "student_ic")
    sql = f"UPDATE student SET {update_fields} WHERE student_ic = %s"
    values = tuple(data[key] for key in data if key != "student_ic") + (student_ic,)

    try:
        # Execute the update query
        cursor.execute(sql, values)
        mydb.commit()
        print("Student data updated successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()


def retrieve_table_dict(tableName):
    try:
        query = f"SELECT * FROM {tableName}"
        cursorDict.execute(query)
        entries = cursorDict.fetchall()
        return entries
    except mysql.connector.Error as e:
        return f"Error: {e}"
    
def retrieve_confiscated_item_log():
    try:
        query = '''
        SELECT 
            ci.confiscated_item_id,
            ci.item_name,
            ci.student_ic,
            s.name AS student_name,
            ci.item_description,
            ci.confiscation_date,
            ci.confiscater_warden_ic,
            w.name AS warden_name,
            ci.item_status,
            ci.confiscation_reason,
            ci.return_date,
            ci.notes
        FROM 
            confiscated_items ci
        JOIN 
            student s ON ci.student_ic = s.student_ic
        JOIN 
            warden w ON ci.confiscater_warden_ic = w.warden_ic
        '''
        cursorDict.execute(query)

        entries = cursorDict.fetchall()
        return entries
    except mysql.connector.Error as e:
        return f"Error: {e}"
    
def insert_confiscated_item(data):
    insert_query = """
    INSERT INTO confiscated_items (
        item_name, student_ic, item_description, confiscation_date, 
        confiscater_warden_ic, item_status, confiscation_reason, return_date, notes
    ) VALUES (%s, %s, %s, CURDATE(), %s, 'Confiscated', %s, NULL, %s);
    """

    # Values to insert (order should match the placeholders in the query)
    values = (
        data['item_name'],
        data['student_ic'],
        data['item_description'],
        data['confiscater_warden_ic'],
        data['confiscation_reason'],
        data['note']
    )

    # Execute the query and commit the changes
    cursor.execute(insert_query, values)
    mydb.commit()

    return "[✔] Confiscated item inserted successfully!"

def update_confiscated_item_status(action, id):
    try:
        query = "UPDATE confiscated_items SET item_status = %s WHERE confiscated_item_id = %s"

        print("Changing status...")
        cursor.execute(query, (action, id))
        mydb.commit()
    except Error as e:
        return (f"Error: {e}")

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