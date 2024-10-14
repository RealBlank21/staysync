from flask import Flask, request, render_template, redirect, url_for, session, make_response, flash, jsonify
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
    if session.get('user_role') !='Admin':
        return redirect(url_for('login'))
    
    username = session.get('username')
    user_role = session.get('user_role')

    entries = db.retrieve_table_dict("hostel_applications")

    return render_template('hostel_application.html', entries=entries, username=username, user_role=user_role)

@app.route('/hostel_application_action', methods=['POST'])
def handle_action():
    action = request.json.get('action')
    entryIndex = request.json.get('entry')

    print(action)
    
    db.hostel_application_action(action, entryIndex)
    
    return render_template('hostel_application.html')

@app.route('/outing_application')
def outing_application():
    if session.get('user_role') !='Student':
        return redirect(url_for('login'))
    
    username = session.get('username')
    user_role = session.get('user_role')

    return render_template('outing_application.html', username=username, user_role=user_role)

@app.route('/confiscated_item_log')
def confiscated_item_log():
    if session.get('user_role') not in ['Warden', 'Admin']:
        return redirect(url_for('login'))
    
    username = session.get('username')
    user_role = session.get('user_role')

    entries = db.retrieve_table_dict("confiscated_items")

    return render_template('confiscated_item_log.html', username=username, user_role=user_role, entries=entries)

@app.route('/student_information')
def student_information():
    if session.get('user_role') not in ['Warden', 'Admin']:
        return redirect(url_for('login'))
    
    username = session.get('username')
    user_role = session.get('user_role')

    entries = db.retrieve_table_dict("students")

    return render_template('students.html', username=username, user_role=user_role, entries=entries)

@app.route('/warden_information')
def warden_information():
    if session.get('user_role') not in ['Warden', 'Admin']:
        return redirect(url_for('login'))
    
    username = session.get('username')
    user_role = session.get('user_role')

    entries = db.retrieve_table_dict("warden")

    return render_template('warden.html', username=username, user_role=user_role, entries=entries)

@app.route('/admin_information')
def admin_information():
    if session.get('user_role') not in ['Admin']:
        return redirect(url_for('login'))
    
    username = session.get('username')
    user_role = session.get('user_role')

    entries = db.retrieve_table_dict("admin")

    return render_template('admin.html', username=username, user_role=user_role, entries=entries)

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/test')
def test():
    return render_template('test.html', error_message="Error")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
