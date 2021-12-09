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

    return json_response( token = create_token(  g.jwt_data ), data = json.loads(user,rm) )
