from flask import Flask, render_template, request, redirect, url_for
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


def chat():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        return render_template('chat.html', username=username, room=room)
    else:
        return redirect(url_for('home'))
