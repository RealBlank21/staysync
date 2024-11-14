from flask import Flask, request, render_template, redirect, url_for, session, make_response, flash, jsonify, abort
import requests
from flask_mail import Mail, Message
from datetime import timedelta
import os
from app import authentication, db, pdf
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer

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

serializer = URLSafeTimedSerializer(app.secret_key)

def send_mail(to, subject, body):
    msg = Message(subject, recipients=[to])
    msg.body = body
    mail.send(msg)

def send_mail_with_attachment(to, subject, body, student_ic):
    # Construct the file path using the student IC
    pdf_filename = f"{student_ic}.pdf"
    attachment_path = f"./pdf/applications/{pdf_filename}"
    
    msg = Message(subject=subject, recipients=[to])
    msg.body = body
    
    # Attach the PDF file
    try:
        with open(attachment_path, 'rb') as f:
            msg.attach(pdf_filename, "application/pdf", f.read())
        
        # Send the email
        mail.send(msg)
        print(f"Email sent successfully to {to} with attachment.")
    except FileNotFoundError:
        print(f"Error: PDF file {pdf_filename} not found.")

def send_verification_email(user_email):
    token = serializer.dumps(user_email, salt='email-verify')
    verification_url = url_for('verify_email', token=token, _external=True)
    
    msg = Message('Email Verification', recipients=[user_email])
    msg.body = f"Please click on the following link to verify your email and access the system: {verification_url}"
    mail.send(msg)

@app.route('/verify_email/<token>')
def verify_email(token):
    try:
        user_email = serializer.loads(token, salt='email-verify', max_age=3600)  # Token valid for 1 hour
        # Retrieve user information based on the email
        user = db.get_user_by_email(user_email)  # Function to retrieve user details from the database

        # Set up session data after verification
        session['role'] = user.role
        session['name'] = user.name
        session['ic'] = user.ic

        return "Verification successful! You are now logged in."
    except:
        abort(404)  # Invalid or expired token

@app.errorhandler(404)
def page_not_found(error):
    return "The verification link is invalid or expired. Please request a new one.", 404

@app.route('/')
def front_page():
    username = session.get('username')
    user_role = session.get('user_role')
    
    return render_template('front_page.html', username=username, user_role=user_role)

@app.route('/contact_us')
def contact_us():
    username = session.get('username')
    user_role = session.get('user_role')
    
    return render_template('contact_us.html', username=username, user_role=user_role)

@app.route('/about_us')
def about_us():
    username = session.get('username')
    user_role = session.get('user_role')
    
    return render_template('about_us.html', username=username, user_role=user_role)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'POST':
        ic = request.form.get('ic')
        password = request.form.get('password')
        recaptcha_token = request.form['g-recaptcha-response']

        # Verify the reCAPTCHA response with Google's API
        recaptcha_payload = {
            'secret': "6LfmansqAAAAAA9guboxt1Q4cRid6G_b2TXyF4od",
            'response': recaptcha_token
        }

        recaptcha_result = requests.post('https://www.google.com/recaptcha/api/siteverify', data=recaptcha_payload)
        recaptcha_json = recaptcha_result.json()

        if not recaptcha_json.get('score') >= 0.5:
            error_message = "reCAPTCHA verification failed. Please try again."
            return render_template('login.html', error_message=error_message)

        if not ic or not password:
            error_message = "Please fill in all fields."
        else:
            authentication_status = authentication.validate_password(ic, password)
            if authentication_status:
                # user_role = db.retrieve_role(ic)
                # session['username'] = db.retrieve_name(ic)
                # session['user_role'] = user_role
                # session['user_ic'] = ic

                user_email = db.retrieve_mail(ic)

                send_verification_email(user_email)
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
    error_message = None

    if 'username' in session:
        return redirect(url_for('front_page'))
    
    if request.method == "POST":
        # Get reCAPTCHA response from the form
        recaptcha_response = request.form['g-recaptcha-response']

        # Verify the response
        payload = {
            'secret': "6LfycnsqAAAAAItT7R-K4xmxmOHhIWJet7LGp-kj",
            'response': recaptcha_response
        }
        verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        response = requests.post(verify_url, data=payload)
        result = response.json()

        if not result['success']:
            return render_template('application.html', error_message="reCAPTCHA verification failed.")
        
        student_hostel_application_form_data = request.form.to_dict()
        student_hostel_application_form_data.pop('g-recaptcha-response', None)

        student_hostel_application_form_data.get('name', '').strip().upper()

        check_invalid = authentication.validate_form_data(student_hostel_application_form_data)

        if check_invalid:
            return render_template('application.html', error_message=check_invalid)

        # Now insert the data without the reCAPTCHA response
        print(db.insert_student_admission(student_hostel_application_form_data))

        pdf.create_application_pdf(student_hostel_application_form_data, student_hostel_application_form_data['student_ic']+".pdf")

        student_email = student_hostel_application_form_data['student_email']

        # Format the body to include all the data for verification
        body = "Your hostel application has been successfully submitted! Please check your details below:\n\n"

        body += "\nPlease review the details below. If any information is incorrect, contact our team as soon as possible."

        # Send the email
        send_mail_with_attachment(
            to=student_email,
            subject="Hostel Application Submitted",
            body=body,
            student_ic=student_hostel_application_form_data['student_ic']
        )

        return render_template('application.html', success_message="Your hostel application has been successfully submitted! Please check your email within 1-3 business days for updates as our team reviews your application.")
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

    entries = db.retrieve_table_dict("hostel_application")

    return render_template('hostel_application.html', students=entries, username=username, user_role=user_role)

