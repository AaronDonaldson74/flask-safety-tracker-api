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
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ppe = db.Column(db.String(200), nullable=True)
    conditions = db.Column(db.String(200), nullable=True)
    equipment = db.Column(db.String(200), nullable=True)
    others = db.Column(db.String(200), nullable=True)
    meds = db.Column(db.String(200), nullable=True)
    description = db.Column(db.String, nullable=False)
    user = db.relationship('User', backref=db.backref('incidentForms', lazy=True))

    def __init__(self, author, ppe, conditions, equipment, others, meds, description):
        self.author = author
        self.ppe = ppe
        self.conditions = conditions
        self.equipment = equipment
        self.others = others
        self.meds = meds
        self.description = description

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    user_name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.Integer, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    def __init__(self, user_name, department, admin):
        self.user_name = user_name
        self.department = department
        self.admin = admin

class IncidentFormSchema(ma.Schema):
    class Meta:
        fields = ("id",
            "pub_date",
            "author",
            "ppe",
            "conditions",
            "equipment",
            "others",
            "meds",
            "description",
        )

class UserSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "user_name",
            "department",
            "admin"
        )
            

user_schema = UserSchema()
users_schema = UserSchema(many=True)

incidentForm_schema = IncidentFormSchema()
incidentForms_schema = IncidentFormSchema(many=True)

@app.route("/")
def hello_world():
    return "Hello, World!"
    # output = incidentForm_schema.dump().data
    # return jsonify({'user' : output})

@app.route("/user", methods=["POST"])
def add_user():
  user_name = request.json["user_name"]
  department = request.json["department"]
  admin = request.json["admin"]

  new_user = User(user_name, department, admin)

  db.session.add(new_user)
  db.session.commit()

  user = User.query.get(new_user.id)
  return user_schema.jsonify(user)

@app.route("/users", methods=["GET"])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)

    return jsonify(result)

@app.route("/incidentForm", methods=["POST"])
def add_incidentForm():
    author = request.json["author"]
    ppe = request.json["ppe"]
    conditions = request.json["conditions"]
    equipment = request.json["equipment"]
    others = request.json["others"]
    meds = request.json["meds"]
    description = request.json["description"]

    new_incidentForm = IncidentForm(
            author,
            ppe,
            conditions,
            equipment,
            others,
            meds,
            description)

    db.session.add(new_incidentForm)
    db.session.commit()

    incidentForm = IncidentForm.query.get(new_incidentForm.id)
    return incidentForm_schema.jsonify(incidentForm)

@app.route("/incidentForms", methods=["GET"])
def get_incidentForms():
    all_incidentForms = IncidentForm.query.all()
    result = incidentForms_schema.dump(all_incidentForms)

    return jsonify(result)

@app.route("/user/<id>", methods=["PATCH"])
def update_user(id):
    user = User.query.get(id)

    new_user_name = request.json["user_name"]
    new_department = request.json["department"]
    new_admin = request.json["admin"]

    user.user_name = new_user_name
    user.department = new_department
    user.admin = new_admin

    db.session.commit()
    return user_schema.jsonify(user)

@app.route("/incidentForm/<id>", methods=["PATCH"])
def update_incidentForm(id):
    incidentForm = IncidentForm.query.get(id)

    new_author = request.json["author"]
    new_ppe = request.json["ppe"]
    new_conditions = request.json["conditions"]
    new_equipment = request.json["equipment"]
    new_others = request.json["others"]
    new_meds = request.json["meds"]
    new_description = request.json["description"]
    
    incidentForm.author = new_author
    incidentForm.ppe = new_ppe
    incidentForm.conditions = new_conditions
    incidentForm.equipment = new_equipment
    incidentForm.others = new_others
    incidentForm.meds = new_meds
    incidentForm.description = new_description

    db.session.commit()
    return incidentForm_schema.jsonify(incidentForm)


if __name__ == "__main__":
    app.debug = True
    app.run()







