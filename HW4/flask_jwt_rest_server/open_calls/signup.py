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

def signup():
    username = request.form.get('username')
    password = request.form.get('password')

    cur = g.db.cursor()

    cur.execute("select username from users where username = '" + username + "';")
    userid = cur.fetchone()
    

    if userid == username:
        print("That username already exists, try another")
        return json_response(data={"message:" + username + " already exists!"})
    else:
        saltedpassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(10))

        cur.execute("insert into users (username, password) VALUES ('"
                    + username + "', '" + saltedpassword.decode('utf-8') + "');")
        cur.close()
        g.db.commit()

        print("Created the following user: " + username + ".")
        encoded_JWT=jwt.encode({'username':username,'password':saltedpassword.decode('utf-8')},JWT_SECRET, algorithm="HS256")
        return json_response(data={"message": username +" created successfully."})
