import mysql.connector

mydb = mysql.connector.connect (
    host = 'localhost',
    user = 'root',
    password = ''
)

cursor = mydb.cursor()

cursor.execute("DROP DATABASE IF EXISTS stay_sync")
print("Database dropped successfully.")

cursor.execute("CREATE DATABASE stay_sync")

cursor.execute("USE stay_sync")

cursor.execute("""
    CREATE TABLE user_credentials (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(100) NOT NULL
    )
""")

mydb.commit()

cursor.close()
mydb.close()

print("Database and table created successfully.")