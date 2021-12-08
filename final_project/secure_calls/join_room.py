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
    logger.debug("{} has joined the room {}".format('username', 'room'))
    in_jwt = request.args.get("jwt")

    cur = g.db.cursor()

    cur.execute("select * from messages;")
    msgs_in_db = cur.fetchall()
    cur.close()
    cur.execute("select * from users;")
    users_in_db = cur.fetchall()
    cur.close()
    cur.execute("select * from room;")
    room_in_db = cur.fetchall()
    cur.close()

    #getting rooms
    room = '{"room":['
    for r in room_in_db:
        if r[0] < len(room_in_db) :
            room += '{"id":"'+str(r[0])+'"},'
        else:
            room += '{"id":"'+str(r[0])+'"},'
    room += "]}"
    logger.debug(room)   
    
    #getting users in room
    user_room = '{"user_room":['
    for r in users_in_db:
        if r[0] < len(user_room) :
            user_room += '{"id":"'+str(r[0])+'"},'
        else:
            user_room += '{"id":"'+str(r[0])+'"},'
    room += "]}"
    logger.debug(room) 
    
    return json_response( token = create_token(  g.jwt_data ), data = json.loads(room) )