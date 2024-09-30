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
        portrait = request.form.get('portrait')
        fullName = request.form.get('fullName')
        gender = request.form.get('gender')
        studentId = request.form.get('studentId')
        studentIc = request.form.get('studentIc')
        dob = request.form.get('dob')
        phoneSelf = request.form.get('phoneSelf')
        phoneGuardian = request.form.get('phoneGuardian')
        email = request.form.get('email')
        addressLine1 = request.form.get('addressLine1')
        addressLine2 = request.form.get('addressLine2')
        area = request.form.get('area')
        city = request.form.get('city')
        state = request.form.get('state')
        zipCode = request.form.get('zip')
        medicalCondition1 = request.form.get('medicalCondition1')
        medicalCondition2 = request.form.get('medicalCondition2')
        medicalCondition3 = request.form.get('medicalCondition3')

        db.insert_student_admission(fullName, gender, studentId, studentIc, dob, phoneSelf, phoneGuardian, email, addressLine1, addressLine2, area, city, state, zip, medicalCondition1, medicalCondition2, medicalCondition3)
        return render_template('application.html', success_message="Application has been submitted!")
    else:
        return render_template('application.html')

@app.route('/logout')
def logout():
    # Remove user from session
    session.pop('username', None)
    session.pop('user_role', None)
    return redirect(url_for('front_page'))

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/test')
def test():
    return render_template('test.html', error_message="Error")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
