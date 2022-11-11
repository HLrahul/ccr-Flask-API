# from crypt import methods
from operator import imod
from flask import request, jsonify, make_response
from Application import app
from Application.models import User
from Application.database import db

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
