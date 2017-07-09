# Modular-Flask-Friends
A Flask friend management app with a MVC structure à la Django.

## Technologies
* Python 2.7
* Flask
* mySQL

## To get it running
* Create a ```new_db``` database in mySQL with a table ```students```
| Column Name | Datatype    |
|:-----------:|:-----------:|
| id          | INT         |
| name        | varchar(45) |
| email       | varchar(45) |
* Edit ```mysqlconnection.py``` with the correct user, password, and port information
```python
config = {
    'host': 'localhost',
    'database': db,
    'user': 'test',
    'password': 'Test1234',
    'port': '3306'
}
```
* It would be a good idea to set up a virtual environment for Flask 
* Inside your virtual environment run ```(flaskEnv) $ pip install -r requirements.txt```
* Run the server with ```(flaskEnv) $ python server.py```
