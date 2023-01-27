from flask import Flask, render_template, request, jsonify
import json
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        return "hi"
