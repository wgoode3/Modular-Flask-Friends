from flask import render_template, redirect, request, session, flash
from models import FriendConstructor

Friend = FriendConstructor()

def index():
	friends = Friend.getAll()
	return render_template('index.html', friends=friends)

def new():
	friend = Friend.create(request.form['name'], request.form['email'])
	if not friend[0]:
		for error in friend[1]:
			flash(error)
	return redirect('/')

def edit(friend_id):
	friend = Friend.getOne(friend_id)[0]
	friends = Friend.getAll()
	return render_template('edit.html', friend=friend, friends=friends)

def update(friend_id):
	Friend.update(friend_id, request.form['name'], request.form['email'])
	flash('Successfully updated a friend!')
	return redirect('/')

def remove(friend_id):
	Friend.delete(friend_id)
	flash('Successfully removed a friend!')
	return redirect('/')