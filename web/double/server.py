#!/usr/bin/env python3

from flask import Flask, request, Response, redirect, render_template_string
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from uuid import uuid4

import json
from datetime import datetime

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["50000 per hour"],
    storage_uri="memory://",
)

default_blob = [
    {
        "repo_name": "my_org/cool_repo",
        "flaky_tests": 9001,
        "prs_blocked": 2,
        "time_lost": "30s"
    }
]
  
@app.route('/')
@limiter.limit("5/second")
def index():
    return Response(open("index.html").read())

@app.route('/gen_email', methods=["POST"])
@limiter.limit("5/second")
def gen_email():
    blob = request.form["blob"]
    try:
        blob = json.loads(blob)
    except Exception as e:
        print(e)
        blob = default_blob
    ret = '''
    <h1>Repo Stats</h1>
    <h2>{{ date }}</h2>
    <table>
    <tr>
        <th>Repo Name</th>
        <th>Flaky or Broken Tests</th>
        <th>PRs Blocked</th>
        <th>Time lost</th>
    </tr>
    '''
    for obj in blob:
        ret += render_template_string('''<tr>
            <td>{{ repo_name }}</td>
            <td>{{ flaky_tests }}</td>
            <td>{{ prs_blocked }}</td>
            <td>{{ time_lost }}</td>
        </tr>''', **obj)
    ret += "</table>"
    print(ret)
    return render_template_string(ret, date=datetime.today().strftime('%Y-%m-%d'))
    

@app.route('/source')
@limiter.limit("5/second")
def source():
    return Response(open(__file__).read(), mimetype='text/plain')

@app.route('/docker')
@limiter.limit("5/second")
def docker():
    return Response(open("Dockerfile").read(), mimetype='text/plain')

app.run('0.0.0.0', 10006)