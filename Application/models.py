from flask import request, jsonify
from Application.database import db
from passlib.hash import pbkdf2_sha256
import uuid

class User():

    def signup(self):
        credentials = request.json
        print(request)
        
        user = {
            "_id": uuid.uuid4().hex,
            "name": credentials["name"],
            "email": credentials["email"],
            "password": credentials["password"]
        }

        # user['password'] = pbkdf2_sha256.encrypt(user['password'])

        if db.users.find_one({ "email": user['email'] }):
            return jsonify({ "msg": "User already exists!" }), 400
        if db.users.insert_one(user):
            return jsonify({ "msg": "User added successfully!" }), 200

        return jsonify({ "Error": "Something went wrong" }), 400