@app.route('/hostel_application_action', methods=['POST'])
def hostel_application_action():
    data = request.get_json()
    student_ic = data.get('student_ic')
    action = data.get('action')

    print("Action:", action, "IC:", student_ic)

    db.update_hostel_application_status(action, student_ic)

    student_email = db.retrieve_hostel_application(student_ic)["email"]
    
    if action == "Approved":
        # Retrieve data and send to hostel application
        print("Status updated to Approved")

        body = "Your application has been approved! Welcome to the hostel."

        student_data = db.retrieve_hostel_application(student_ic)
        print(db.insert_student_data(student_data))

    if action == "Rejected":
        print("Status updated to Rejected")

        body = "Your application has been rejected."


    send_mail(
        to=student_email,
        subject="Hostel Application",
        body=body,
    )

    return jsonify({'message': 'Action completed successfully'})

@app.route('/outing_application')
def outing_application():
    if session.get('user_role') !='Student':
        return redirect(url_for('login'))
    
    username = session.get('username')
    user_role = session.get('user_role')

    return render_template('outing_application.html', username=username, user_role=user_role)

@app.route('/update-admin', methods=['POST'])
def update_admin():
    # Extract form data
    form_data = request.form.to_dict()

    db.update_admin_data(form_data)

    return jsonify(success=True)

@app.route('/update-warden', methods=['POST'])
def update_warden():
    # Extract form data
    form_data = request.form.to_dict()

    db.update_warden_data(form_data)

    return jsonify(success=True)

@app.route('/update-student', methods=['POST'])
def update_student():
    # Extract form data
    form_data = request.form.to_dict()

    db.update_student_data(form_data)

    return jsonify(success=True)

@app.route('/confiscated_item_log')
def confiscated_item_log():
    if session.get('user_role') not in ['Warden', 'Admin']:
        return redirect(url_for('login'))
    
    username = session.get('username')
    user_role = session.get('user_role')

    entries = db.retrieve_confiscated_item_log()

    student_data = db.retrieve_table_dict('student')

    student_ics_and_names = [
        {'student_ic': student['student_ic'], 'name': student['name']} for student in student_data
    ]

    return render_template('confiscated_item_log.html', username=username, user_role=user_role, confiscated_item=entries, student_ics_and_names=student_ics_and_names)

@app.route('/submit_confiscation', methods=['POST'])
def submit_confiscation():
    form_data = request.get_json()
    
    print(db.insert_confiscated_item(form_data))

    return jsonify({'success': True, 'message': 'Confiscation item submitted successfully!'})

@app.route('/confiscated_item_action', methods=['POST'])
def confiscated_item_action():
    try:
        data = request.get_json()
        confiscated_item_id = data['confiscated_item_id']
        action = data['action']
        
        db.update_confiscated_item_status(action, confiscated_item_id)

        return jsonify({"message": "Action processed successfully"}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/student_information')
def student_information():
    if session.get('user_role') not in ['Warden', 'Admin']:
        return redirect(url_for('login'))
    
    username = session.get('username')
    user_role = session.get('user_role')

    entries = db.retrieve_table_dict("student")

    return render_template('students.html', username=username, user_role=user_role, student=entries)

@app.route('/warden_information')
def warden_information():
    if session.get('user_role') not in ['Warden', 'Admin']:
        return redirect(url_for('login'))
    
    username = session.get('username')
    user_role = session.get('user_role')

    entries = db.retrieve_table_dict("warden")

    return render_template('warden.html', username=username, user_role=user_role, warden=entries)

@app.route('/admin_information')
def admin_information():
    if session.get('user_role') not in ['Admin']:
        return redirect(url_for('login'))
    
    username = session.get('username')
    user_role = session.get('user_role')

    entries = db.retrieve_table_dict("admin")

    return render_template('admin.html', username=username, user_role=user_role, admin=entries)

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

@app.route("/fingerprint_test")
def index():
    return render_template("fingerprint_test.html")

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        send_mail(
            to="realblanket21@gmail.com",
            subject="Hostel Application Submitted",
            body="Your hostel application has been successfully submitted! "
                "Please check your email within 1-3 business days for updates as our team reviews your application."
        )
        return "Mail Sent!"
    except Exception as e:
        return str(e)

@app.route('/forgot_password')
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('test.html', error_message="Error")

#if __name__ == '__main__':
#    app.run(debug=True)