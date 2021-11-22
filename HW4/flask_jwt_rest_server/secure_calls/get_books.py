from flask import request, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
from tools.token_tools import create_token
from psycopg2 import sql
import json
from tools.logging import logger

def handle_request():
    logger.debug("Get Books Handle Request")
    in_jwt = request.args.get("jwt")
 
    cur = g.db.cursor()

    cur.execute("select * from books;")
    books_in_db = cur.fetchall()
    cur.close()

    message = '{"books":['
    for b in books_in_db:
        if b[0] < len(books_in_db) :
            message += '{"id":"'+str(b[0]) + '","name":"' + str(b[1]) + '","price":"' + str(b[2]) +'"},'
        else:
            message += '{"id":"'+str(b[0]) + '","name":"' + str(b[1]) + '","price":"' + str(b[2]) +'"}'
    message += "]}"
    logger.debug(message)
    books= books_in_db
    logger.debug(books)
    return json_response( token = create_token(  g.jwt_data ), data = json.loads(message) )
