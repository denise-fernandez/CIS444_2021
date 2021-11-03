from flask import Flask, render_template, request
from flask_json import FlaskJSON, jsonify, JsonError, json_response, as_json
import jwt
import psycopg2
import datetime
import bcrypt
import db_con
import json

from db_con import get_db_instance, get_db

app = Flask(__name__)
FlaskJSON(app)

global JWT
JWT_SECRET = None

global_db_con = get_db()

with open("secret", "r") as f:
    JWT_SECRET = f.read()

@app.route('/cart', methods=["POST"]) #endpoint
def cart():
    name = request.form['name']
    cur = global_db_con.cursor()
    cur.execute("INSERT INTO cart(id, name, price) SELECT id, name, price FROM books WHERE name = '" + name + "';")
    cur.close()
    global_db_con.commit()

    print("Added book to cart.")
    print(str(name))
    return json_response(data={"message": str(name) +" added successfully."}, status=200) 


#buy books
@app.route('/buy', methods=["GET"]) #endpoint
def buy():
    in_jwt = request.args.get("jwt")

    cur = global_db_con.cursor()
    cur.execute("select * from cart;")
    buylist = cur.fetchall()
    cur.close()

    count=1
    message = '{"buylist":['
    for b in buylist:

        if count < len(buylist) :
            message += '{"id":"'+str(b[0]) + '","name":"' + str(b[1]) + '","price":"' + str(b[2]) +'"},'
            count=count+1
        else:
            message += '{"id":"'+str(b[0]) + '","name":"' + str(b[1]) + '","price":"' + str(b[2]) +'"}'
    message += "]}"


    print(message)
    return json_response(data=json.loads(message), status=200)


# get list of books
@app.route('/bookstore', methods=["GET"]) #endpoint
def bookstore():
    in_jwt = request.args.get("jwt")

    cur = global_db_con.cursor()
    cur.execute("select * from books;")
    booklist = cur.fetchall()
    cur.close()

    message = '{"books":['
    for b in booklist:
        if b[0] < len(booklist) :
            message += '{"id":"'+str(b[0]) + '","name":"' + str(b[1]) + '","price":"' + str(b[2]) +'"},'
        else:
            message += '{"id":"'+str(b[0]) + '","name":"' + str(b[1]) + '","price":"' + str(b[2]) +'"}'
    message += "]}"

    return json_response(data=json.loads(message))

    
#login endpoint
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    cur = global_db_con.cursor()

    cur.execute("select password from users where username = '" + username + "';")
    userIn = cur.fetchone() #user
    cur.close() 
    
    cur = global_db_con.cursor()
    cur.execute("select id from users where username = '" + username + "';")
    userID = cur.fetchone() #user
 
    cur.close()

    print("username")
    print(username)
    print("userIn")
    print(userIn)
    print("password.encode(utf-8)")
    print(password.encode('utf-8'))
    print("password")
    print(password)
    print("userID")
    print(userID)

    #check if the user credentials exists in users DB
    if userIn is None:  #creds don't match anything in db
        print("User doesn't exists")
        return json_response( data={"message": "Invalid User: " +username}, status =404)##

    #user and password match db
    if bcrypt.checkpw(bytes(password.encode('utf-8')), str.encode(userIn[0])) == True:
        print("Signed in as: " + username)

        JWT = jwt.encode( {"id": userID, "username": username, "password":userIn}, JWT_SECRET, algorithm="HS256")#

        return json_response( data={"jwt": JWT})
    else:
        print("Incorrect password")
        return json_response( data={"message": "Incorrect Password"}, status = 404)

#signup endpoint
@app.route('/signup', methods=["POST"])
def signup():
    username = request.form.get('username')
    password = request.form.get('password')

    cur = global_db_con.cursor()

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
        global_db_con.commit()

        print("Created the following user: " + username + ".")
        encoded_JWT=jwt.encode({'username':username,'password':saltedpassword.decode('utf-8')},JWT_SECRET, algorithm="HS256")
        return json_response(data={"message": username +" created successfully."})


app.run(host='0.0.0.0', port=80)

