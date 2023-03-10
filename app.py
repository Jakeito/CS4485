from flask import Flask, render_template, request, jsonify, redirect
import json
import psycopg2
import hashlib
from flask_login import *

app = Flask(__name__)

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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/home')

@app.route('/api/register', methods=['POST'])
def add_user():
    if request.method == 'POST':
        user_info = request.json
        frontend_message = strongPWD(user_info['password'])
        if frontend_message == 'Strong':
            if 'mname' in user_info:
                #get return val of insertuser and check
                insert_status = insert_user(user_info['net_id'],user_info['password'],user_info['fname'],user_info['mname'],user_info['lname'],user_info['usertype'])
                if insert_status != 'Success':
                    return insert_status
            else:
                #get return val of insertuser and check
                insert_status = insert_user(user_info['net_id'],user_info['password'],user_info['fname'],'',user_info['lname'],user_info['usertype'])
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

##checks if the password contains 12 character, upper and lower case character, and a number
##returns a boolean and sends a message to front end display
def strongPWD (pwd):
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
def encrypt (pwd):
    newPwd = hashlib.sha256(pwd.encode())
    newPwd = newPwd.hexdigest()
    return newPwd

