"""
Threaded 2.0

A creative space for thread writing. A a single user or party of users create a thread 
and  dependent upon the settings of the thread - whether the thread is made public or 
private, limits or encourages the number of users that thread can be edited by and 
appended to. 

(c) Annie Fraysse, 2016

"""

from jinja2 import StrictUndefined 

from flask import Flask, render_template, flash, redirect, request, jsonify, url_for, session
from flask_debugtoolbar import DebugToolbarExtension 

from model import connect_to_db, db, User, Images, Connections, OwnedThreads, ContributerThreads

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

@app.route('/login', methods=['GET'])
def login_form():
    """ login form. """

    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    """ Processes login. """

    login_email = request.form.get("login_email")
    login_password = request.form.get("login_password")

    # try to see if credentials put in work
    # if incorrect, ask to try again 
    # if correct, log in user and store to session and grab friend information 
    try:
        current_user = db.session.query(User).filter(User.email == login_email,
                                                    User.password == login_password).one()

    except NoResultFound:
        flash("We can't seem to find you! Please try again.", "Danger Will Robinson!")
        return redirect('/login')

    # Acquire current user's friend information to display in badges on page

    received_friend_requests, sent_friend_requests = get_friend_requests(current_user.user_id)
    receieved_request_count = len(received_friend_requests)
    sent_request_count = len(sent_friend_requests)
    total_request_count = receieved_request_count + sent_request_count

    # a nested dictionary stores more to the session than simply the user_id

    session["current_user"] = {
        "first_name": current_user.first_name,
        "user_id": current_user.user_id,
        "receieved_request_count": receieved_request_count,
        "sent_request_count": sent_request_count,
        "total_request_count": total_request_count
    }

    flash("Hello {}. You have successfully logged in!").format(current_user.first_name)
    
    return redirect("/dashboard/{}".format(current_user.user_id))

@app.route('/register', methods=['GET'])
def registration_form():
    """ registration form. """

    return render_template("registration.html")


@app.route('/register', methods=['POST'])
def register():
    """ get form variables from registration form. """

    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    signup_email = request.form.get("signup_email")
    signup_password = request.form.get("signup_password")
    age = request.form.get("age")

    # check to ensure signup email doesn't already exist
    # if email does not exist, create new user
    # if email does exist, flash message to ask for a login 

    try:
        db.session.query(User).filter(User.email == signup_email).one()

    except NoResultFound:
        new_user = User(first_name=first_name,
                        last_name=last_name,
                        email=signup_email,
                        password=signup_password,
                        age=age)

        db.session.add(new_user)
        db.session.commit()

   # add same info to session similar to login route 

        session["current_user"] = {
            "first_name": new_user.first_name,
            "user_id": new_user.user_id,
            "receieved_request_count": 0,
            "sent_request_count": 0,
            "total_request_count": 0
        }

        flash("You have successfully signed up for an account and are now logged in.", "success")

        return redirect("/dashboard")

        # return redirect("/dashboard/%s" % new_user.user_id)

    flash("Opps! We already have that email on record. Please login!", "Danger Will Robinson!")

    return redirect("/login")


@app.route('/user_name', methods=['GET'])
def user_name_render():
    """ Renders template for create username. """

    return render_template("user_name_create.html")

@app.route('/user_name', methods=['POST'])
def user_name_post():
    """ Gets form variables from username create page. """

    username = request.form.get("username")

    username_taken = User.query.filter_by(username=username).all()

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


@app.route('/dashboard', methods=['GET'])
def dashboard_render():
    """ Render dashboard template. """

    return render_template("dashboard.html")

@app.route('/dashboard', methods=['POST'])
def dashboard_view():

    pass





##############################################################################
# Connects to DB

if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()







