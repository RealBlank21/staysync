import mysql.connector
from mysql.connector import Error
import os
import argon2

mysql_url = "mysql://root:cldWscwfzqrsQIsVFeEFSIvOPjwhWhfd@junction.proxy.rlwy.net:20548/railway"

# Open and read the PEPPER.txt file
with open("PEPPER.txt", 'r') as file:
    PEPPER = file.read().strip()

def hash_password(password):
    try:
        salt = os.urandom(16)
        ph = argon2.PasswordHasher()
        hashed_password = ph.hash(password + PEPPER)
        return hashed_password
    except Exception as e:
        print(f"Error hashing password: {e}")
        return None

def hash_password(password):
    try:
        salt = os.urandom(16)
        ph = argon2.PasswordHasher()
        hashed_password = ph.hash(password + PEPPER)
        return hashed_password
    except Exception as e:
        print(f"Error hashing password: {e}")
        return None

def connect_db():
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

        return mydb

    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

def retrieve_credentials(ic):
    mydb = connect_db()
    if mydb is None:
        return None

    cursorDict = mydb.cursor(dictionary=True)
    try:
        cursorDict.execute("SELECT * FROM admin WHERE admin_ic=%s", (ic,))
        val = cursorDict.fetchone()

        if not val:
            cursorDict.execute("SELECT * FROM warden WHERE warden_ic=%s", (ic,))
            val = cursorDict.fetchone()

        return val
    finally:
        cursorDict.close()
        mydb.close()

def retrieve_mail(ic):
    mydb = connect_db()
    if mydb is None:
        return None

    cursor = mydb.cursor()
    try:
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
    finally:
        cursor.close()
        mydb.close()

def get_user_by_email(user_email):
    mydb = connect_db()
    if mydb is None:
        return None

    cursorDict = mydb.cursor(dictionary=True)
    try:
        query = """
        SELECT 'warden' AS role, name, warden_ic AS ic FROM warden WHERE email = %s
        UNION
        SELECT 'admin' AS role, name, admin_ic AS ic FROM admin WHERE email = %s
        """
        cursorDict.execute(query, (user_email, user_email))
        user = cursorDict.fetchone()  # Fetch one result (None if not found)

        return user
    finally:
        cursorDict.close()
        mydb.close()

def retrieve_admin(ic):
    mydb = connect_db()
    if mydb is None:
        return None

    cursorDict = mydb.cursor(dictionary=True)
    try:
        cursorDict.execute("SELECT * FROM admin WHERE admin_ic = %s", (ic,))
        val = cursorDict.fetchone()

        return val
    finally:
        cursorDict.close()
        mydb.close()

def retrieve_warden(ic):
    mydb = connect_db()
    if mydb is None:
        return None

    cursorDict = mydb.cursor(dictionary=True)
    try:
        cursorDict.execute("SELECT * FROM warden WHERE warden_ic = %s", (ic,))
        val = cursorDict.fetchone()

        return val
    finally:
        cursorDict.close()
        mydb.close()

def retrieve_student(ic):
    mydb = connect_db()
    if mydb is None:
        return None

    cursorDict = mydb.cursor(dictionary=True)
    try:
        cursorDict.execute("SELECT * FROM student WHERE student_ic = %s", (ic,))
        val = cursorDict.fetchone()

        return val
    finally:
        cursorDict.close()
        mydb.close()

def retrieve_hostel_application(ic):
    mydb = connect_db()
    if mydb is None:
        return None

    cursorDict = mydb.cursor(dictionary=True)
    try:
        cursorDict.execute("SELECT * FROM hostel_application WHERE student_ic = %s", (ic,))
        val = cursorDict.fetchone()

        return val
    finally:
        cursorDict.close()
        mydb.close()

def retrieve_role(ic):
    mydb = connect_db()
    if mydb is None:
        return None

    cursor = mydb.cursor()
    try:
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
    finally:
        cursor.close()
        mydb.close()

def retrieve_name(ic):
    mydb = connect_db()
    if mydb is None:
        return None

    cursor = mydb.cursor()
    try:
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
    finally:
        cursor.close()
        mydb.close()

def ic_check(IC):
    mydb = connect_db()
    if mydb is None:
        return False

    cursor = mydb.cursor()
    try:
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
    finally:
        cursor.close()
        mydb.close()

def insert_student_admission(student_hostel_application_data: dict):
    mydb = connect_db()
    if mydb is None:
        return "Error: Unable to connect to the database."

    cursor = mydb.cursor()
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
        return f"Error: {e}"
    finally:
        cursor.close()
        mydb.close()

def update_hostel_application_status(action, ic):
    mydb = connect_db()
    if mydb is None:
        return "Error: Unable to connect to the database."

    cursor = mydb.cursor()
    try:
        query = "UPDATE hostel_application SET status = %s WHERE student_ic = %s"
        print("Changing status...")
        cursor.execute(query, (action, ic))
        mydb.commit()
    except Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        mydb.close()

def save_pdf_to_db(ic, pdf_path):
    mydb = connect_db()
    if mydb is None:
        return "Error: Unable to connect to the database."

    cursor = mydb.cursor()
    try:
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()

        # Insert the PDF data into the database
        query = "INSERT INTO hostel_applications (student_email, pdf_data) VALUES (%s, %s)"
        cursor.execute(query, (ic, pdf_data))
        mydb.commit()
    except Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        mydb.close()

