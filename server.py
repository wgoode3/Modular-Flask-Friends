from flask import Flask
from urls import routes
from models import db_connection

app = Flask(__name__)
app.secret_key = 'modularized flask app'
routes(app)
db_connection(app, 'new_db')

app.run(debug=True)