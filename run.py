from flask import Flask, request, render_template, redirect, url_for
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import mysql.connector

app = Flask(__name__)
ph = PasswordHasher()

# Connect to MySQL database
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='stay_sync'
)

cursor = mydb.cursor()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

    if username == 'admin' and password == 'admin':
        return redirect(url_for('dashboard'))
    else:
        return "Login Failed"

@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        if not username or not password or not role:
            return f"Please fill in all fields\n{username}, {password}, {role}", 400
        
        hashed_password = ph.hash(password)

        sql = "INSERT INTO user_credentials (username, password, role) VALUES (%s, %s, %s)"
        values = (username, hashed_password, role)
        
        try:
            cursor.execute(sql, values)
            mydb.commit()
            return redirect(url_for('register_user'))
        except mysql.connector.Error as err:
            return f"Error: {err}"

    return render_template('register_user.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
