import os
from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///password_manager.db'
app.config['SECRET_KEY'] = '316e3afd6308914772212d40'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message = ''
migrate = Migrate(app, db)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ.get('MAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASS')
app.config['MAIL_USE_TLS'] = True


mail = Mail(app)

from app import routes
