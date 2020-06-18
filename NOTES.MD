### This was originally for a TODO api development, I have used it here to create my incident report app. 


# FLASK TODO API
​
- Lets get the folder setup
```
$ mkdir todo-app
$ cd todo-app
$ mkdir flask-todo-api
$ cd flask-todo-api
```
​
- Lets make our files
```
MAC
$ touch app.py
$ touch .gitignore
$ touch README.md
PC
$ type nul > app.py
$ type nul > .gitignore
$ type nul > README.MD
```
​
- Lets open vscode
```
$ code .
```
​
- Update your .gitignore
```
app.sqlite
```
​
- Lets read the docs
[flask-pypi](https://pypi.org/project/Flask/)
[flask-docs](https://flask.palletsprojects.com/en/1.1.x/)
​
[flask-sqlalchemy-pypi](https://pypi.org/project/Flask-SQLAlchemy/)
[flask-sqlalchemy-docs](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
​
[flask-marshmallow-pypi](https://pypi.org/project/flask-marshmallow/)
[flask-marshmallow-docs](https://flask-marshmallow.readthedocs.io/)
​
- Lets install all of our dependencies
```
$ pipenv install Flask Flask-SQLAlchemy flask-marshmallow
```
​
- Lets make sure we set Flask up correctly
  - Add the following to app.py
```python
from flask import Flask
​
app = Flask(__name__)
​
@app.route("/")
def hello():
    return "Hello, World!"
​
if __name__ == "__main__":
    app.debug = True
    app.run()
```
​
- Lets hop into our shell and run our app
```
$ pipenv shell
$ python app.py
```
​
- Open your browser and traverse to http://localhost:5000/
  - You should see Hello, World! on the screen
    - If you didn't see the Hello, World! you set something up wrong.  Head to your terminal and might have some answers for you.
    - If you saw Hello, World!, Go back to your terminal and you will see a GET request with a 200.
​
- We have working code lets save this to git
  - Open your readme first and add a simple description.  We will update this further later.
  - You can right click the readme and preview
```
# Python Flask TODO Api
​
> Python Flask backend app for keeping track of todos.  It uses a flask sqlite database along with flask-marshmallow for object serialization/deserialization.  You can Post, Get, Patch, and Delete todos through flask routes.
```
```
$ git init
$ git add .
$ git commit -m "Initial Commit"
```
- Hop over to github and create a repo
```
$ git remote add origin https://github.com/gleekzorp/flask-todo-api.git
$ git push -u origin master
```
​
- Lets import all of our dependencies
  - Add the following to the top of app.py
```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
```
​
- Lets get our database setup first
  - Add the following to your app.py below the app = Flask
```python
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
​
db = SQLAlchemy(app)
ma = Marshmallow(app)
​
class Todo(db.Model):
  __tablename__ = "todos"
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), nullable=False)
  done = db.Column(db.Boolean)
​
  def __init__(self, title, done):
    self.title = title
    self.done = done
​
class TodoSchema(ma.Schema):
  class Meta:
    fields = ("id", "title", "done")
​
todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)
```
​
- Lets make sure we didn't have any typos and build our sqlite database
  - Make sure to be in your pipenv shell and hop into a python repl
  - When finished you should have an app.sqlite file
    - It should be greyed out due to the .gitignore
```
$ python
>>> from app import db
>>> db.create_all()
```
​
# LETS MAKE SOME API ROUTES
## Lets start with adding a todo
  - Add this below the hello route
```python
@app.route("/todo", methods=["POST"])
def add_todo():
  title = request.json["title"]
  done = request.json["done"]
​
  new_todo = Todo(title, done)
​
  db.session.add(new_todo)
  db.session.commit()
​
  todo = Todo.query.get(new_todo.id)
  return todo_schema.jsonify(todo)
```
​
- Lets test this in postman
  - Start your server
```
$ python app.py
```
- Create a POST route to http://localhost:5000/todo
- Make sure body is type json
```json
{
	"title": "Clean My Bedroom",
	"done": false
}
```
- Lets make sure our id is working
```json
{
	"title": "Clean My Car",
	"done": false
}
```
​
- We have working code lets save this to git
```
$ git add .
$ git commit -m "sqlite database setup along with post route"
$ git push
```
​
## Lets create a route to get all the todos
```python
@app.route("/todos", methods=["GET"])
def get_todos():
  all_todos = Todo.query.all()
  result = todos_schema.dump(all_todos)
​
  return jsonify(result)
```
​
- Lets test this in postman
  - Start your server
```
$ python app.py
```
- Create a GET route to http://localhost:5000/todos
​
- We have working code lets save this to git
```
$ git add .
$ git commit -m "get all todos route setup"
$ git push
```
​
## Lets create a route to Patch a todo
```python
@app.route("/todo/<id>", methods=["PATCH"])
def update_todo(id):
  todo = Todo.query.get(id)
​
  new_done = request.json["done"]
​
  todo.done = new_done
​
  db.session.commit()
  return todo_schema.jsonify(todo)
```
​
- Lets test this in postman
  - Start your server
```
$ python app.py
```
- Create a PATCH route to http://localhost:5000/todo/id
- Make sure body is type json
```json
{
	"done": true
}
```
​
- We have working code lets save this to git
```
$ git add .
$ git commit -m "patch route setup for updating done based on todo id"
$ git push
```
​
## Lets create a route to Delete a todo
```python
@app.route("/todo/<id>", methods=["DELETE"])
def delete_todo(id):
  todo = Todo.query.get(id)
  db.session.delete(todo)
  db.session.commit()
​
  return jsonify("Todo Deleted!")
```
​
- Lets test this in postman
  - Start your server
```
$ python app.py
```
- Create a DELETE route to http://localhost:5000/todo/id
- We have working code lets save this to git
```
$ git add .
$ git commit -m "Delete route setup based on id"
$ git push
```
​
- Lets update our readme
# Python Flask TODO Api
​
> Python Flask backend app for keeping track of todos.  It uses a flask sqlite database along with flask-marshmallow for object serialization/deserialization.  You can Post, Get, Patch, and Delete todos through flask routes.
​
- Dependencies
  - Python
    - [python](https://www.python.org/)
  - Flask
    - [flask-pypi](https://pypi.org/project/Flask/)
    - [flask-docs](https://flask.palletsprojects.com/en/1.1.x/)
  - Flask-SQLAlchemy
    - [flask-sqlalchemy-pypi](https://pypi.org/project/Flask-SQLAlchemy/)
    - [flask-sqlalchemy-docs](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
  - Flask-Marshmallow
    - [flask-marshmallow-pypi](https://pypi.org/project/flask-marshmallow/)
    - [flask-marshmallow-docs](https://flask-marshmallow.readthedocs.io/)
​
- Install all dependencies
```
$ pipenv install Flask Flask-SQLAlchemy flask-marshmallow
```
​
- Create your sqlite database
```
$ pipenv shell
$ python
>>> from app import db
>>> db.create_all()
```
​
- Flask Routes
  - POST One Todo
    - http://localhost:5000/todo
    ```
    {
        "title": "Clean My Bedroom",
        "done": false
    }
    ```
  - GET All Todos
    - http://localhost:5000/todos
  - PATCH One Todo (only updates done)
    - http://localhost:5000/todo/id
    ```
    {
        "done": true
    }
    ```
  - DELETE One Todo
    - http://localhost:5000/todo/id