#!/usr/bin/env python3

from flask import Flask, request, Response, redirect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from uuid import uuid4
import secrets

from sqlite3 import *
from os import system


app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["50000 per hour"],
    storage_uri="memory://",
)

HEADER = '''
        <h1>StatusEffect</h1>
        <h2 style='color:red'>For When You're On Fire</h2>
        <br>
        '''

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
            CREATE TABLE accounts(id, name, token)
        ''')
        cur.execute('''
            CREATE TABLE products(id, name, accountId, publicStatus, privateStatus)
        ''')
    create_acc("admin")
    product_id = create_product("admin", "Five-Nines-Service")
    with Db() as cur:
        cur.execute("UPDATE products SET privateStatus = ? WHERE id = ?", (open('flag.txt').read(), product_id))

def create_acc(username):
    with Db() as cur:
        res = cur.execute("SELECT id from accounts WHERE name = ?", (username,))
        if len(res.fetchall()):
            return None
        id_ = str(uuid4())
        token = secrets.token_bytes(16).hex()
        cur.execute("INSERT INTO accounts VALUES (?, ?, ?)", (id_, username, token))
        return token

def get_user_id(username):
    with Db() as cur:
        res = cur.execute("SELECT id from accounts WHERE name = ?", (username,))
        return res.fetchall()[0][0]

def create_product(username, product_name):
    user_id = get_user_id(username)
    with Db() as cur:
        res = cur.execute("SELECT id from products WHERE accountId = ? AND name = ?", (user_id, product_name))
        if len(res.fetchall()):
            return None
        product_id = str(uuid4())
        cur.execute("INSERT INTO products VALUES (?, ?, ?, 'Normal', 'Normal')", (product_id, product_name, user_id))
        return product_id

def get_product_id(username=None, user_id=None, product_name=None):
    if username and not user_id:
        user_id = get_user_id(username)
    with Db() as cur:
        res = cur.execute("SELECT id from products WHERE accountId = ? and name = ?", (user_id, product_name))
        return res.fetchall()[0][0]

def get_user_id_from_product(product_id):
    with Db() as cur:
        res = cur.execute("SELECT accounts.id from accounts JOIN products ON accounts.id = products.accountId WHERE products.id = ?", (product_id,))
        return res.fetchall()[0][0]

def get_public_status(product_id):
    with Db() as cur:
        res = cur.execute("SELECT publicStatus from products WHERE products.id = ?", (product_id,))
        return res.fetchall()[0][0]

def get_private_status(product_id):
    with Db() as cur:
        res = cur.execute("SELECT privateStatus from products WHERE products.id = ?", (product_id,))
        return res.fetchall()[0][0]

def get_names_from_product(product_id):
    with Db() as cur:
        res = cur.execute("SELECT accounts.name, products.name from accounts JOIN products ON accounts.id = products.accountId WHERE products.id = ?", (product_id,))
        return res.fetchall()[0]

def auth(token=None, username=None, user_id=None, product_name=None, product_id=None):
    valid = False
    if username and not user_id:
        user_id = get_user_id(username)
    if user_id and product_name and not product_id:
        product_id = get_product_id(user_id=user_id, product_name=product_name)
    if product_id and not user_id:
        user_id = get_user_id_from_product(product_id)
    if not valid and user_id and product_id:
        with Db() as cur:
            res = cur.execute(
                '''SELECT * FROM products JOIN accounts ON accounts.id = products.accountId
                        WHERE accounts.token = ? and accounts.id = ? and products.id = ?''',
                (token, user_id, product_id)
            )
            valid = len(res.fetchall()) > 0
    if not valid and user_id:
        with Db() as cur:
            res = cur.execute(
                '''SELECT * FROM accounts WHERE accounts.token = ? and accounts.id = ?''',
                (token, user_id)
            )
            valid = len(res.fetchall()) > 0    
    return valid 

@app.route('/')
@limiter.limit("5/second")
def index():
    return Response(open("index.html").read())

@app.route('/create_account', methods=['POST'])
@limiter.limit("5/second")
def create_account():
    username = request.form["username"]
    token = create_acc(username)
    if token:
        resp = redirect(f"/{username}", 302)
        resp.set_cookie("token", token)
        return resp
    return Response("That account name already exists!", 400)

@app.route('/<username>', methods=['GET'])
@limiter.limit("5/second")
def user_get(username):
    token=request.cookies.get("token")
    user_id = get_user_id(username)
    authed = auth(token=token, user_id=user_id)

    ret = HEADER
    if not authed:
        ret += '''
        You don't have permission to see this. Please enter a valid API token to view this content.<br>
        <input type="text" 
            value=""
            style="width:300px"
            id="tokenbox"/>
        <button onClick="document.cookie='token='+document.getElementById('tokenbox').value;location.reload()"/>
            Create!
        </button>
        '''
        return ret
    ret += f"""
    Your API token is: <code>{token}</code><br>
    <h4>Create a Product!</h4>
    <form action="/create_product/{username}" method="post">
        Product Name: <input name="product_name" id='product_name' cols="15" placeholder=""></input>
        <input type="submit" value="Create!"></input>
    </form>
    <br>
    <h3>Your products:</h3>
    <ul>
    """
    with Db() as cur:
        res = cur.execute("SELECT name from products WHERE accountId = ?", (user_id,))
        for row in res:
            ret += f"<li><a href='/{username}/{row[0]}'>{row[0]}</a></li>"
    ret += "</ul>"
    return ret

@app.route('/create_product/<username>', methods=['POST'])
@limiter.limit("5/second")
def create_product_endpoint(username):
    product_name = request.form["product_name"]
    token = request.cookies.get("token")
    authed = auth(token=token, username=username)
    if not authed:
        return Response("Forbidden", 403)
    product_id = create_product(username, product_name)
    if not product_id:
        return Response("You already have a product with that name!", 400)
    return redirect(f"/{username}/{product_name}")

@app.route('/get_public_status', methods=['GET'])
@limiter.limit("5/second")
def get_public_status_endpoint():
    return get_public_status(request.args.get("product_id"))

@app.route('/get_private_status', methods=['GET'])
@limiter.limit("5/second")
def get_private_status_endpoint():
    username = request.args.get("username")
    product_name = request.args.get("product_name")
    user_id = request.args.get("user_id")
    product_id = request.args.get("product_id")
    token = request.cookies.get("token")

    authed = auth(token=token, username=username, product_name=product_name, user_id=user_id, product_id=product_id)
    if not authed:
        return Response("Forbidden", 403)
    return get_private_status(request.args.get("product_id"))

@app.route('/set_public_status/<product_id>', methods=['POST'])
@limiter.limit("5/second")
def set_public_status(product_id):
    token = request.cookies.get("token")
    authed = auth(token=token, product_id=product_id)
    if not authed:
        return Response("Forbidden", 403)
    with Db() as cur:
        cur.execute("UPDATE products SET publicStatus = ? WHERE id = ?", (request.form['status'], product_id))
    username, product_name = get_names_from_product(product_id)
    return redirect(f"/{username}/{product_name}", 302)

@app.route('/set_private_status/<product_id>', methods=['POST'])
@limiter.limit("5/second")
def set_private_status(product_id):
    token = request.cookies.get("token")
    authed = auth(token=token, product_id=product_id)
    if not authed:
        return Response("Forbidden", 403)
    with Db() as cur:
        cur.execute("UPDATE products SET privateStatus = ? WHERE id = ?", (request.form['status'], product_id))
    username, product_name = get_names_from_product(product_id)
    return redirect(f"/{username}/{product_name}", 302)

@app.route('/<username>/<product_name>', methods=['GET'])
@limiter.limit("5/second")
def product_get(username, product_name):
    token = request.cookies.get("token")
    authed = auth(token=token, username=username, product_name=product_name)

    product_id = get_product_id(username=username, product_name=product_name)
    public_status = get_public_status(product_id)
    
    ret = HEADER
    ret += f'''
    <h3>Product {product_name}</h3><br>
    <h4>Public Status: {public_status}</h4>
    <form action="/set_public_status/{product_id}" method="post">
        Update public status: <input name="status" id='status' cols="15" placeholder=""></input>
        <input type="submit" value="Update"></input>
    </form>

    '''

    if not authed:
        return ret
    private_status = get_private_status(product_id)
    ret += f'''
    <br><br>
    <h4>Private Status: {private_status}</h4>
    <form action="/set_private_status/{product_id}" method="post">
        Update private status: <input name="status" id='status' cols="15" placeholder=""></input>
        <input type="submit" value="Update"></input>
    </form>
    '''
    return ret

@app.route('/source')
@limiter.limit("5/second")
def source():
    return Response(open(__file__).read(), mimetype='text/plain')

@app.route('/docker')
@limiter.limit("5/second")
def docker():
    return Response(open("Dockerfile").read(), mimetype='text/plain')

initDb()
app.run('0.0.0.0', 10002)