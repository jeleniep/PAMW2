from flask import Flask
import redis
from flask import request
from flask import make_response
from flask import render_template
import sys
import uuid
from login import Login

login = Login()
login.test()
app = Flask(__name__)
r = redis.Redis(host='db', port=6379, db=0)
r.hset('users', 'test', 'test');

@app.route('/')
def index():
    # r.set('foo', 'bar')
    r.set('lol', 'kol')
    print('tutaj:', r.hget('user', 'test'), flush=True)
    response = make_response(r.get('lol'), 200)
    person = {"passwd": "Lol", "salt": "kolo"}
    r.hmset("test", person)
    # print(r.hgetall("test"), flush=True)
    # print(uuid.uuid4())
    # print(r.hgetall("test"))
    print(login.generate_uuid(), flush=True)
    response.headers["Access-Control-Allow-Origin"] = "http://localhost"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    login.test()
    return render_template("index.html")


@app.route('/login', methods=['POST'])
def loginn():
    r = redis.Redis(host='db', port=6379, db=0)
    username = request.form.get('login')
    password = request.form.get('password')
    print( password, r.hget('users', username).decode('UTF-8'), flush=True)

    if password == r.hget('users', username).decode('UTF-8'):
        new_uuid = login.generate_uuid()
        r.hset('sessions', new_uuid, username)
        print(r.hgetall('sessions'), flush=True)
        response = make_response( render_template("pdfs.html"), 200)
        response.set_cookie('sessionId', new_uuid)
        response.headers["Access-Control-Allow-Origin"] = "http://localhost"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    return 'Złe hasło'