from app import db, login_manager
from app import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    services = db.relationship('UserService', backref='user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def is_password_correct(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_services(self):
        services = []
        for us in self.services:
            services.append(us.service)
        return services


class Service(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=50), nullable=False)
    link = db.Column(db.String(length=100))
    password_hash = db.Column(db.String(length=60), nullable=False)
    users = db.relationship('UserService', backref='service', lazy=True)


class UserService(db.Model):
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), primary_key=True)
    service_id = db.Column(db.Integer(), db.ForeignKey('service.id'), primary_key=True)
