from flask_sqlalchemy import SQLAlchemy
from eralchemy import render_er

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    url = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descr = db.Column(db.String(120), unique=True, nullable=False)
    url = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.descr

    def serialize(self):
        return {
            "id": self.id,
            "descr": self.descr,
            "url": self.url
            # do not serialize the password, its a security breach
        }
    
class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer)
    url = db.Column(db.String(80), unique=False, nullable=False)
    

    def __repr__(self):
        return '<Favorite %r>' % self.url

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "url": self.url
            # do not serialize the password, its a security breach
        }


render_er(Base, 'diagram.png')