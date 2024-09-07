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

# Commit the transaction
mydb.commit()

# Close the cursor and connection
cursor.close()
mydb.close()

print("User credentials inserted and database setup completed successfully.")
