from mysqlconnection import MySQLConnector
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def db_connection(app, db_name):
	global db
	db = MySQLConnector(app, db_name)

def validator(name, email):
	errors = []

	if len(name) < 1:
		errors.append('Name is required!')
	elif len(name) < 3:
		errors.append('Name must be 3 characters or more!')

	if len(email) < 1:
		errors.append('Email is required!')
	elif not EMAIL_REGEX.match(email):
		errors.append('Invalid email!')
	else:
		query = "SELECT * FROM students WHERE email=:email"
		check = db.query_db(query, {'email': email})
		if len(check) > 0:
			errors.append('Email already exists!')

	return errors
	
class FriendConstructor(object):
	def create(self, name, email):
		validations = validator(name, email) 
		if len(validations) > 0:
			return False, validations
		else:
			query = "INSERT INTO students(name, email) VALUES(:name, :email)"
			data = {'name': name, 'email': email}
			return True, db.query_db(query, data)
	def getAll(self):
		return db.query_db("SELECT * FROM students")
	def getOne(self, friend_id):
		return db.query_db("SELECT * FROM students WHERE id={}".format(friend_id))
	def update(self, friend_id, name, email):
		query = "UPDATE students SET name=:name, email=:email WHERE id=:id"
		data = {'name': name, 'email': email, 'id': friend_id}
		db.query_db(query, data)
		return True
	def delete(self, friend_id):
		return db.query_db("DELETE FROM students WHERE id={}".format(friend_id))