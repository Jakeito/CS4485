from flask import Flask, render_template, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
import json
import hashlib
import uuid

app = Flask(__name__)

# using SQLAlchemy to connect to a POstgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/Tutoring'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'
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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

@app.route('/login', methods=['POST'])
def login():
    # extract login credentials from request body
    credentials = request.get_json()
    username = credentials['username']
    password = credentials['password']

    # connect to database and retrieve user with matching credentials
    user = User.query.filter_by(username=username, password=password).first()

    # if user exists, generate token and return success response
    if user is not None:
        # generate and store access token for user
        token = str(uuid.uuid4())
        user.token = token
        db.session.commit()
        
        # return success response with token
        response = {
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }
        return jsonify(response), 200
    
    # if user does not exist, return error response
    else:
        response = {
            'message': 'Invalid username or password'
        }
        return jsonify(response), 401

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
