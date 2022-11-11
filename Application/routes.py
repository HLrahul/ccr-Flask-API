# from crypt import methods
from flask import request, jsonify, make_response,  render_template
from Application import app
from Application.models import User
from Application.database import db

@app.route('/')
def home():
    return render_template('Header.html')

@app.route('/signup', methods=['POST'])
def CreateUser():
    return User().signup()

@app.route('/listUsers', methods=['GET'])
def listUsers():
    usersList = []
    
    collection = db['users']
    for user in collection.find({}):
        usersList.append(user)

    return jsonify(usersList), 200

@app.route('/signout')
def signout():
    return User().signout()

@app.route('/deleteAccount', methods=['DELETE'])
def deleteAccount():
    return User().deleteAccount()