from flask import Flask, render_template, request, jsonify, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import json
import psycopg2
import hashlib
import imghdr
import uuid
import os
from flask_login import *
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'tutors/'

# using SQLAlchemy to connect to a POstgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/Tutoring'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
db = SQLAlchemy(app)
Session(app)

@app.route('/', methods=['GET'])
def redir():
    return redirect('/home')

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/register-student', methods=['GET'])
def register_student():
    return render_template('register-student.html')

@app.route('/register-tutor', methods=['GET'])
def register_tutor():
    return render_template('register-tutor.html')

@app.route('/signin', methods=['GET'])
def signin():
    return render_template('signin.html')

@app.route('/profile/<id>')
def show_profile(id):
    return render_template('profile.html') #This page should be able to change based on user (tutor vs student) (jxy123456 vs plt654321)

@app.route('/api/register-tutor', methods=['POST'])
def check_response():
    data = request.json
    print(data)
    return data

@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        # extract login credentials from request body
        credentials = request.json
        username_input = credentials['net-id']
        password_input = credentials['password']
        hashed = encrypt(password_input)

        #connect to postgre
        conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432') 

        #creating a cursor object using cursor()
        cursor = conn.cursor()
    
        try:
            #inserting data into DB
            cursor.execute(f"select net_id from login where hashed_pw = '{password_input}'") #CHANGE THIS TO HASHED WHEN WE START STORING HASHED
            results = cursor.fetchone()
        except Exception as e:
            print(e)
            conn.close()
            return 'Invalid username or password'
        if results is not None:
            session['key'] = username_input
            conn.close()
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password'

#Backend10: respond to API call to send back a query for the user's fav list from the database
@app.route('/favorites/<int:id>', methods=['GET'])
def get_favorites(id):
    # Execute a SELECT statement to retrieve the user's fav list from the database
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432')
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM FavoriteTutors WHERE id = %s", (id,))

    # Fetch the results and store them in results
    results = cursor.fetchall()

    # Return the results as JSON response
    return jsonify(results)

@app.route('/logout')
def logout():
    session.pop('key', None)
    return redirect('/home')

@app.route('/api/tutor-picture', methods=['POST'])
def add_pic():
    net_id = request.args.get('net-id')
    try:
        if 'file' not in request.files:
            print('missing file')
            return 'failed'
        pic = request.files['file']
        if pic.filename == '':
            print('no file')
            return 'failed'
        filename = secure_filename(pic.filename)
        path = app.config['UPLOAD_FOLDER'] + net_id
        if not os.path.exists(path):
            os.makedirs(path)
        pic.save(os.path.join(app.config['UPLOAD_FOLDER'] + net_id + '/', filename))
    except Exception as e:
        print(e)
        return 'failed'
    return 'success'

@app.route('/api/register-student', methods=['POST'])
def add_user():
    if request.method == 'POST':
        user_info = request.json
        frontend_message = strongPWD(user_info['password'])
        if frontend_message == 'Strong':
            if 'mname' in user_info:
                #get return val of insertuser and check
                insert_status = insert_user(user_info['net-id'],user_info['password'],user_info['first-name'],user_info['middle-name'],user_info['last-name'],user_info['user-type'])
                if insert_status != 'Success':
                    return insert_status
            else:
                #get return val of insertuser and check
                insert_status = insert_user(user_info['net-id'],user_info['password'],user_info['first-name'],'',user_info['last-name'],user_info['user-type'])
                if insert_status != 'Success':
                    return insert_status
            return frontend_message
        else:
            return frontend_message
    
