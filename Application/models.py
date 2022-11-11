import collections
import email
import json
from flask import request, jsonify, session
from Application.database import db
from passlib.hash import pbkdf2_sha256
import uuid

class User():

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user

        msg = "Successfully created a Session!"
        return jsonify(msg, user), 200

    def signup(self):
        credentials = request.json
        
        user = {
            "_id": uuid.uuid4().hex,
            "name": credentials["name"],
            "email": credentials["email"],
            "password": credentials["password"]
        }

        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        collection = db['users']
        if collection.find_one({ "email": user['email'] }):
            return jsonify({ "msg": "User already exists!" }), 400
        if collection.find_one({ "name": user['name'] }):
            return "UserName already taken, try different name!", 400
        if collection.insert_one(user):
            return self.start_session(user)
            # return jsonify({ "msg": "User added successfully!" }), 200

        return jsonify({ "Error": "Something went wrong" }), 400

    def signout(self):
        session.clear()

        return "U have successfully signed out!", 200

    def deleteAccount(self):
        credentials = request.json
        collection = db['users']

        if collection.find_one({ "email" : credentials['email'] }):
            collection.delete_one({ "email" : credentials['email'] })
            return "The Account has been deleted successfully!", 200

        return "Account not found!", 400