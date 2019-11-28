from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", who="Marcin Najman", numbers=[1, 2])

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username is None or password is None:
        return render_template("error.html")
    if username == 'test' and password =="test":
        return render_template("profile.html")
    return render_template("error.html")
