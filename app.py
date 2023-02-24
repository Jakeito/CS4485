from flask import Flask, render_template, request, jsonify, redirect
import json
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

@app.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

@app.route('/signin', methods=['GET'])
def signin():
    return render_template('signin.html')
