from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
import bcrypt
import psycopg2
from psycopg2 import sql

from tools.logging import logger

def handle_request():
    logger.debug("Signup Handle Request")
    #use data here to auth the user
    password_from_user = request.form['password']
    ufu = request.form['username']

    cur = g.db.cursor()
    cur.execute(sql.SQL("select * from users where username = '" + ufu + "';"))
    user = cur.fetchone()
    cur.close()

    logger.debug(user)

    if user is not None:
        print("That username already exists, try another")
        return json_response(message = "User already exists")

    else:
        saltedpassword = bcrypt.hashpw( bytes(password_from_user, 'utf-8'), bcrypt.gensalt(12))
        logger.debug(saltedpassword)
        cur.execute(sql.SQL("insert into users (username, password) VALUES ('"
                    + user + "', '" + saltedpassword.decode('utf-8') + "');"))
        cur.close()
        g.db.commit()

        logger.debug("Created the following user: " + user)
        return json_response(message = "Successfully created user")
