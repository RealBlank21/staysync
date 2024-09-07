from flask import Flask, request, render_template, redirect, url_for, session, flash
import os
from app import authentication, db

with open("SESSION.txt", 'r') as file:
    SESSION = file.read().strip()

app = Flask(__name__)
app.secret_key = SESSION

@app.route('/')
def front_page():
    return render_template('front_page.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            error_message = "Please fill in all fields."
        else:
            authentication_status = authentication.validate_password(username, password)
            if authentication_status:
                user_role = db.retrieve_role(username)
                session['username'] = username
                session['user_role'] = user_role
                return redirect(url_for('dashboard'))
            else:
                error_message = "Incorrect username or password."

    return render_template('index.html', error_message=error_message)

@app.route('/register_user')
def register_user():
    return render_template('register_user.html')


"""
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
"""

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        user_role = session.get('user_role')
        return render_template('dashboard.html', username=username, user_role=user_role)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Remove user from session
    session.pop('username', None)
    session.pop('user_role', None)
    return redirect(url_for('login'))

@app.route('/test')
def test():
    return render_template('test.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
