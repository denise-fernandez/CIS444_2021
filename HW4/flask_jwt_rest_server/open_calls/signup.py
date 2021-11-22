from flask import Flask,render_template,request, redirect, url_for, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt
import psycopg2
from psycopg2 import sql

import sys
import datetime
import bcrypt
import traceback


from db_con import get_db_instance, get_db
from tools.token_tools import create_token

from tools.logging import logger


def handle_request():
    logger.debug("Signup Handle Request")
    password_from_user = request.form['newpassword']
    ufu = request.form['newuser']

    cur = g.db.cursor()
    cur.execute(sql.SQL("select * from users where username = '" + ufu + "';"))
    user = cur.fetchone()

    logger.debug(user)

    if user is not None:
        print("That username already exists, try another")
        return json_response(message = "User already exists")

    else:
        saltedpassword = bcrypt.hashpw( bytes(password_from_user, 'utf-8'), bcrypt.gensalt(12))
        logger.debug(saltedpassword)
        cur.execute(sql.SQL("insert into users (username, password) VALUES ('"
                    + ufu + "', '" + saltedpassword.decode('utf-8') + "');"))
        cur.close()
        g.db.commit()

        logger.debug("Created the following user: " + ufu)
        return json_response(message = "Successfully created user")
