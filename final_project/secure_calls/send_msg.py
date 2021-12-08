from flask import Flask, render_template, request, redirect, url_for
from flask import Flask,render_template,request, redirect, url_for, g
from flask_json import FlaskJSON, JsonError, json_response, as_json, json
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
    logger.debug("{} has sent message to the room {}: {}".format('username','room','message'))
    in_jwt = request.args.get("jwt")

    cur = g.db.cursor()

    cur.execute("select * from messages;")
    msgs_in_db = cur.fetchall()
    cur.close()

    message = '{"messages":['
    for m in msgs_in_db:
        if m[0] < len(msgs_in_db) :
            message += '{"msg_id":"'+str(m[0]) + '","user_id":"' + str(m[1]) + '","msg_text":"' + str(m[2]) +'"},'
        else:
            message += '{"msg_id":"'+str(m[0]) + '","user_id":"' + str(m[1]) + '","msg_text":"' + str(m[2]) +'"},'
    message += "]}"
    logger.debug(message)
    msgs= msgs_in_db
    logger.debug(msgs)
    return json_response( token = create_token(  g.jwt_data ), data = json.loads(message) )