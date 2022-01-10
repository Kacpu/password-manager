from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from app.models import User, Service, UserService
from flask_login import current_user


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Given username already exists!')

    def validate_email(self, email_to_check):
        user = User.query.filter_by(email_address=email_to_check.data).first()
        if user:
            raise ValidationError('Given email already exists!')

    username = StringField(label='Username', validators=[Length(min=4, max=30), DataRequired()])
    email = StringField(label='Email address', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=8), DataRequired()])
    confirm_password = PasswordField(label='Confirm password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Create account')


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class AddServiceForm(FlaskForm):
    def validate_service_name(self, service_name_to_check):
        for service in current_user.admin_services:
            if service.name == service_name_to_check.data:
                raise ValidationError('Given service already exists!')

    service_name = StringField(label='Service name', validators=[Length(max=50), DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Add service')


class UpdateServiceForm(FlaskForm):
    def __init__(self, exist_service_name, **kwargs):
        super().__init__(**kwargs)
        self.exist_service_name = exist_service_name

    def validate_service_name(self, update_service_name):
        for service in current_user.admin_services:
            if service.name != self.exist_service_name and service.name == update_service_name.data:
                raise ValidationError('Given service already exists!')

    service_name = StringField(label='Service name', validators=[Length(max=50)])
    password = PasswordField(label='Password', validators=[])
    submit = SubmitField(label='Update')


class AddPermissionForm(FlaskForm):
    def __init__(self, service_id, **kwargs):
        super().__init__(**kwargs)
        self.service_id = service_id

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if not user:
            raise ValidationError('User with given username dose not exist!')
        if username_to_check.data == current_user.username:
            raise ValidationError('Can not give permission to yourself!')
        for permission in UserService.query.filter_by(service_id=self.service_id):
            if permission.user.username == username_to_check.data:
                raise ValidationError('Given permission already exists!')

    username = StringField(label='Username', validators=[Length(max=50), DataRequired()])
    submit = SubmitField(label='Add permission')


class ShowPasswordForm(FlaskForm):
    password = PasswordField('password', validators=[DataRequired()], id='password')
    show_password = SubmitField(label='Show password', id='check')
