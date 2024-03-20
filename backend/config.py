# this file contains the main configuartion of this app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
# ^ creates an instance of our database
# gives us access to the databse to perform CRUD operations

# *************************************************************
# notice the setup 
# 1 configuration file
# 2 next we design our databse models ( our data ) 
# 3 
# *************************************************************