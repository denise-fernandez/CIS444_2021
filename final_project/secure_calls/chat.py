from flask import Flask, render_template, request, redirect, url_for
from flask import Flask,render_template,request, redirect, url_for, g
from flask_json import FlaskJSON, JsonError, json_response, as_json,json
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
    logger.debug(request.form['username']+" has joined the room "+ request.form['room'])
    in_jwt = request.args.get("jwt")

    cur = g.db.cursor()

    user = request.form['username']
    rm = request.form['room']


    if user and rm:
        return render_template('chat.html', username=user, room=rm)
    else:
        return redirect(url_for('index.html'))
    #return json_response( data = json.loads(user,rm) )