def insert_student_data(data):
    mydb = connect_db()
    if mydb is None:
        return "Error: Unable to connect to the database."

    cursor = mydb.cursor()
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
        return f"Error: {err}"
    finally:
        cursor.close()
        mydb.close()

def update_admin_data(data):
    mydb = connect_db()
    if mydb is None:
        return "Error: Unable to connect to the database."

    cursor = mydb.cursor()
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
    finally:
        cursor.close()
        mydb.close()

def update_warden_data(data):
    mydb = connect_db()
    if mydb is None:
        return "Error: Unable to connect to the database."

    cursor = mydb.cursor()
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
    finally:
        cursor.close()
        mydb.close()

def update_student_data(data):
    mydb = connect_db()
    if mydb is None:
        return "Error: Unable to connect to the database."

    cursor = mydb.cursor()
    print(data)
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
    finally:
        cursor.close()
        mydb.close()

def retrieve_table_dict(tableName):
    mydb = connect_db()
    if mydb is None:
        return "Error: Unable to connect to the database."

    cursorDict = mydb.cursor(dictionary=True)
    try:
        query = f"SELECT * FROM {tableName}"
        cursorDict.execute(query)
        entries = cursorDict.fetchall()
        return entries
    except mysql.connector.Error as e:
        return f"Error: {e}"
    finally:
        cursorDict.close()
        mydb.close()

def retrieve_confiscated_item_log():
    mydb = connect_db()
    if mydb is None:
        return "Error: Unable to connect to the database."

    cursorDict = mydb.cursor(dictionary=True)
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
    finally:
        cursorDict.close()
        mydb.close()

def insert_confiscated_item(data):
    mydb = connect_db()
    if mydb is None:
        return "Error: Unable to connect to the database."

    cursor = mydb.cursor()
    insert_query = """
    INSERT INTO confiscated_items (
        item_name, student_ic, item_description, confiscation_date, 
        confiscater_warden_ic , item_status, confiscation_reason, return_date, notes
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

    try:
        # Execute the query and commit the changes
        cursor.execute(insert_query, values)
        mydb.commit()
        return "[✔] Confiscated item inserted successfully!"
    except mysql.connector.Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        mydb.close()

def update_confiscated_item_status(action, id):
    mydb = connect_db()
    if mydb is None:
        return "Error: Unable to connect to the database."

    cursor = mydb.cursor()
    try:
        query = "UPDATE confiscated_items SET item_status = %s WHERE confiscated_item_id = %s"
        print("Changing status...")
        cursor.execute(query, (action, id))
        mydb.commit()
    except Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        mydb.close()

def update_ban_period(student_id, outing_datetime):
    mydb = connect_db()
    if mydb is None:
        return "Error: Unable to connect to the database."

    cursor = mydb.cursor()
    try:
        cursor.execute('''
            UPDATE student_outing_placeholder
            SET banPeriod = %s
            WHERE studentID = %s
        ''', (outing_datetime, student_id))
        mydb.commit()
    except Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        mydb.close()

def retrieve_hostel_application_record(IC):
    mydb = connect_db()
    if mydb is None:
        return "Error: Unable to connect to the database."

    cursor = mydb.cursor()
    try:
        query = "SELECT * FROM hostel_application WHERE student_ic = %s"
        cursor.execute(query, (IC,))
        record = cursor.fetchone()
        return record
    finally:
        cursor.close()
        mydb.close()

def add_new_user(data):
    mydb = connect_db()
    if mydb is None:
        return "Error: Unable to connect to the database."

    cursor = mydb.cursor()
    try:
        # Hash the password
        password = data['password']
        hashed_password = hash_password(password)
        data['password'] = hashed_password

        if data['user_type'] == "warden":
            insert_query = """
            INSERT INTO warden (warden_ic, name, email, phone_number, address, date_of_joining, gender, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                data['warden_ic'],
                data['name'],
                data['email'],
                data['phone_number'],
                data['address'],
                data['date_of_joining'],
                data['gender'],
                data['password']
            ))
        
        elif data['user_type'] == "admin":
            insert_query = """
            INSERT INTO admin (admin_ic, name, email, phone_number, address, date_of_joining, gender, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                data['admin_ic'],
                data['name'],
                data['email'],
                data['phone_number'],
                data['address'],
                data['date_of_joining'],
                data['gender'],
                data['password']
            ))
        
        # Commit the transaction
        mydb.commit()
        return "User  added successfully."

    except Error as e:
        print("Error while inserting data into MySQL", e)
        return "Error: Unable to add user."

    finally:
        cursor.close()
        mydb.close()

def set_new_password(ic, new_password):
    mydb = connect_db()
    if mydb is None:
        return "Error: Unable to connect to the database."

    cursor = mydb.cursor()
    try:
        hashed_password = hash_password(new_password)
        role = retrieve_role(ic)

        if role == "Admin":
            # Update the password for the admin table
            cursor.execute("UPDATE admin SET password = %s WHERE admin_ic = %s", (hashed_password, ic))
        
        elif role == "Warden":
            # Update the password for the warden table
            cursor.execute("UPDATE warden SET password = %s WHERE warden_ic = %s", (hashed_password, ic))
        
        # Commit the changes to the database
        mydb.commit()

        return "Success"
    
    except Exception as e:
        mydb.rollback()  # Rollback in case of error
        return f"Error: {str(e)}"
    
    finally:
        cursor.close()
        mydb.close()