def insert_user(net_id, passwd, fname, mname, lname, usertype):
    #connect to postgre
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432') 

    #creating a cursor object using cursor()
    cursor = conn.cursor()

    #tempcode for confirming a connection
    cursor.execute('select version()')

    #fetch a single row using fetchone. method fetchmany and fetchall can be used depending on query, this is just verifying db connection
    connectCheck = cursor.fetchone()
    print('Connection established to: ', connectCheck)
    
    try:
        
        #call hashing function
        #save hashedpw, and send into db
        hashedPassword = encrypt(passwd)
            
        #inserting data into DB
        cursor.execute("insert into Person (net_id, fname, mname, lname, hours_completed, usertype) values (\'" + net_id + "\', \'" + fname + "\', \'" + mname + "\', \'" + lname + "\', 0, \'" + usertype + "\')")
        conn.commit()
        cursor.execute("insert into Login (net_id, hashed_pw) values (\'" + net_id + "\',\'" + hashedPassword + "\')")
        conn.commit()
    except:
        return ("Error, user already exists")
    conn.close()
    return 'Success'


##checks to see if the appointment is valid, then calls insertAppointment to add to the database
@app.route('/api/register-appointment', methods=['POST'])
def appointmentCreation ():
    timeSlotInfo = request.json
    timeSlot = timeSlotInfo['day'] + " " + timeSlotInfo['time']
    timeSlot_status = timeVal(timeSlot)

    if timeSlot_status == 'Valid':
        appointment_status = insertAppointment (timeSlotInfo['session_id'], timeSlotInfo['tutor_id'], timeSlotInfo['student_id'], timeSlotInfo['day'], timeSlotInfo['time'])
        return appointment_status
    else:
        return timeSlot_status


##adds the appointment to the database
def insertAppointment(session_id, tutor_id, student_id, day, time):
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432')
    cursor = conn.cursor()

    try:
        cursor.execute("insert into TutorApts (session_id, tutor_id, student_id, day, time) values (\'" + session_id + "\', \'" + tutor_id + "\', \'" + student_id + "\', \'" + day + "\', \'" + time + "\')")
        conn.commit()
    except:
        return ("Error, appointment could not be created")
    conn.close()
    return 'Success'


##checks if the password contains 12 character, upper and lower case character, and a number
##returns a boolean and sends a message to front end display
def strongPWD(pwd):
    check = True
    weakPass = ""
    
    if len(pwd) < 12:
        check = False
        weakPass += "Password needs to be at least 12 characters.\n"

    if pwd.islower() or pwd.isupper():
        check = False
        weakPass += "Password needs at least 1 upper and 1 lower case character.\n"
    
    if any(i.isdigit() for i in pwd) == False:
        check = False
        weakPass += "Password needs at least one number.\n"


    if check:
        return "Strong"
    else:
        return weakPass
    #if this gets here, there is an error
    return error


##returns an encrypted password
def encrypt(pwd):
    newPwd = hashlib.sha256(pwd.encode())
    newPwd = newPwd.hexdigest()
    return newPwd

if __name__ == '__main__':
    app.run(debug=True)

##checks to see if the file is PNG JPEG JPG  
def picVal (imagePath):
    if imghdr.what(imagePath) in ['jpeg','jpg', 'png']:
        return "Valid"
    else:
        return "Not a supported file type.\n"


##validates netID
def idVal (netID):
    if not netID[:3].isalpha() or not netID[3:].isnumeric():
        return "Not a valid NetID. \n"
    return "Valid"

#validates subject
def subjectVal (subject):
    ##separates the subject at the space character
    sub = subject.split()

    if not sub[0].isalpha() or not sub[1].isnumeric():
        return "Not a valid subject. \n"
    return "Valid"

def timeVal (timeSlot):
    ##separates the timeSlot string at the space characters
    day = timeSlot.split()

    day[1] = day[1].replace("-", ":")
    time = day[1].split(":")

    if not day[0].lower() in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        return "Not a valid day. \n"
    ##checks to see if the time is valid
    if not (int(time[0]) < 25 and int(time[2]) < 25 and int(time[1]) < 60 and int(time[3]) < 60):
        return "Not a valid time. \n"
    
    return "Valid"
