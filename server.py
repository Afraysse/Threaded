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




##############################################################################
# Connects to DB

if __name__ == "__main__":

    app.debug = True

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run()







