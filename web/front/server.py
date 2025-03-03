#!/usr/bin/env python3

from flask import Flask, request, Response, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from uuid import uuid4

from sqlite3 import *
from os import system
import traceback


app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["50000 per hour"],
    storage_uri="memory://",
)

class Db(object):
    def __init__(self):
        self.con = connect("db.db")
        self.cur = self.con.cursor()

    def __enter__(self):
        return self.cur

    def __exit__(self, type, value, traceback):
        self.con.commit()
        self.cur.close()
        self.con.close()

def initDb():
    system("rm -f db.db")
    with Db() as cur:
        cur.execute('''
            CREATE TABLE users (name, pass)
        ''')
        cur.execute(f'''
            INSERT INTO users VALUES ('admin', '{str(uuid4())}')
        ''')
        
    
@app.route('/')
@limiter.limit("5/second")
def index():
    return Response(open("index.html").read())


@app.route('/login', methods=["POST"])
@limiter.limit("5/second")
def login():
    user = request.form['user']
    pwd = request.form['pwd']
    try:
        query = f"SELECT * FROM users WHERE name = '{user}' and pass = '{pwd}'"
        with Db() as cur:
            res = cur.execute(query)
            if len(res.fetchall()) > 0:
                return open("flag.txt").read()
            else: 
                return "Sorry, we were unable to log you in."
    except Exception:
        ret = f'''Encountered error trying to login!

Query:
{query}

Traceback:
{traceback.format_exc()}
        '''
        return Response(ret, mimetype='text/plain')


@app.route('/source')
@limiter.limit("5/second")
def source():
    return Response(open(__file__).read(), mimetype='text/plain')

@app.route('/docker')
@limiter.limit("5/second")
def docker():
    return Response(open("Dockerfile").read(), mimetype='text/plain')

initDb()
app.run('0.0.0.0', 10004)