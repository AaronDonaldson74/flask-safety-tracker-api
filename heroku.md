# Python Flask App Heroku Setup
- Head over to heroku and make an account
- Make sure you have the Heroku CLI installed
  - https://devcenter.heroku.com/articles/heroku-cli#download-and-install
​
## Install Dependencies
> The psycopg2 could have the following errors:
  - Windows most likely needs psycopg2
  - Mac most likely needs psycopg2-binary
- flask-heroku
```
$ pipenv install flask-heroku
```
- psycopg2-binary
```
$ pipenv install psycopg2-binary
```
- gunicorn
```
$ pipenv install gunicorn
```
​
## Add your Procfile to the root
```
web: gunicorn app:app
```
​
## Commit the changes
```
$ git add .
$ git commit -m "added dependencies for heroku push"
```
​
## Create A New App On Heroku
- Create a new app
- Call it df-flask-todo-api
- Head over to the deploy section and copy the code they have for existing repo's
- Head back to your terminal and paste in the code you just copied
  - The folder has to be a git repository.
  - Make sure everything is commited
  - You might have to login after running this command.  Follow the prompts if it asks you to login
```
$ git status
$ heroku git:remote -a df-flask-todo-api
```
- Make sure heroku has been added as a remote
```
$ git remote -v
```
​
## Create A Postgres DB on Heroku
- Click configure addons
- Search for postgres
- After it adds postgress, click on the icon to go to the database
- Go to settings
- View credentials
- Copy the URI
​
​
## Change App To Work With Heroku And Postgres
```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
​
app = Flask(__name__)
heroku = Heroku(app)
CORS(app)
​
app.config['SQLALCHEMY_DATABASE_URI'] = 'Your uri here'
​
# The rest of the code doesn't change
```
- Create the tables in the Database
  - After running the next commands it should create new tables on heroku's postgress database.  You won't see any new files locally like we saw previously with the app.sqlite file before.
```
$ pipenv shell
$ python
>>> from app import db
>>> db.create_all()
>>> 
```
- Push the code up to heroku
```
$ git add .
$ git commit -m "added postgress database"
$ git push heroku master
```
​
## Refactor The React Client To Work With Postgres App
- Change any localhost:5000's with your heroku url
- Test it locally
- Commit and push your code
​
​
## Create the todo app client on Heroku
- Create a new app on heroku call it df-react-todo-client
- Go into settings and add the following buildpack
  - You can search for others if you want
```
https://github.com/mars/create-react-app-buildpack
```
- Head over to the deploy section and copy the code they have for existing repo's
- Head back to your terminal and paste in the code you just copied
```
$ git status
$ heroku git:remote -a df-flask-todo-api
```
- Make sure heroku has been added as a remote
```
$ git remote -v
```
- Push to heroku
```
$ git push heroku master
```
​
​
## Make Sure To Get Rid Of All Print and Console Logs
- Use the following command for any other changes
```
$ git status
$ git add .
$ git commit -m "your change message"
$ git push origin master
$ git push heroku master
```