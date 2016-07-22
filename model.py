""" 
OpenBook 2.0 uses SQLAlchemy and PostgreSQL to store and query user and 
site information. 

"""

from flask_sqlalchemy import SQLAlchemy

import datetime

# search engines uses the library SQLAlchemy-searchable 

from sqlalchemy_searchable import make_searchable
from sqlalchemy_utils.types import TSVectorType  

db = SQLAlchemy()

make_searchable()

############################################################
# db tables for Model.py


class User(db.Model):
    """ Contains user information. """

    __tablename__ = "user"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String, nullable=False)

    # Put name inside TSVectorType definition for it to be fulltext-indexed (searchable)
    search_vector = db.Column(TSVectorType('first_name', 'last_name'))

    def __repr__(self):

        return "<User user_id={} email={}>".format(self.user_id, self.email)

    # for new users to insert into user table 
    @classmethod
    def add_new_user(cls, first_name, last_name, email, age, password=None):

        new_user = cls(first_name=first_name,
                        last_name=last_name,
                        email=email,
                        age=age,
                        password=password)

        db.session.add(new_user)
        db.session.commit()


class Connections(db.Model):
    """ Establishes relationship between users. """

    __tablename__ = 'connection'

    connection_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    control_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    connector_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    user = db.relationship("User",
                            primaryjoin="User.user_id == Connections.control_id",
                            backref=db.backref("Connections",
                                                order_by=connection_id))

    def __repr__(self):

        return ("Connection between control_id: \
                %s and connector_id: %s>") % (self.control_id,
                                            self.connector_id)

    @classmethod
    def add_connection(cls, control_id, connector_id):

        new_connection = cls(control_id=control_id, connector_id=connector_id)
        db.session.add(new_connection)
        db.session.commit()



class Images(db.Model):
    """ Stores user images that have been uploaded. """

    __tablename__ = "images"

    image_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    uploaded_At = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    likes = db.Column(db.Integer, nullable=True)
    caption = db.Column(db.String(600), nullable=True)

    user = db.relationship("User", backref=db.backref("images", order_by=user_id))

    def __repr__(self):

        return "<Images image_id={} likes={} caption={}".format(self.image_id,
                                                                self.likes,
                                                                self.caption)

class OwnedThreads(db.Model):
    """ Contains owned thread information per user. """

    __tablename__ = "owned_threads"

    owned_thread_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(600), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    public_or_private = db.Column(db.String, nullable=False)
    live_or_closed = db.Column(db.String, nullable=False)
    contributer_count = db.Column(db.Integer, nullable=True)

    # Define relationship to User

    user = db.relationship("User", backref=db.backref("owned_threads", order_by=user_id))


    def __repr__(self):

        return "<OwnedThreads owned_thread_id={} public_or_private={} live_or_closed={}>".format(self.owned_thread_id, 
                                                                                        self.public_or_private, self.live_or_closed)

class ContributerThreads(db.Model):
    """ Contains contributed threads according to user on owned threads. """

    __tablename__ = "contributer_threads"

    contributer_thread_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    text = db.Column(db.String(100), nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    likes = db.Column(db.Integer, nullable=True)

    # Define relationship to User

    user = db.relationship("User", backref=db.backref("contributer_threads", order_by=user_id))


    def __repr__(self):

        return "<ContributerThreads contributer_thread_id={} text={} date_submitted={} likes={}".format(self.contributer_thread_id,
                                                                                                        self.text,
                                                                                                        self.date_submitted,
                                                                                                        self.likes)

################################################################################

def connect_to_db(app):
    """ Connect to the database in Flask app. """

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///threaded'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."


