from flask import Flask, render_template, request, jsonify, redirect, session
from flask_sqlalchemy import SQLAlchemy
import json
import hashlib
import uuid

app = Flask(__name__)

# using SQLAlchemy to connect to a POstgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/Tutoring'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'
SESSION_TYPE = 'sqlalchemy'
db = SQLAlchemy(app)

@app.route('/', methods=['GET'])
def redir():
    return redirect('/home')

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/signin', methods=['GET'])
def signin():
    return render_template('signin.html')

@app.route('/profile/<id>')
def show_profile(id):
    return render_template('profile.html') #This page should be able to change based on user (tutor vs student) (jxy123456 vs plt654321)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

@app.route('/api/login', methods=['POST'])
def login():
    # extract login credentials from request body
    credentials = request.json()
    username_input = credentials['net-id']
    password_input = credentials['password']

    # connect to database and retrieve user with matching credentials
    user = User.query.filter_by(username=username_input, password=password_input).first()

    # if user exists, generate token and return success response
    if user is not None:
        # generate and store access token for user
        token = str(uuid.uuid4())
        user.token = token
        session['key'] = username_input
        
        # return success response with token
        response = {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }
        return response
    
    # if user does not exist, return error response
    else:
        return 'Invalid username or password'

##checks if the password contains 12 character, upper and lower case character, and a number
##returns a boolean and sends a message to front end display
def strongPWD (pwd):
    check = True
    weakPass = ""
    
    if len(pwd) < 12:
        check = False
        weakPass += "Password needs to be at least 12 character. "

    if pwd.islower() or pwd.isupper():
        check = False
        weakPass += "Password needs at least 1 upper and 1 lower case character. "
    
    if any(i.isdigit() for i in pwd) == False:
        check = False
        weakPass += "Password needs at least one number. "

    if check:
        return "Strong"
    else:
        return weakPass

    return check

##returns an encrypted password
def encrypt (pwd):
    newPwd = hashlib.sha256(pwd.encode())
    newPwd = newPwd.hexdigest()
    return newPwd
