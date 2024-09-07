import mysql.connector

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