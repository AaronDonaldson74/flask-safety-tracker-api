from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
import os
from datetime import datetime
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)
heroku = Heroku(app)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")

db = SQLAlchemy(app)
ma = Marshmallow(app)
fb = Bcrypt(app)

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
    user_name = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    department = db.Column(db.Integer, nullable=False)
    admin = db.Column(db.Boolean, nullable=False)


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

# Creates a user profile.
@app.route("/user/register", methods=["POST"])
def add_user():
  user_name = request.json["user_name"]
  password = request.json["password"]
  department = request.json["department"]
  admin = request.json["admin"]

  hashed_password = fb.generate_password_hash(password).decode('utf-8')

  new_user = User(user_name=user_name,
  password=hashed_password,
  department=department,
  admin=admin)

  db.session.add(new_user)
  db.session.commit()

  user = User.query.get(new_user.id)
  return user_schema.jsonify(user)

#This route for testing purposes.
@app.route("/users", methods=["GET"])
def get_users():
    all_users = User.query.all()
    result = users_schema.dump(all_users)

    return jsonify(result)

#This route for login authentication.
@app.route('/user/login', methods=["POST"])
def login():
    post_data = request.get_json()
    db_user = User.query.filter_by(user_name=post_data.get('user_name')).first()
    
    if db_user is None:
        return jsonify('Username Not Found')

    user_name = post_data.get('user_name')
    password = post_data.get('password')
    db_user_hashed_password = db_user.password
    valid_password = fb.check_password_hash(db_user_hashed_password, password)

    if valid_password:
        return jsonify({
            "userInfo": user_schema.dump(db_user),
            "message": "User Verified"
        })
    
    return jsonify("I'm sorry, that password is not correct")

#This route is for posting an incident form.
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

@app.route("/user/<id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)

    db.session.delete(user)
    db.session.commit()

    return jsonify("User Deleted!")

@app.route("/incidentForm/<id>", methods=["DELETE"])
def delete_incidentForm(id):
    incidentForm = IncidentForm.query.get(id)

    db.session.delete(incidentForm)
    db.session.commit()

    return jsonify("Form Deleted!")

if __name__ == "__main__":
    app.debug = True
    app.run()







