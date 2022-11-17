# from crypt import methods
from flask import request, jsonify, render_template, session, redirect
from functools import wraps
from Application import app
from Application.models import User
from Application.database import db


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/login')

    return wrap

@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/signup', methods=['GET','POST'])
def CreateUser():
    if request.method == 'POST':
        res = User().signup()
        if res == "Successfully Registered! Login to go to Dashboard!":
            return render_template('signup.html', msg = res)
        else:
            return render_template('signup.html', msg = res)

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        res = User().login()
        if res != "User Doesn't Exist":
            logger = db['users'].find_one({ "email": request.form.get('email') })
            if logger['role'] == 'agent':
                return render_template('admindashboard.html', msg = res)
            else:
                return render_template('dashboard.html', msg = res)
        else:
            return render_template('login.html', msg = res)

    return render_template('login.html')

@app.route('/listUsers', methods=['GET'])
def listUsers():
    usersList = []
    
    collection = db['users']
    for user in collection.find({}):
        usersList.append(user)

    return render_template('listusers.html', res = usersList)

@app.route('/signout')
def signout():
    return User().signout()

@app.route('/deleteAccount', methods=['DELETE'])
def deleteAccount():
    return User().deleteAccount()