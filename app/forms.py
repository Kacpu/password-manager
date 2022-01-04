from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from app.models import User


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
