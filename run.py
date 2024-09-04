from flask import Flask, request, render_template, redirect, url_for

import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'stay_sync'
)

print(mydb)

app = Flask(__name__, template_folder="app/templates")

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

    if username == 'admin' and password == 'admin':
        #return redirect(url_for('dashboard'))
        authentication = authenticate_user(username, password)

        return str(authentication)
    else:
        return "Login Failed"

def authenticate_user(username, password):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM account_credentials WHERE username = %s AND password = %s", (username, password))
    result = mycursor.fetchone()
    if 

@app.route('/dashboard')
def dashboard():
    return render_template('admin_dashboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)