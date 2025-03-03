#!/usr/bin/env python3

from sqlite3 import *
from os import system
from flask import Flask, request, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["50000 per hour"],
    storage_uri="memory://",
)

RESERVED = sorted([i.lower().strip() for i in open("sqlite_reserved.txt")], key=len, reverse=True)

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
            CREATE TABLE authors(first, middle, last)
        ''')
        cur.execute('''
            INSERT INTO authors VALUES
                ("Tobias", '', "Smollett"),
                ("William", '', "Shakespeare"),
                ("Edward", "Morgan", "Forster"),
                ("George", "", "Eliot"),
                ("Louisa", "May", "Alcott"),
                ("Lucy", "Maud", "Montgomery"),
                ("Frank", "T.", "Merill"),
                ("Herman", "", "Melville"),
                ("Alexandre", "", "Dumas"),
                ("Elizabeth", "", "Von Arnim")
        ''')
        cur.execute('''
            CREATE TABLE users(username, passwords)
        ''')
        cur.execute(f'''
            INSERT INTO users VALUES
                ("admin", "{open("flag.txt").read()}")
        ''')


def sanitize(s):
    s = s.lower()
    for keyword in RESERVED:
        while keyword in s:
            s = s.replace(keyword, '')
    return s

@app.route('/', methods=["GET"])
@limiter.limit("2/second")
def index():
    if 'lastname' not in request.args:
        return open("index.html").read()
    else:
        with Db() as cur:
            lastname = sanitize(request.args['lastname'])
            res = cur.execute(f"SELECT * from authors where last LIKE '%{lastname}%'")
            ret = '<table>'
            ret += '<tr><th>First Name</th> <th>Middle Name</th> <th>Last Name</th></tr>'
            for row in res:
                ret += '<tr>'
                for entry in row:
                    ret += f"<td>{entry}</td>"
                ret += '</tr>'
            ret += '</table>'
            return ret

@app.route('/source')
@limiter.limit("2/second")
def source():
    return Response(open(__file__).read(), mimetype="text/plain")

@app.route('/blacklist')
@limiter.limit("2/second")
def blacklist():
    return Response(open("sqlite_reserved.txt").read(), mimetype="text/plain")

if __name__ == "__main__":
    initDb()
    app.run('0.0.0.0', 10005)