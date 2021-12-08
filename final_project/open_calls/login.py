from flask import Flask,render_template,request, redirect, url_for, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt
import psycopg2  
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
    pfu = request.form['password']
    user = {
            "sub" : request.form['username'] #sub is used by pyJwt as the owner of the token
            }

    cur = g.db.cursor()
    cur.execute("select * from users where username = '" + user['sub'] + "';")
    dbcredz = cur.fetchone()
    cur.close()
    #print(dbcredz)

    if dbcredz is None:
        logger.debug("No User")
        return json_response(status_=401, message = 'No user exists', authenticated =  False )
    else:
        if bcrypt.checkpw(bytes(pfu, 'utf-8'), bytes(dbcredz[2], 'utf-8')) == True:
            logger.debug("Successful Login for : " + request.form['username'] )
            return json_response( token= create_token(user), authenticated = True)
        else:
            return json_response(status_ = 401, data={"message": "Incorrect Password"}, authenticated = False)

