"""
OpenBook 2.0

A creative space for thread writing. A a single user or party of users create a thread 
and  dependent upon the settings of the thread - whether the thread is made public or 
private, limits or encourages the number of users that thread can be edited by and 
appended to. 

(c) Annie Fraysse, 2016

"""

from jinja2 import StrictUndefined 

from flask import Flask, render_template, flash, redirect, request, jsonify, url_for, session
from flask_debugtoolbar import DebugToolbarExtension 

from model import connect_to_db, db

# Import SQLAlchemy exception error to use in try/except
from sqlalchemy.orm.exc import NoResultFound

# Import search function from library to query for information in database
from sqlalchemy_searchable import search 

# creates a flask app
app = Flask(__name__)

# requirement for flask session and debug toolbar
app.secret_key = "BCA"

# raise error in jinja if undefined 
app.jinja_env.undefined = StrictUndefined

####################################################

@app.route('/', methods=['GET'])
def index():
    """ Homepage with login/registration """

    current_session = session.get('user_id', None)
    return render_template("homepage.html")

@app.route('/login', methods=['POST'])
def login():
    """ Processes login. """

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        flash ("We can't find you! Please register!")
        return redirect('/registration')

    if user.password != password:
        flash("Password is negatory, so srry. Please try again!")
        return redirect('/login')

    session["user_id"] = user.user_id

    return redirect('/feed')

@app.route('/register', methods=['GET'])
def registration_form():
    """ registration form. """

    return render_template("registration.html")

@app.route('/register', methods=['POST'])
def register():
    """ get form variables from registration form. """

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")
    age = request.form.get("age")

    new_user = User(first_name=first_name, last_name=last_name, email=email,
                    password=password, age=age)

    db.session.add(new_user)
    db.session.commit()

    flash("Welcome {} {}!".format(first_name, last_name))
    return redirect('/user_name')

@app.route('/user_name', methods=['GET'])
def user_name_render():
    """ Renders template for create username. """

    return render_template("user_name_create.html")

@app.route('/user_name', methods=['POST'])
def user_name_post():
    """ Gets form variables from username create page. """

    username = request.form.get("username")

    username_taken = User.query.filter_by(username=username).first()

    if username not in username_taken:
        flash("Success!")
        return redirect('/login')

    else:
        flash("Oh no! That name is already being used! Pls try again!")



@app.route('/logout')
def logout():
    """ Log out user. """

    del session["user_id"]
    flash("Goodbye! Stop in again soon!")
    return redirect("/")




##############################################################################
# Connects to DB

if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()







