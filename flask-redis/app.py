from flask import Flask
import redis
from flask import request, make_response, render_template, send_file, redirect, Response
import sys
import uuid
import requests
from login import Login
from datetime import datetime, timedelta
import jwt

login = Login()
login.test()
app = Flask(__name__)
key = 'secret'

r = redis.Redis(host='db', port=6379, db=0)
ip = "192.168.0.59:8080"
r.hset('users', 'test', 'test')

def checkAuth(sessionId):
    print(sessionId)
    if sessionId is not None and r.hget('sessions', sessionId):
        return True
    return False

@app.route('/')
def index():
    if checkAuth(request.cookies.get('sessionId')):
        exp = datetime.now() + timedelta(minutes = 2)
        jwt_token_send_pdf = jwt.encode({'user': r.hget('sessions', request.cookies.get('sessionId')).decode('UTF-8'), 'exp': exp.timestamp() }, key, algorithm='HS256')
        res = requests.get("http://"+ ip +"/getPdfList", headers={'Authorization': jwt_token_send_pdf})
        response = make_response( render_template("pdfs.html", files=res.json()), 200)       
        return response
    response = make_response(render_template("index.html"), 200)
    return response


@app.route('/login', methods=['POST'])
def loginToPdfScreen():
    username = request.form.get('login')
    password = request.form.get('password')
    if password == r.hget('users', username).decode('UTF-8'):
        new_uuid = login.generate_uuid()
        r.hset('sessions', new_uuid, username)
        exp = datetime.now() + timedelta(minutes = 2)
        jwt_token_send_pdf = jwt.encode({'user': username, 'exp': exp.timestamp() }, key, algorithm='HS256')
        res = requests.get("http://"+ ip +"/getPdfList", headers={'Authorization': jwt_token_send_pdf})
        response = make_response( render_template("pdfs.html", files=res.json()), 200)
        response.set_cookie('sessionId', new_uuid)
        return response
    response = make_response(render_template("index.html"), 401)
    return response

@app.route('/addPdf', methods=['POST'])
def addPdf():
    if not checkAuth(request.cookies.get('sessionId')):
        response = make_response( render_template("index.html"), 401)
        response.headers["Access-Control-Allow-Origin"] = "http://localhost"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    exp = datetime.now() + timedelta(minutes = 2)
    jwt_token_send_pdf = jwt.encode({'user': r.hget('sessions', request.cookies.get('sessionId')).decode('UTF-8'), 'exp': exp.timestamp() }, key, algorithm='HS256')
    file = request.files.get('pdf');
    fileDict = { file.filename : file }
    requests.post("http://"+ ip +"/addPdf", files=fileDict, headers={'Authorization': jwt_token_send_pdf})
    res = requests.get("http://"+ ip +"/getPdfList", headers={'Authorization': jwt_token_send_pdf})
    response = make_response( render_template("pdfs.html", files=res.json()), 200)
    return response

@app.route('/logout')
def logout():
    r.hdel('sessions', request.cookies.get('sessionId'))
    response = make_response( render_template("index.html"), 200)
    response.headers["Access-Control-Allow-Origin"] = "http://localhost"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route('/getPdf')
def getPdf():
    exp = datetime.now() + timedelta(minutes = 2)
    jwt_token_send_pdf = jwt.encode({'user': r.hget('sessions', request.cookies.get('sessionId')).decode('UTF-8'), 'exp': exp.timestamp() }, key, algorithm='HS256')
    redir = redirect("http://"+ ip +"/getPdf/"+request.args['name']+'?token='+jwt_token_send_pdf.decode('UTF-8'))
    return redir

