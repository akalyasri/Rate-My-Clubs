from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from __init__ import create_app, db

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    two_fa_secret = db.Column(db.String(120))  # For storing 2FA token

class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    description = db.Column(db.Text)
    location = db.Column(db.String(120))  # New field for club location


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)



