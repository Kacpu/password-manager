from app import db, login_manager, app
from app import bcrypt
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.symmetric_encryption import encrypt, decrypt


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=100), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    services = db.relationship('UserService', backref='user', lazy=True)
    admin_services = db.relationship('Service', backref='admin', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def is_password_correct(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def get_provided_services(self):
        services = []
        for us in self.services:
            services.append(us.service)
        return services


class Service(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=50), nullable=False)
    link = db.Column(db.String(length=100))
    status = db.Column(db.String(length=20), nullable=False)
    encrypted_password = db.Column(db.String(length=100), nullable=False)
    password_iv = db.Column(db.String(length=100), nullable=False)
    users = db.relationship('UserService', backref='service', lazy=True)
    admin_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

    show_password = "fake"

    def set_password(self, password, pin):
        self.encrypted_password, self.password_iv = encrypt(pin, password)

    def get_password(self, pin):
        return decrypt(pin, self.password_iv, self.encrypted_password)

    def check_permissions_number(self):
        print(len(self.users))
        if len(self.users) == 0:
            self.status = "Private"
        else:
            self.status = "Shared"


class UserService(db.Model):
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), primary_key=True)
    service_id = db.Column(db.Integer(), db.ForeignKey('service.id'), primary_key=True)
