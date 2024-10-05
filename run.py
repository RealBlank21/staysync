from flask import Flask, request, render_template, redirect, url_for, session, make_response
from datetime import timedelta
import os
from app import authentication, db

with open("SESSION.txt", 'r') as file:
    SESSION = file.read().strip()

app = Flask(__name__)
app.secret_key = SESSION

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=3)

@app.route('/')
def front_page():
    username = session.get('username')
    user_role = session.get('user_role')
    
    return render_template('front_page.html', username=username, user_role=user_role)

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

                # Mark the session as permanent
                session.permanent = True

                return redirect(url_for('front_page'))
            else:
                error_message = "Incorrect username or password."

    return render_template('login.html', error_message=error_message)

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        user_role = session.get('user_role')
        response = make_response(render_template('dashboard.html', username=username, user_role=user_role))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response
    else:
        return redirect(url_for('login'))
    
@app.route('/application', methods=['GET', 'POST'])
def application():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == "POST":
        student_hostel_application_form_data = request.form

        db.insert_student_admission(student_hostel_application_form_data)
        print("success")

        return render_template('application.html', success_message="Application has been submitted!")
    else:
        return render_template('application.html')

@app.route('/logout')
def logout():
    # Remove user from session
    session.pop('username', None)
    session.pop('user_role', None)
    return redirect(url_for('front_page'))

@app.route('/hostel_application')
def hostel_application():
    return render_template('hostel_application.html')

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/test')
def test():
    return render_template('test.html', error_message="Error")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
