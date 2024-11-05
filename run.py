from flask import Flask, request, render_template, redirect, url_for, session, make_response, flash, jsonify
from flask_mail import Mail, Message
from datetime import timedelta
import os
from app import authentication, db
from datetime import datetime

with open("SESSION.txt", 'r') as file:
    SESSION = file.read().strip()

app = Flask(__name__)
app.secret_key = SESSION

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'realblank21@gmail.com'
app.config['MAIL_PASSWORD'] = 'wukf ctml yhol iboj'
app.config['MAIL_DEFAULT_SENDER'] = 'noreply@gmail.com'

mail = Mail(app)

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

    entries = db.retrived_table_joined()

    students = db.retrieve_table_dict("students")

    studentNames = [student['studentName'] for student in students]

    return render_template('confiscated_item_log.jinja', username=username, user_role=user_role, entries=entries, studentNames=studentNames)

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

@app.route('/outing_manager')
def outing_manager():
    students = db.retrieve_table_dict("student_outing_placeholder")
    return render_template('outing_manager.html', entries=students)

@app.route('/outing_check')
def outing_check():
    students = db.retrieve_table_dict("student_outing_placeholder")
    return render_template('outing_check.html', entries=students)

@app.route('/student_outing', methods=['POST'])
def student_outing():
    outing_student_id = request.form.get('outing_student_id')

    students = db.retrieve_table_dict("student_outing_placeholder")

    banPeriod = students[int(outing_student_id) - 1]["banPeriod"]

    current_time = datetime.now()

    if not banPeriod or current_time > datetime.fromisoformat(banPeriod):
        print("You can go outing.")
        return redirect(url_for('outing_check'))

    print("You are still in the ban period.")

    return redirect(url_for('outing_check', error='Invalid student ID'))

@app.route('/save_outing_ban', methods=['POST'])
def save_outing_ban():
    for field_name, outing_datetime in request.form.items():
        if field_name.startswith("outingDateTime_"):
            student_id = field_name.split("_")[1]
            if outing_datetime:
                db.update_ban_period(student_id, outing_datetime)
                print(outing_datetime)

    return redirect(url_for('outing_manager'))

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        msg = Message('Hello from Flask!', 
                      recipients=['realblanket21@gmail.com'])
        msg.body = 'This is a test email sent from a Flask web application!'
        mail.send(msg)
        return 'Email sent!'
    except Exception as e:
        return str(e)

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test.html', error_message="Error")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
