from flask import request, jsonify, make_response
from Application import app
from Application.models import User

@app.route('/ccrapi/signup', methods=['POST'])
def CreateUser():
    return User().signup()
