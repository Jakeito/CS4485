from flask import Flask, render_template, request, jsonify, redirect, session, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import json
import datetime
import psycopg2
import hashlib
import imghdr
import uuid
import os
from flask_login import *
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/tutors/'
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

'''PAGES'''
@app.route('/')
def redir():
    return redirect('/home')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register-student')
def register_student():
    return render_template('register-student.html')

@app.route('/register-tutor')
def register_tutor():
    return render_template('register-tutor.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/profile/<string:subpath>')
def show_profile(subpath):
    return render_template('profile.html')

@app.route('/tutor')
def show_tutor():
    return render_template('tutor.html')

@app.route('/appointment')
def appointments():
    return render_template('appointment.html')

@app.route('/booking')
def booking():
    return render_template('booking.html')

@app.route('/subjects')
def subjects():
    return render_template('supported.html')

'''API ROUTES'''
@app.route('/api/net-id')
def check_netid():
    return session['key']

@app.route('/api/user-type')
def check_usertype():
    return session['usertype']

@app.route('/api/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        # extract login credentials from request body
        credentials = request.json
        username_input = credentials['net-id']
        password_input = credentials['password']
        hashed = encrypt(password_input)
        usertype = usertype_check(username_input)
        print(hashed)
        #connect to postgre
        conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432') 

        #creating a cursor object using cursor()
        cursor = conn.cursor()
    
        try:
            #inserting data into DB
            cursor.execute(f"select net_id from login where hashed_pw = '{hashed}'")
            results = cursor.fetchone()
        except Exception as e:
            print(e)
            conn.close()
            return 'Invalid username or password'
        if results is not None and username_input == results[0]:
            session['key'] = username_input
            session['usertype'] = usertype
            conn.close()
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password'

#Backend10: respond to API call to send back a query for the user's fav list from the database
@app.route('/api/favorite', methods=['GET'])
def get_favorites():
    # get id
    id = session['key']

    # Execute a SELECT statement to retrieve the user's fav list from the database
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432')
    cursor = conn.cursor() 
    cursor.execute(f"SELECT tutor_id FROM FavoriteTutors WHERE student_id = '{id}'")

    # Fetch the results and store them in results
    tutors = cursor.fetchall()
    results = []
    for i in tutors:
        cursor.execute(f"SELECT fname, mname, lname, net_id FROM Person WHERE net_id = '{i[0]}'")
        result = cursor.fetchone()
        favorite_dict = {
            'net-id': result[3],
            'fname': result[0],
            'mname': result[1],
            'lname': result[2],
        }
        results.append(favorite_dict)
    conn.close()    
    # Return the results as JSON response
    return results

#Similar to backend 10, but check if a tutor is favorited and return true or false
@app.route('/api/check-favorite', methods=['POST'])
def check_favorites():
    # get id
    id = session['key']
    tutor_info = request.json

    # Execute a SELECT statement to retrieve the user's fav list from the database
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432')
    cursor = conn.cursor() 
    cursor.execute("SELECT tutor_id FROM FavoriteTutors WHERE student_id = %s and tutor_id = %s", (id, tutor_info['tutor-id']))


    # Fetch the results and store them in results
    try:
        tutors = cursor.fetchone()
        conn.close()
        if tutors is not None:
            return 'true'
        else:
            return 'false'
    except Exception as e:
        print(repr(e))
        return 'false'

@app.route('/logout')
def logout():
    session.pop('key', None)
    session.pop('usertype', None)
    return redirect('/home')

@app.route('/api/subjects', methods=['GET'])
def get_all_subjects():
    #turning table into string for frontend
    class_table_dirty = supported_subjects()
    class_table_clean = []
    for element in class_table_dirty:
        class_table_clean.append(element[0])
    print(class_table_clean)
    return class_table_clean

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
        if not filename.endswith('png') and not filename.endswith('jpeg') and not filename.endswith('jpg'):
            return 'Wrong file extension'
        path = app.config['UPLOAD_FOLDER'] + net_id
        extension = filename.split('.')
        if not os.path.exists(path):
            os.makedirs(path)
        pic.save(os.path.join(app.config['UPLOAD_FOLDER'] + net_id + '/', net_id + '.' + extension[1]))
    except Exception as e:
        print(e)
    return 'Valid'

#this register deals with registering a student
@app.route('/api/register-student', methods=['POST'])
def add_student():

    if request.method == 'POST':
        user_info = request.json
        #check username and pwd input input
        username_valid = idVal(user_info['net-id'])
        password_strong = strongPWD(user_info['password'])
        frontend_msg = ''

        if username_valid == 'Valid' and password_strong == 'Strong':
            if 'middle-name' in user_info:
                #get return val of insertuser and check
                insert_status = insert_user(user_info['net-id'],user_info['password'],user_info['first-name'],user_info['middle-name'],user_info['last-name'],user_info['user-type'].lower())
                if insert_status != 'Valid':
                    return insert_status
            else:
                #get return val of insertuser and check
                insert_status = insert_user(user_info['net-id'],user_info['password'],user_info['first-name'],'',user_info['last-name'],user_info['user-type'].lower())
                if insert_status != 'Valid':
                    return insert_status
                
            return 'Valid'
        else:
            if username_valid != 'Valid':
                frontend_msg += username_valid
                frontend_msg += '\n'
            if password_strong != 'Strong':
                frontend_msg += password_strong
            return frontend_msg

#this register deals with registering a tutor
@app.route('/api/register-tutor', methods=['POST'])
def add_tutor():
    if request.method == 'POST':
        user_info = request.json
        frontend_msg = ''

        #check username and pwd input input
        username_valid = idVal(user_info['net-id'])
        password_strong = strongPWD(user_info['password'])

        #validate subjects and timeslots
        availability_valid = 'Valid'
        #availability_array is an array of day and time pairs, and each pair needs to be validated
        availability_array = user_info['availability'].split('\n')
        for timeslots in availability_array:
            if timeVal(timeslots) != 'Valid':
                availability_valid = 'At least one availability is not formatted correctly, please format as [Day] [Start-End]'
        

        supported_subjects_valid = 'Valid'
        #availability_array is an array of class abbreviation and numbers, and each pair needs to be validated, but can be inserted as one string
        supported_subjects_array = user_info['support-subjects'].split('\n')
        for subjects in supported_subjects_array:
            if subjectVal(subjects) != 'Valid':
                supported_subjects_valid = 'At least one inputted subject in not formatted correctly, please format as [Class letters] [Class number]'

        if username_valid == 'Valid' and password_strong == 'Strong' and availability_valid == 'Valid' and supported_subjects_valid == 'Valid':
            #insert values here based on if the user has a middle name
            if 'middle-name' in user_info:
                #get return val of insertuser and check
                insert_status = insert_user(user_info['net-id'],user_info['password'],user_info['first-name'],user_info['middle-name'],user_info['last-name'],user_info['user-type'].lower())
            else:
                #get return val of insertuser and check
                insert_status = insert_user(user_info['net-id'],user_info['password'],user_info['first-name'],'',user_info['last-name'],user_info['user-type'].lower())

            insert_tutor_info(user_info['net-id'], user_info['availability'], user_info['support-subjects'], user_info['about-me'])
            return insert_status
        else:
            if username_valid != 'Valid':
                frontend_msg += username_valid
            if password_strong != 'Strong':
                frontend_msg += '\n'
                frontend_msg += password_strong
            if availability_valid != 'Valid':
                frontend_msg += '\n'
                frontend_msg += availability_valid
            if supported_subjects_valid != 'Valid':
                frontend_msg += '\n'
                frontend_msg += supported_subjects_valid
            return frontend_msg

##checks to see if the appointment is valid, then calls insertAppointment to add to the database
#recieves an appointmentTime, formatted as a string ex. "Monday 11am-3pm"
@app.route('/api/register-appointment', methods=['GET', 'POST'])
def appointmentCreation (appointmentTime):
    if request.method == 'POST':
        timeSlotInfo = request.json
        day, timeSlot = appointmentTime.split(" ")
        
        timeSlot_status = timeVal(timeSlot)
        available = checkAvailability(timeSlotInfo, day, timeSlot)

        if timeSlot_status == 'Valid' and available:
            appointment_status = insertAppointment (timeSlotInfo['session_id'], timeSlotInfo['tutor_id'], timeSlotInfo['student_id'], day, timeSlot)
            return appointment_status
        elif timeSlot_status != 'Valid':
            return timeSlot_status
        else:
            return "Error, Tutor is not available at that time"

@app.route('/api/tutor/pic')
def get_tutor_pic():
    net_id = request.args.get('net-id')
    return send_from_directory(f'tutors/{net_id}', net_id)

@app.route('/api/tutor')
def get_tutor_profile():
    id = request.args.get('net-id')
    
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432') 
    cursor = conn.cursor()

    try:
        #get tutor full name
        cursor.execute(f"select net_id, fname, mname, lname from Tutors where net_id = '{id}'")
        tutor_personal_info = cursor.fetchone()
        tutor_dict = {
            'net-id': tutor_personal_info[0],
            'first-name': tutor_personal_info[1],
            'middle-name': tutor_personal_info[2],
            'last-name': tutor_personal_info[3]
        }

        #get tutor subjects
        cursor.execute(f"select classname from SubjectList where tutor_id = '{id}'")
        class_list = cursor.fetchall()
        class_list_clean = []
        for element in class_list:
            class_list_clean.append(element[0])
        tutor_dict.update({'subjects': class_list_clean})

        #get tutor availability
        cursor.execute(f"select day, time from tutoravailability where tutor_id = '{id}'")
        available_hours = cursor.fetchall()
        tutor_dict.update({'availability': available_hours})

        #get about me
        cursor.execute(f"select about_me from aboutme where tutor_id = '{id}'")
        about_me = cursor.fetchone()
        tutor_dict.update({'about-me': about_me[0]})

        conn.close()
        return tutor_dict
    except Exception as e:
        print(e)
        return e

#this route deals with returning relevant tutor information based on mode        
@app.route('/api/tutors')
def get_tutor_info():
    #connect to postgre
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432') 
    cursor = conn.cursor()

    try:
        #setting up the dict array
        all_info_dict_array = []
        #first, get list of all tutors
        cursor.execute('select net_id from Tutors')
        tutors = cursor.fetchall()
        #contains the array of only tutor net IDs
        tutor_list_clean = []
        for element in tutors:
            tutor_list_clean.append(element[0])
        #iterate through the list of tutors, dict their info, and append to dict array
        for tutor in tutor_list_clean:
            #get tutor full name
            cursor.execute('select net_id, fname, mname, lname from Tutors where net_id = \'' + tutor + '\'')
            tutor_personal_info = cursor.fetchone()
            tutor_dict = {
                'net-id': tutor_personal_info[0],
                'first-name': tutor_personal_info[1],
                'middle-name': tutor_personal_info[2],
                'last-name': tutor_personal_info[3]
            }

            #get tutor subjects
            cursor.execute('select classname from SubjectList where tutor_id = \''+ tutor +'\'')
            class_list = cursor.fetchall()
            class_list_clean = []
            for element in class_list:
                class_list_clean.append(element[0])
            tutor_dict.update({'subjects': class_list_clean})

            #get tutor availability
            cursor.execute('select day, time from tutoravailability where tutor_id = \''+ tutor +'\'')
            available_hours = cursor.fetchall()
            tutor_dict.update({'availability': available_hours})

            #get about me
            cursor.execute('select about_me from aboutme where tutor_id = \''+ tutor +'\'')
            about_me = cursor.fetchone()
            tutor_dict.update({'about-me': about_me[0]})

            all_info_dict_array.append(tutor_dict)
        conn.close()
        return all_info_dict_array
    except:
        conn.close()
        return 'Failed to retrieve tutor info'
    
#adds a tutor to a student's favorite list
@app.route('/api/add-favorite-tutor', methods=['POST'])
def add_favorite_tutor():
    data = request.json
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432') 
    cursor = conn.cursor()

    #get student id
    student_id = session['key']
    tutor_id = data['tutor-id']
    #check for login session, if not logged in don't add to favorites
    try:
        if student_id != '':
            cursor.execute('insert into FavoriteTutors (student_id, tutor_id) values (%s, %s)', (student_id, tutor_id))
            conn.commit()
            conn.close()
            return 'Success'
    except Exception as e:
        conn.close()
        return 'Error adding to favorite' + repr(e)
    
#removes a tutor from student's favorite list
@app.route('/api/remove-favorite-tutor', methods=['POST'])
def remove_favorite_tutor():
    data = request.json
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432') 
    cursor = conn.cursor()

    #get student id
    student_id = session['key']
    tutor_id = data['tutor-id']
    #check for login session, if not logged in don't remove from favorites
    try:
        if student_id != '':
            cursor.execute('delete from FavoriteTutors where student_id = %s and tutor_id = %s', (student_id, tutor_id))
            conn.commit()
            conn.close()
            return 'Success'
    except Exception as e:
        conn.close()
        return 'Error removing from favorites' + repr(e)
    
#recieves an ID and returns the user's list of appointments
@app.route('/api/get-appointments')
def usersAppointments():
    #get id
    id = session['key']

    #connect to postgre
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432') 
    cursor = conn.cursor()

    try:
        #gets a list of appointments, contains the tutor first and last name, student first and last name, time and date
        cursor.execute("SELECT t.fname AS tutor_fname, t.lname AS tutor_lname, s.fname AS student_fname, s.lname AS student_lname, ta.time, ta.date FROM TutorApts ta INNER JOIN Person t ON ta.tutor_id = t.net_id INNER JOIN Person s ON ta.student_id = s.net_id WHERE ta.tutor_id = '%s' OR ta.student_id = '%s';", (id, id))

        results = cursor.fetchall()

        #if there are no appointments made with that ID
        if cursor.rowcount == 0:
            conn.close()
            return "No appointments with that ID"

        #sorts the results based on date
        results = sorted(results, key=lambda x: x[-1])

        conn.close()
        return results
    
    except: 
        conn.close()
        return "Error, could not find appointments"

#checks to see if an appointment has passed, if it has it removes it and adds it to the user's hours
@app.route('/api/check-appointment', methods=['POST'])
def checkPassedAppointments():
    #get id
    id = session['key']

    #gets the current date and time when the function is called
    currentDateTime = datetime.datetime.now()
    time = currentDateTime.time()
    date = currentDateTime.date()
    format = '%Y-%m-%d'
    format2 = '%H:%M'
    check = 0

    #connects
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432') 
    cursor = conn.cursor()

    try:
        #grabs a list of the appointments that contain the id
        cursor.execute("SELECT * FROM TutorApts WHERE tutor_id = '%s' OR student_id = '%s'", (id, id))
        results = cursor.fetchall()

        #if there are no appointments
        if cursor.rowcount == 0:
            conn.close()
            return "No appointments with that ID"
        
        #sorts the results based on date (not sorted based on time if there is more than one on a given date)
        results = sorted(results, key=lambda x: x[-1])

        #goes through every result and sees if it is past the date
        for x in results:
            aptDate = datetime.datetime.strptime(x[6], format).date()
            #if it is before the date
            if aptDate < date:
                completedHoursFormat = timeFormat(x[4])
                completedHours = completedHoursFormat[2] - completedHoursFormat[0]

                #removes the appointment
                cursor.execute("DELETE FROM TutorApts WHERE date = '%s'", (x[6]))
                cursor.commit()

                #adds the hours to the student and tutor accounts
                cursor.execute("UPDATE Person SET hours_completed = hours_completed+%d WHERE net_id = '%s'",(completedHours, x[1]))
                cursor.commit()
                cursor.execute("UPDATE Person SET hours_completed = hours_completed+%d WHERE net_id = '%s'",(completedHours, x[2]))
                cursor.commit()
                
                check +=1
            #if the appointment is today
            elif aptDate == date:
                completedHoursFormat = timeFormat(x[4])
                completedHours = completedHoursFormat[2] - completedHoursFormat[0]
                timeStr = str(completedHoursFormat[2])+":"+str(completedHoursFormat[3])
                aptTime = datetime.datetime.strptime(timeStr, format2).time()

                if (aptTime < time):
                    #removes the appointment
                    cursor.execute("DELETE FROM TutorApts WHERE date = '%s'", (x[6]))
                    cursor.commit()

                    #adds the hours to the student and tutor accounts
                    cursor.execute("UPDATE Person SET hours_completed = hours_completed+%d WHERE net_id = '%s'",(completedHours, x[1]))
                    cursor.commit()
                    cursor.execute("UPDATE Person SET hours_completed = hours_completed+%d WHERE net_id = '%s'",(completedHours, x[2]))
                    cursor.commit()
                else:
                    break
                
            #if there is no more appointments that have passed
            else:
                break

        #returns the amount of appointments removed. will return the string even if it deletes no appointments
        conn.close()
        return "Removed " + check + " appointment(s) and added them to completed hours."
    
    except: 
        conn.close()
        return "Error, could not find appointments"
    
@app.route('/api/profile')
def get_profile():
    id = session['key']
    user_type = session['usertype']
    
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432') 
    cursor = conn.cursor()
    if user_type == 'student':
        cursor.execute(f"SELECT * FROM Person WHERE net_id = '{id}'")
        result = cursor.fetchone()
        info_dict = {
            'first-name': result[1],
            'middle-name': result[2],
            'last-name': result[3],
            'net-id': result[0],
            'hours': result[4]
        }
        conn.close()
        return info_dict
    else: #if usertype is tutor
        cursor.execute(f"select net_id, fname, mname, lname from Tutors where net_id = '{id}'")
        tutor_personal_info = cursor.fetchone()
        tutor_dict = {
            'net-id': tutor_personal_info[0],
            'first-name': tutor_personal_info[1],
            'middle-name': tutor_personal_info[2],
            'last-name': tutor_personal_info[3]
        }

        #get tutor subjects
        cursor.execute(f"select classname from SubjectList where tutor_id = '{id}'")
        class_list = cursor.fetchall()
        class_list_clean = []
        for element in class_list:
            class_list_clean.append(element[0])
        tutor_dict.update({'subjects': class_list_clean})

        #get tutor availability
        cursor.execute(f"select day, time from tutoravailability where tutor_id = '{id}'")
        available_hours = cursor.fetchall()
        tutor_dict.update({'availability': available_hours})

        #get about me
        cursor.execute(f"select about_me from aboutme where tutor_id = '{id}'")
        about_me = cursor.fetchone()
        tutor_dict.update({'about-me': about_me[0]})
        conn.close()
        return tutor_dict

'''HELPER FUNCTIONS'''
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
    return 'Valid'

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

##checks if the tutor has an available timeslot, returns a boolean
def checkAvailability(timeSlotInfo, day, timeSlot):
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432')
    cursor = conn.cursor()
    check = False

    try:
        ##gets the tutors available days
        cursor.execute("SELECT time FROM TutorAvailability WHERE tutor_id = '%s' AND day = '%s'", (timeSlotInfo['tutor_id'], day))
        results = cursor.fetchall()

        if cursor.rowcount == 0:
            conn.close()
            return False
        
        #checks if the selected time is in the tutors available hours
        for x in results:
            time2 = timeFormat(x)
            if checkTime(timeSlot, time2):
                availableTime = x
                check = True

        if check == False:
            conn.close()
            return check
        
        ##checks to see if an apointment is already schedules in that time slot
        cursor.execute("SELECT * FROM TutorApts WHERE tutor_id = '%s' AND time = '%s' AND day = '%s'", (timeSlotInfo['tutor_id'], availableTime, day))
        results = cursor.fetchall()
        if cursor.rowcount != 0:
            conn.close()
            return False

    except:
        conn.close()
        return False

    conn.close()
    return check

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

#inserts a tutor's additional information
def insert_tutor_info(net_id, availability, supported_subjects, about_me):
    #connect to postgre
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432') 
    #creating a cursor object using cursor()
    cursor = conn.cursor()
    #try catch will fail if the insert fails, returning an error message
    try:
        #insert availability into availability table, input is a string with input separated by newlines
        availability_array = availability.split('\n')
        #print(availability_array)
        
        for x in availability_array:
            #making sure to cull accidental newlines
            print(x)
            if x != '':
                #each availability entry in the array/list is stored as "[day] [time]", and needs to be split further via its space
                day_time_split = x.split()

                #insert each date and time entry
                cursor.execute("insert into tutoravailability (tutor_id, day, time) values (\'"+net_id+"\', \'"+day_time_split[0]+"\', \'"+day_time_split[1]+"\')")
                conn.commit()

        #insert supported subjects into supported subjects table, input is a string with input separated by newlines
        supported_subjects_array = supported_subjects.split('\n')

        for input in supported_subjects_array:
            if input != '':
                #insert each subject entry
                cursor.execute('insert into SubjectList (tutor_id, classname) values (\''+ net_id +'\',\''+ input +'\')')
                conn.commit()
        

        #insert about me into table
        cursor.execute('insert into AboutMe(tutor_id, about_me) values (\''+ net_id + '\', \''+ about_me +'\')')
        conn.commit()

    except:
        return ("Error in inserting tutor information")
    conn.close()
    return 'Valid'

#returns all of the supported subjects
def supported_subjects():
    #connect to postgre
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432') 

    #creating a cursor object using cursor()
    cursor = conn.cursor()

    #tempcode for confirming a connection
    cursor.execute('select version()')

    #fetch a single row using fetchone. method fetchmany and fetchall can be used depending on query, this is just verifying db connection
    connectCheck = cursor.fetchone()
    print('Connection established to: ', connectCheck)

    #try catch will fail if the search fails, returning an error message
    try:
        #retrieve the unique list of classes taught
        cursor.execute('select classname from unique_subjects')
        table = cursor.fetchall()
        conn.close()
        #returns a table that contains the list of class names
        return table
    except:
        conn.close()
        return ("Error in retrieving class list")
        
##returns an encrypted password
def encrypt(pwd):
    newPwd = hashlib.sha256(pwd.encode())
    newPwd = newPwd.hexdigest()
    return newPwd

##checks to see if the file is PNG JPEG JPG  
def picVal (imagePath):
    if imghdr.what(imagePath) in ['jpeg','jpg', 'png']:
        return "Valid"
    else:
        return "Not a supported file type.\n"

##validates netID
def idVal (netID):
    if not netID[:3].isalpha() or not netID[3:].isnumeric() or len(netID) != 9:
        return "Not a valid NetID. \n"
    return "Valid"

#validates subject
def subjectVal (subject):
    ##separates the subject at the space character
    sub = subject.split()
    if(len(sub) == 2):
        if not sub[0].isalpha() or not sub[1].isnumeric():
            return "Not a valid subject. \n"
        return "Valid"
    else:
        return "Not a valid subject, please put a space between class name and number \n"

##checks to see if one time value fits in another
def checkTime (time1, time2):
    
    if time1[0] < time2[0] or time1[2] > time2[2]:
        return False
    if (time1[0] == time2[0] and time1[1] < time2[1]) or (time1[2] == time2[2] and time1[3] > time2[3]):
        return False
    return True

#reformats time from the database to 4 ints, [hour1, minute1, hour2, minute2]. 
#the rusults will be in 24-hour time to keep am and pm separate
#ex: 12pm-3pm will become an array [12,0,15,0], for 
def timeFormat(timeSlot):
    
    start_time, end_time = timeSlot.split('-')

    #if there are minute values
    if ":" in timeSlot:
        start_hour, start_min = [val for val in start_time[:-2].split(':')]
        end_hour, end_min = [val for val in end_time[:-2].split(':')]
    #else if there is no minute values
    else:
        start_hour = int(start_time[:-2])
        end_hour = int(end_time[:-2])
        start_min = 0
        end_min = 0

    start_hour = int(start_hour)
    end_hour = int(end_hour)

    if start_time[-2:] == 'pm' and start_hour != 12:
        start_hour += 12

    if end_time[-2:] == 'pm' and end_hour != 12:
        end_hour += 12

    if start_min == '':
        start_min = 0
    if end_min == '':
        end_min = 0
         
    return [int(start_hour), int(start_min), int(end_hour), int(end_min)]

#validates time and day from a givent imeslot
def timeVal (timeSlot):
    ##separates the timeSlot string at the space characters
    try:
        day = timeSlot.split()

        day[1] = day[1].replace("-", ":")
        time = day[1].split(":")

        if not day[0].lower() in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            return "Not a valid day. \n"
        ##checks to see if the time is valid
        if not (int(time[0]) < 25 and int(time[2]) < 25 and int(time[1]) < 60 and int(time[3]) < 60):
            return "Not a valid time. \n"
        return "Valid"
    except Exception as e:
        return "Not a valid day/time. \n"

def usertype_check(net_id):
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432') 
    cursor = conn.cursor()
    try:
        #gets a list of appointments, contains the tutor first and last name, student first and last name, time and date
        cursor.execute(f"select usertype from Person where net_id = '{net_id}'")
        results = cursor.fetchone()
        return results[0]
    except Exception as e:
        print(e)

@app.route('/api/filter', methods=['GET'])
def filter_tutors():
    # Connect to PostgreSQL database 
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432')

    # get filter input from request
    search_query = request.args.get('filter')
    with conn.cursor() as cur:
        # Query all tutors and their subjects from database
        cur.execute("SELECT name, subjects FROM tutors")
        rows = cur.fetchall()

    if search_query:
        filtered_tutors = {}
        # split search query into terms
        search_terms = search_query.split() 
        for row in rows:
            name = row[0]
            subjects = row[1]
            for term in search_terms:
                if term in name or any(subject.startswith(term) for subject in subjects):
                    filtered_tutors.setdefault(name, []).extend(subjects)
                    break
    else:
        filtered_tutors = {row[0]: row[1] for row in rows}
    
    # Convert subjects from comma-separated strings to lists
    for name, subjects in filtered_tutors.items():
        filtered_tutors[name] = [subject.strip() for subject in subjects.split(',')]

    # Create list of tutor dictionaries
    tutor_list = [{'tutor-name': name, 'subjects': subjects} for name, subjects in filtered_tutors.items()]
    conn.close()

    print(tutor_list)
    return jsonify(tutor_list)

if __name__ == '__main__':
    app.run(debug=True)
