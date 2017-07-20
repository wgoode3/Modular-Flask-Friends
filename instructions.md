# Modular Flask Assignment
## Part 1
You have probably noticed that as the features of your website grow, the size of your server.py grows as well. Maybe you have considered that you could better organize all this code into blocks so that as the size of the project increases you can still easily find the code that handles any given feature. You may have even considered how when making a larger flask app certain queries could get called more than once in different functions. Rather than writing a query like ```mysql.query_db('SELECT * FROM friends')``` multiple times you might envision some way to instead just write ```Friends.all()```. You can organize the code that communicates with your database into a standalone class and use that class in the functions that handle your views. Ultimately you can break off that class into its own file called models.py. You can also break off the functions that determine what is shown in the html templates into their own file and call it views.py. And last you can break the decorators that handle url routes into a file called urls.py. When you seperate these parts your project will have a MVC (Model, View, Controller) structure. MVC is a popular structure for laying out a web app. You will learn a lot more about MVC when you begin Django. 
![diagram](https://raw.githubusercontent.com/wgoode3/Modular-Flask-Friends/master/static/img/diagram.png "diagram")
Return to your past Full Friends assignment. First create a new class that will have methods that you can use to make all the queries to your database that you will be needing. If you are familiar with the CRUD operations you essentially need those. Create, Read (one to fetch all friends and one for just a specific friend), Update, and Delete. The class you will make should be called FriendModel. Fill out each of the methods: create, getAll, getOne, update, and delete with the queries necessary to accomplish the task and do not forget to return something as well.
```python
# add this into your server.py

class FriendModel(object):
	def create(self, name, age, friend_since):
		query = "INSERT INTO friends(name, age, friend_since) VALUES(:name, :age, friend_since)"
		data = {'name': name, 'email': email}
		return db.query_db(query, data)
	def getAll(self):
		return db.query_db("SELECT * FROM friends")
	def getOne(self, friend_id):
		return db.query_db("SELECT * FROM friends WHERE id = :id", {'id': friend_id})
	def update(self, friend_id, name, age, friend_since):
		query = "UPDATE friends SET name=:name, age=:age, friend_since:friend_since WHERE id=:id"
		data = {'name': name, 'age': age, 'friend_since': friend_since, 'id': friend_id}
		db.query_db(query, data)
		return True
	def delete(self, friend_id):
		return db.query_db("DELETE FROM friends WHERE id = :id", {'id': friend_id})
		
# don't forget to also instantiate this FriendModel class.

Friend = FriendModel()
```
Then go back to your code and instead of making a SQL query using ```friends = mysql.query_db('SELECT * FROM friends')``` you can instead make a SQL query using ```friends = Friend.getAll()```.
If you want to add validations to your methods, you can make them function like the create method below:
```python
def create(self, name, email):
	errors = []
		
	if len(name) < 1:
		errors.append('Name is required')
	elif len(name < 3):
		errors.append('Name must be 3 characters or more')
		
	if len(email) < 1:
		errors.append('Email is required')
	elif not EMAIL_REGEX.match(email):
		errors.append('Not a valid email')

	if len(errors) > 0:
		return (False, errors)
	else:
		query = 'INSERT INTO friends (name, email) VALUES (:name, :email)'
		data = {'name': name, 'email': email}
		return (True, mysql.query_db(query, data))
```
If you have a method that also validates the data, you need to be able to handle both the cases when it should return errors and the cases when it saves something to the database. One way to accomplish this is by returning a tuple. It will be up to your view function to decide what to do with the data returned.
```python
@app.route('/new', methods=['POST'])
def new():
	new_friend = Friend.create(request.form['name'], request.form['email'])

	if new_friend[0]:
		# do something if true
	else:
		# if false display the errors that are in new_friend[1]
```
After rewriting your code go to ```localhost:5000``` and ensure the site still works. Modularizing a Flask app can be tricky, and catching bugs immediately after writing the code that produced them will make them easier to spot.
## Part 2
The next step should be easy. You are going to move the FriendModel class to a seperate file called models.py. Note that models is plural, if you had additional tables like courses, or products you would do the same thing and break them out of your server.py and make them a part of models as well.

In order to get access to app, you will create a function called db_connection that takes the arguments 'app' and 'db_name'. You will use this to create a global variable mysql. A global variable is 'scoped' so that other classes and functions outside of the function db_connection can use it.
```python
# in a new file called models.py

from mysqlconnection import MySQLConnector

def db_connection(app, db_name):
	global mysql
	mysql = MySQLConnector(app, db_name)
	
# put the FriendModel class here ...

```
In server.py you instantiate app like normal, and also set a variable DB_NAME to equal the name of your database. Next you run a function called db_connection and give it arguments app and DB_NAME. Invoking the function db_connection enables you to pass along the variables 'app' and 'db_name'.
```python
# in your server.py
from flask import Flask, render_template, redirect, request, session, flash
from models import db_connection, FriendModel

DB_NAME = 'new_db'

app = Flask(__name__)
app.secret_key = 'modularized flask app'

db_connection(app, DB_NAME)
# ...
```
Note that you could attempt to set app to be a global variable and then import server in our models.py. This is known as a _circular import_ where server is importing something from models and models is importing from server. This is considered something to be avoided.
## Part 3
Next try breaking the decorator ```@app.route('/foo')``` off of the associated functions and organizing them all together with functions that call their original function. Be sure to give the new function unique names to prevent python from seeing the functions as recursive (functions that call themselves). 
```python
# in your server.py

@app.route('/')
def indexRoute(): 
	return index()

# rest of your routes here...

def index():
	friends = Friend.getAll()
	return render_template('index.html', friends=friends)
	
# rest of your view functions here...
	
```
Now go back to ```localhost:5000``` and test that all of the routes can still be easily reached.
## Part 4
The next step is to create a new file called views.py. You will be moving the functions that were formerly associated with the decorators ```@app.route('/foo')``` functions into views.py. 
```python
# in a new file views.py

from flask import render_template, redirect, request, # anything else you need to import...
from models import FriendModel

Friend = FriendModel()

def index():
	friends = Friend.getAll()
	return render_template('index.html', friends=friends)
	
# and so on ...
```
And now in server.py you need to import views.py and to tell your routes where to find the associated functions. You can rename your route functions back to the original names now if you wish.
```python
# in the server.py
# add import views with the rest of your imports
import views

@app.route('/')
def index(): 
	return views.index()

@app.route('/new', methods=['POST'])
def new(): 
	return views.new()

# and so on...
```
Once again go to ```localhost:5000``` and test that all of the routes can still be easily reached.
## Part 5
Now you will be making a new file called urls.py and moving all of these route functions into it inside of a function called routes that takes an argument 'app'.
```python
# in urls.py
import views

def routes(app):
	@app.route('/') 
	def index(): 
		return views.index()

	@app.route('/new', methods=['POST'])
	def new(): 
		return views.new()

	# ...the rest of your routes go here

```
Don't forget to import the routes function in server and to run it. This is how you will pass the 'app' to urls.py.
```python
# in server.py don't forget to import routes
from urls import routes
# also call the function routes
routes(app)
```
Now make sure everything is still working. Assuming they are you should be able to take a moment and clean up your server.py and make it look like this.
```python
from flask import Flask
from models import db_connection
from urls import routes

DB_NAME = 'new_db'
app = Flask(__name__)
app.secret_key = 'modularized flask app'

db_connection(app, DB_NAME)
routes(app)

app.run(debug=True)
```
And by now the folder structure should look like this:
```
> modular_flask_friends
	> static
		> css
		> js
	> templates
		index.html
		edit.html
	models.py
	mysqlconnection.py
	server.py
	urls.py
	views.py
```
The new files you made: models.py, urls.py, and views.py will become very familiar when you start Django.
