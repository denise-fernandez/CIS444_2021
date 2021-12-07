from flask import Flask,render_template,request, redirect, url_for, g
from flask_json import FlaskJSON, JsonError, json_response, as_json
import jwt

import sys
import datetime
import bcrypt
import traceback


ERROR_MSG = "Ooops.. Didn't work!"

DEBUG = True


#Create our app
app = Flask(__name__)
#add in flask json
FlaskJSON(app)


#This gets executed by default by the browser if no page is specified
#So.. we redirect to the endpoint we want to load the base page
@app.route('/') #endpoint
def index():
    print("made contact")
    return redirect('/static/index.html')


if __name__ == '__main__':
    app.run(host='https://54.183.101.86')
