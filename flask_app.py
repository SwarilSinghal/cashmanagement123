
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, redirect, request, session
from flask_session import Session
import urllib
import pymongo

app = Flask(__name__)
Session(app)

@app.route("/")
def menu():
    # return 'Hello from Flask!'
    print("HOME session:", session)
    if "username" not in session or ("username" in session and session['username'] == None):
        return render_template("login.html")
    # print("USER TYPE MENU:", session['type'])
    return render_template('menu.html', logged_in='true', type=session['type'])


def readDb(collection, condition):
    try:
        mongo_uri = "mongodb://swaril:" + urllib.parse.quote(
            "$w@R!1") + "@ac-ymz3eon-shard-00-00.iympypo.mongodb.net:27017,ac-ymz3eon-shard-00-01.iympypo.mongodb.net:27017,ac-ymz3eon-shard-00-02.iympypo.mongodb.net:27017/?ssl=true&replicaSet=atlas-y20jq1-shard-0&authSource=admin&retryWrites=true&w=majority"
        print(mongo_uri)
        client = pymongo.MongoClient(
            mongo_uri)
        print(client)
        db = client.cashManagement
        print(db)
        records = db[collection]
        print(records)
        cursor = records.find_one(condition)
        print(cursor)
        return cursor
    except:
        print("DATABASE COULDNOT CONNECT")
        return {'status':'error'}

@app.route("/login", methods=["POST", "GET"])
def login(records=None):
    message = 'Please login to your account'
    if "username" in session and session['username'] != None:
        return redirect('/')
    # return render_template('login.html', message=message)
    if hasattr(request, 'method') and request.method == "POST":
        print("inside request")
        username = request.form.get("username")
        password = request.form.get("password")
        # mongo_uri = "mongodb://swaril:" + urllib.parse.quote(
        #     "$w@R!1") + "@ac-ymz3eon-shard-00-00.iympypo.mongodb.net:27017,ac-ymz3eon-shard-00-01.iympypo.mongodb.net:27017,ac-ymz3eon-shard-00-02.iympypo.mongodb.net:27017/?ssl=true&replicaSet=atlas-y20jq1-shard-0&authSource=admin&retryWrites=true&w=majority"
        # client = pymongo.MongoClient(
        #     mongo_uri)
        # db = client.User
        # records = db.cashManagement
        user_found = readDb( "Users" , {"username": username})
        # print("user Found" + email_found)
        if user_found and "username" in user_found and "password" in user_found:
            username = user_found['username']
            passwordcheck = user_found['password']

            # if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
            if passwordcheck == password:
                print(username)
                session["username"] = username
                session['type'] = user_found['type']
                session['amount'] = user_found['amount']
                return redirect('/')
            else:
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)


@app.route("/logout")
def logout():
    session["username"] = None
    return redirect("/")


