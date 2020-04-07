# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#
app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ----------------------------------------------------------------------------#
# App Models.
# ----------------------------------------------------------------------------#

class Venues(db.Model):  ###Parent
    __tablename__ = 'venue'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    website = db.Column(db.String(500), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    genres = db.Column("genres", db.ARRAY(db.String()), nullable=False)
    seeking_talent = db.Column(db.Boolean, nullable=True, default=True)
    seeking_description = db.Column(db.String(), nullable=True)
    show = db.relationship('Show', backref='venueshowlink', lazy=True)

    def __repr__(self):
        return f'<Venue {self.venue_id} {self.name}>'


class Artist(db.Model):  ###Parent
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(120), nullable=False)
    website = db.Column(db.String(500), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    genres = db.Column("genres", db.ARRAY(db.String()), nullable=False)
    seeking_venue = db.Column(db.Boolean, nullable=True, default=True)
    seeking_description = db.Column(db.String(), nullable=True)
    show = db.relationship('Show', backref='artistshowlink', lazy=True)

    def __repr__(self):
        return f'<Venue {self.id} {self.name}>'


class Show(db.Model):  ###Child
    __tablename__ = 'show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'))