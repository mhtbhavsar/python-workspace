from flask import Flask, request, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
#from flask.ext.login import UserMixin


app = Flask(__name__)
app.config['SECRET_KEY'] = 'randomStringsecretkey_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookshell.db'
db = SQLAlchemy(app)

from flaskblog import routes
