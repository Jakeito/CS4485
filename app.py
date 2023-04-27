from flask import Flask, render_template, request, jsonify, redirect, session, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import json
from datetime import datetime
from datetime import timedelta
import psycopg2
import hashlib
import imghdr
import uuid
import sys, os
from flask_login import *
from werkzeug.utils import secure_filename
import secrets
import string

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

        #connect to postgre
        conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432') 

        #creating a cursor object using cursor()
        cursor = conn.cursor()
    
        try:
            #inserting data into DB
            cursor.execute(f"select hashed_pw from login where net_id = '{username_input}'")
            results = cursor.fetchone()
        except Exception as e:
            print(e)
            conn.close()
            return 'Invalid username or password'
        if results is not None and hashed == results[0]:
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
@app.route('/api/check-favorite')
def check_favorites():
    # get id
    id = session['key']
    tutor_id = request.args.get('net-id')

    # Execute a SELECT statement to retrieve the user's fav list from the database
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432')
    cursor = conn.cursor() 
    cursor.execute("SELECT tutor_id FROM FavoriteTutors WHERE student_id = %s and tutor_id = %s", (id, tutor_id))

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
            return 'Error with picture'
        pic = request.files['file']
        if pic.filename == '':
            print('no file')
            return 'Error with picture'
        filename = secure_filename(pic.filename)
        if not filename.endswith('png') and not filename.endswith('jpeg') and not filename.endswith('jpg'):
            return 'Wrong file extension'
        path = app.config['UPLOAD_FOLDER'] + net_id
        extension = filename.split('.')
        if not os.path.exists(path):
            os.makedirs(path)
        pic.save(os.path.join(app.config['UPLOAD_FOLDER'] + net_id + '/', net_id + '.png'))
    except Exception as e:
        print(e)
        return('Error with picture')
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
def appointmentCreation():
    if request.method == 'POST':
        student_id = session['key']
        tutor_id = request.args.get('net-id')
        result = request.json
        day = result['date'].split(" ")[0]
        day = dayParse(day)
        date = f'{result["date"].split(" ")[1]}-{result["date"].split(" ")[2]}-{result["date"].split(" ")[3]}'
        start_time = result['date'].split(" ")[4]
        start_time = start_time[:-3]
        time = datetime.strptime(start_time, '%H:%M')
        end_time = time + timedelta(minutes=30)
        end_time = end_time.strftime('%H:%M')
        timeSlot = f'{start_time}-{end_time}'
        alphabet = string.ascii_letters + string.digits
        session_id = ''.join(secrets.choice(alphabet) for i in range(10))
        
        timeSlot_status = timeVal(f"{day} {timeSlot}")
        available = checkAvailability(tutor_id, day, date, timeSlot)

        if timeSlot_status == 'Valid' and available:
            appointment_status = insertAppointment (session_id, tutor_id, student_id, day, timeSlot, date)
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
        cursor.execute(f"select net_id, fname, mname, lname, hours_completed from Tutors where net_id = '{id}'")
        tutor_personal_info = cursor.fetchone()
        tutor_dict = {
            'net-id': tutor_personal_info[0],
            'first-name': tutor_personal_info[1],
            'middle-name': tutor_personal_info[2],
            'last-name': tutor_personal_info[3],
            'hours': tutor_personal_info[4]
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
        cursor.execute("SELECT t.fname AS tutor_fname, t.lname AS tutor_lname, s.fname AS student_fname, s.lname AS student_lname, ta.time, ta.date FROM TutorApts ta INNER JOIN Person t ON ta.tutor_id = t.net_id INNER JOIN Person s ON ta.student_id = s.net_id WHERE ta.tutor_id = %s OR ta.student_id = %s;", (id, id))
        results = cursor.fetchall()

        #if there are no appointments made with that ID
        if cursor.rowcount == 0:
            conn.close()
            return "No appointments with that ID"

        #sorts the results based on date
        results = sorted(results, key=lambda x: x[-1])
        conn.close()
        return results
    
    except Exception as e: 
        conn.close()
        print(e)
        return "Error, could not find appointments"

#checks to see if an appointment has passed, if it has it removes it and adds it to the user's hours
@app.route('/api/check-appointment', methods=['POST'])
def checkPassedAppointments():
    #get id
    id = session['key']

    #gets the current date and time when the function is called
    currentDateTime = datetime.now()
    time = currentDateTime.time()
    date = currentDateTime.date()
    format = '%b-%d-%Y'
    format2 = '%H:%M'

    #connects
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432') 
    cursor = conn.cursor()

    try:
        #grabs a list of the appointments that contain the id
        cursor.execute("SELECT * FROM TutorApts WHERE tutor_id = %s OR student_id = %s", (id, id))
        results = cursor.fetchall()

        #if there are no appointments
        if cursor.rowcount == 0:
            conn.close()
            return "No appointments with that ID"
        
        #sorts the results based on date (not sorted based on time if there is more than one on a given date)
        results = sorted(results, key=lambda x: x[-1])

        #goes through every result and sees if it is past the date
        for x in results:
            aptDate = datetime.strptime(x[5], format).date()
            completedHours = completed_hours_calc(x[4])

            #if it is before the date
            if aptDate < date:
                #removes the appointment
                cursor.execute(f"DELETE FROM TutorApts WHERE date = '{x[5]}'")
                conn.commit()

                #adds the hours to the student and tutor accounts
                cursor.execute(f"UPDATE Person SET hours_completed = hours_completed+{completedHours} WHERE net_id = '{x[1]}'")
                conn.commit()
                cursor.execute(f"UPDATE Person SET hours_completed = hours_completed+{completedHours} WHERE net_id = '{x[2]}'")
                conn.commit()
            
            #if the appointment is today
            elif aptDate == date:
                aptTime = x[4].split('-')
                aptTime = aptTime[1]
                aptTime = datetime.strptime(aptTime, format2).time()

                if (aptTime < time):
                    #removes the appointment
                    cursor.execute(f"DELETE FROM TutorApts WHERE date = '{x[5]}'")
                    conn.commit()

                    #adds the hours to the student and tutor accounts
                    cursor.execute("UPDATE Person SET hours_completed = hours_completed+%d WHERE net_id = %s",(completedHours, x[1]))
                    conn.commit()
                    cursor.execute("UPDATE Person SET hours_completed = hours_completed+%d WHERE net_id = %s",(completedHours, x[2]))
                    conn.commit()
                else:
                    break
                
            #if there is no more appointments that have passed
            else:
                continue

        #returns the amount of appointments removed. will return the string even if it deletes no appointments
        conn.close()
        return "Removed appointment and added them to completed hours."
    except Exception as e: 
        conn.close()
        print(e)
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
        cursor.execute(f"select net_id, fname, mname, lname, hours_completed from Tutors where net_id = '{id}'")
        tutor_personal_info = cursor.fetchone()
        tutor_dict = {
            'net-id': tutor_personal_info[0],
            'first-name': tutor_personal_info[1],
            'middle-name': tutor_personal_info[2],
            'last-name': tutor_personal_info[3],
            'hours': tutor_personal_info[4]
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
    
@app.route('/api/filter', methods=['GET'])
def filter_tutors():
    search_string = request.args.get('filter')
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432') 
    cursor = conn.cursor()

    try:
        #get list of net-id's with first, middle, or last name that fits search string
        cursor.execute('select net_id from tutors where fname ilike \'%{}%\' or mname ilike \'%{}%\' or lname ilike \'%{}%\' '.format(search_string, search_string, search_string))
        dirty_name_net_ids = cursor.fetchall()
        clean_name_net_ids = []
            #add each valid net id to list 
        for element in dirty_name_net_ids:
            clean_name_net_ids.append(element[0])
            
        #get list of net-id's with class name that contains search string
        cursor.execute('select tutor_id from SubjectList where classname ilike \'%{}%\' '.format(search_string))
        dirty_class_net_ids = cursor.fetchall()
        clean_class_net_ids = []
            #add each valid net id to list 
        for element in dirty_class_net_ids:
            clean_class_net_ids.append(element[0])

        #create a union set of the two lists
        tutor_list_clean = list(set(clean_name_net_ids) | set(clean_class_net_ids))

        #for each element in aggregated list, dict the information based on the net-id
            #setting up the dict array
        info_dict_array = []
        for tutor in tutor_list_clean:
            #get tutor full name
            cursor.execute('select net_id, fname, mname, lname, hours_completed from Tutors where net_id = \'' + tutor + '\'')
            tutor_personal_info = cursor.fetchone()
            tutor_dict = {
                'net-id': tutor_personal_info[0],
                'first-name': tutor_personal_info[1],
                'middle-name': tutor_personal_info[2],
                'last-name': tutor_personal_info[3],
                'hours-completed': tutor_personal_info[4]
            }

            #get tutor subjects
            cursor.execute('select classname from SubjectList where tutor_id = \''+ tutor +'\'')
            class_list = cursor.fetchall()
            class_list_clean = []
            for element in class_list:
                class_list_clean.append(element[0])
            tutor_dict.update({'subjects': class_list_clean})
            info_dict_array.append(tutor_dict)
            
        conn.close()
        return info_dict_array
    except Exception as e :
        conn.close()
        return('Error' + repr(e))

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
def insertAppointment(session_id, tutor_id, student_id, day, time, date):
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432')
    cursor = conn.cursor()
    try:
        cursor.execute(f"insert into TutorApts (session_id, tutor_id, student_id, day, time, date) values ('{session_id}', '{tutor_id}', '{student_id}', '{day}', '{time}', '{date}')")
        conn.commit()
    except Exception as e:
        print(e)
        return ("Error, appointment could not be created")
    conn.close()
    return 'Success'

##checks if the tutor has an available timeslot, returns a boolean
def checkAvailability(tutor_id, day, date, timeSlot):
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432')
    cursor = conn.cursor()
    check = False
    try:
        ##gets the tutors available days
        cursor.execute("SELECT time FROM TutorAvailability WHERE tutor_id = %s AND day = %s", (tutor_id, day))
        results = cursor.fetchall()

        if cursor.rowcount == 0:
            conn.close()
            return False
        
        #checks if the selected time is in the tutors available hours
        for x in results:
            if checkTime(timeSlot, x[0]):
                check = True

        if check == False:
            conn.close()
            return check
        
        ##checks to see if an apointment is already schedules in that time slot
        cursor.execute("SELECT * FROM TutorApts WHERE tutor_id = %s AND day = %s AND date = %s", (tutor_id, day, date))
        results = cursor.fetchall()
        if cursor.rowcount != 0:
            for i in results:
                startInputTime = datetime.strptime(timeSlot.split('-')[0], '%H:%M')
                endInputTime = datetime.strptime(timeSlot.split('-')[1], '%H:%M')
                startExistingTime = datetime.strptime(i[4].split('-')[0], '%H:%M')
                endExistingTime = datetime.strptime(i[4].split('-')[1], '%H:%M')
                if (startInputTime >= startExistingTime and startInputTime <= endExistingTime) or (endInputTime >= startExistingTime and endInputTime <= endExistingTime):
                    check = False
            conn.close()
    except Exception as e:
        conn.close()
        print(e)
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
        
        for x in availability_array:
            #making sure to cull accidental newlines
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
    time1 = time1.split('-')
    startInput = datetime.strptime(time1[0], '%H:%M')
    endInput = datetime.strptime(time1[1], '%H:%M')
    time2 = time2.split('-')
    startExist = datetime.strptime(time2[0], '%H:%M')
    endExist = datetime.strptime(time2[1], '%H:%M')
    if startInput < startExist or endInput > endExist:
        return False
    return True

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
        print(e)
        return "Not a valid day/time. \n"
    
#parse day name abbreviations to actual day names
def dayParse(day):
    try:
        if day == 'Sun':
            return 'Sunday'
        elif day == 'Mon':
            return 'Monday'
        elif day == 'Tue':
            return 'Tuesday'
        elif day == 'Wed':
            return 'Wednesday'
        elif day == 'Thu':
            return 'Thursday'
        elif day == 'Fri':
            return 'Friday'
        elif day == 'Sat':
            return 'Saturday'
    except Exception as e:
        print(e)

def completed_hours_calc(timeslot):
    times = timeslot.split('-')
    hour1 = int(times[0].split(':')[0])
    hour2 = int(times[1].split(':')[0])
    minute1 = int(times[0].split(':')[1])
    minute2 = int(times[0].split(':')[1])

    hours = hour2 - hour1
    minutes = minute2 - minute1
    if minutes == -30:
        minutes = -.5
    else:
        minutes = .5
    completed_hours = hours + minutes
    return completed_hours

def usertype_check(net_id):
    conn = psycopg2.connect(database='Tutoring', user='postgres', password='1234', host='localhost', port='5432') 
    cursor = conn.cursor()
    try:
        #gets a list of appointments, contains the tutor first and last name, student first and last name, time and date
        cursor.execute(f"select usertype from Person where net_id = '{net_id}'")
        results = cursor.fetchone()
        return results[0]
    except Exception as e:
        print('User does not exist')

if __name__ == '__main__':
    app.run(debug=True)
