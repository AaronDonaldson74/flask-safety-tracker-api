from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from datetime import datetime

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

db = SQLAlchemy(app)
ma = Marshmallow(app)

class IncidentForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    ppe = db.Column(db.String(200), nullable=True)
    conditions = db.Column(db.String(200), nullable=True)
    equipment = db.Column(db.String(200), nullable=True)
    others = db.Column(db.String(200), nullable=True)
    meds = db.Column(db.String(200), nullable=True)
    description = db.Column(db.String, nullable=False)

    user = db.relationship('User',
        backref=db.backref('IncidentForms', lazy=True))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    user_name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.Integer, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)


@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.debug = True
    app.run()







