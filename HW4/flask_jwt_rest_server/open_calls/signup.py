from flask import Flask,render_template,request, redirect, url_for, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

import sys
import datetime
import bcrypt
import traceback


from db_con import get_db_instance, get_db

from tools.token_required import token_required
from tools.get_aws_secrets import get_secrets

from tools.logging import logger
global JWT

def handle_request():
    logger.debug("Signup Handle Request")

    password = request.form['password']
    username = request.form['username']

    cur = g.db.cursor()

    user = {
            "sub" : request.form['username'] #sub is used by pyJwt as the owner of the token
            }

    cur.execute("select username from users where username = '" + username + "';")
    userid = cur.fetchone()

    if userid == username:
        print("That username already exists, try another")
        return json_response(data={"message:" + username + " already exists!"})
    else:
        saltedpassword = bcrypt.hashpw( bytes(password, 'utf-8'), bcrypt.gensalt(10))

        cur.execute("insert into users (username, password) VALUES ('"
                    + username + "', '" + saltedpassword.decode('utf-8') + "');", (user['sub'], saltedpassword.decode('utf-8')))
        cur.close()
        g.db.commit()

        print("Created the following user: " + username)

        return json_response(data={"message": username +" created successfully."})
