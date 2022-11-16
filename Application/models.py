import collections
import email
import json
from flask import request, jsonify, session, redirect
from Application.database import db
from passlib.hash import pbkdf2_sha256
import uuid

class User():

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user

        return "Session created"

    def signup(self):
        
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
        }
        re_pass = request.form.get('retyped-password')

        if user['password'] == re_pass:

            user['password'] = pbkdf2_sha256.encrypt(user['password'])

            collection = db['users']
            if collection.find_one({ "email": user['email'] }):
                return "User already exists!"
            if collection.find_one({ "name": user['name'] }):
                return "UserName already taken, try different name!"
            if collection.insert_one(user):
                return "Successfully Registered! Login to go to Dashboard!"

            return "Error : Something went wrong"

        else:
            return "Password mismatch!"


    def login(self):
        user = db.users.find_one({
            "email": request.form.get('email')
        })

        if user:
            return self.start_session(user)
        
        return jsonify({ "error" : "Invalid login Credentials!" })

    def signout(self):
        session.clear()

        return redirect('/signup')

    def deleteAccount(self):
        credentials = request.json
        collection = db['users']

        if collection.find_one({ "email" : credentials['email'] }):
            collection.delete_one({ "email" : credentials['email'] })
            return "The Account has been deleted successfully!", 200

        return "Account not found!", 400