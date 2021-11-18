from flask import Flask,render_template,request, redirect, url_for, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

import sys
import datetime
import bcrypt
import traceback


from db_con import get_db_instance, get_db
from tools.token_tools import create_token

from tools.logging import logger

global JWT


def handle_request():
    logger.debug("Login Handle Request")
    username = request.form.get('username')
    password = request.form.get('password')
    cur = g.db.cursor()

    cur.execute("select password from users where username = '" + username + "';")
    userIn = cur.fetchone() #user
    cur.close()

    cur = g.db.cursor()
    cur.execute("select id from users where username = '" + username + "';")
    userID = cur.fetchone() #user

    cur.close()

    print("username")
    print(username)
    print("userIn")
    print(userIn)
    print("password.encode(utf-8)")
    print(password.encode('utf-8'))
    print("password")
    print(password)
    print("userID")
    print(userID)

    user = {
            "sub" : request.form['username'] #sub is used by pyJwt as the owner of the token
            }
    cur = g.db.cursor()

    cur.execute("select id from users where username = '" + username + "';")
    userid = cur.fetchone()
    print(userid)
    if not user:
        print("in if not user")
        return json_response(status_=401, message = 'Invalid credentials', authenticated =  False )
    
    print(user)
    
    print("username")
    print(username)
    print("userIn")
    print(userIn)
    print("password.encode(utf-8)")
    print(password.encode('utf-8'))
    print("password")
    print(password)
    print("userID")
    print(userID)

    #check if the user credentials exists in users DB
    if userIn is None:  #creds don't match anything in db
        print("User doesn't exists")
        return json_response( data={"message": "Invalid User: " +username}, status =404)##

    #user and password match db
    if bcrypt.checkpw(bytes(password.encode('utf-8')), str.encode(userIn[0])) == True:
        print("Signed in as: " + username)

        JWT = jwt.encode( {"id": userID, "username": username, "password":userIn}, g.secrets['JWT'], algorithm="HS256")#

        return json_response( data={"jwt": JWT})
    else:
        print("Incorrect password")
        return json_response( data={"message": "Incorrect Password"}, status = 404)

    return json_response( token = create_token(user) , authenticated = False)
