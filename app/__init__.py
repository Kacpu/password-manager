from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///password_manager.db'
app.config['SECRET_KEY'] = '316e3afd6308914772212d40'
db = SQLAlchemy(app)

from app import routes
