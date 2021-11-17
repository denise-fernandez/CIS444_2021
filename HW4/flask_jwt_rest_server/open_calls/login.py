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

def handle_request():
    logger.debug("Login Handle Request")
    #use data here to auth the user

    password_from_user_form = request.form['password']
    user = {
            "sub" : request.form['username'] #sub is used by pyJwt as the owner of the token
            }
    if not user:
        print("in if not user")
        return json_response(status_=401, message = 'Invalid credentials', authenticated =  False )
    
    print(user)
    return json_response( token = create_token(user) , authenticated = False)

