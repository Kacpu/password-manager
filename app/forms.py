from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from app.models import User, Service, UserService
from flask_login import current_user
import re
from password_strength import PasswordPolicy, PasswordStats


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Given username already exists!')
        if has_invalid_characters(username_to_check.data):
            raise ValidationError('Username must contain only letters, numbers or the underscore character!')

    def validate_email(self, email_to_check):
        user = User.query.filter_by(email_address=email_to_check.data).first()
        if user:
            raise ValidationError('Given email already exists!')

    def validate_password(self, password_to_check):
        reg_pass = "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*\W|.*[_])(\S)*$"
        if not re.search(reg_pass, password_to_check.data):
            raise ValidationError('Password must contain at least one lowercase letter, one uppercase letter, '
                                  'one number and one special character!')

    @staticmethod
    def check_password_strength(password):
        if password != '':
            stats = PasswordStats(password)
            if stats.strength() <= 0.33:
                return "Attention! The password you entered is weak!"
            elif stats.strength() <= 0.66:
                return "The password you entered is medium."
            else:
                return "The password you entered is strong."
        return ''

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

    def validate_pin_code(self, pin_code_to_check):
        reg_digit = "^\d+$"
        if not re.search(reg_digit, pin_code_to_check.data):
            raise ValidationError('Pin Code must contain only numbers!')

    service_name = StringField(label='Service name', validators=[Length(max=50), DataRequired()])
    pin_code = StringField(label='Pin Code', validators=[Length(min=4, max=10), DataRequired()])
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

    def validate_pin_code(self, pin_code_to_check):
        reg_digit = "^\d+$"
        if pin_code_to_check.data != '' and self.password.data == '':
            raise ValidationError('You can not change pin code. Give new pin code to the new password.')

        if pin_code_to_check.data != '':
            if not re.search(reg_digit, pin_code_to_check.data):
                raise ValidationError('Pin Code must contain only numbers.')
            if len(pin_code_to_check.data) < 4:
                raise ValidationError('Pin Code must be at least 4 characters long.')

    def validate_password(self, password_service_name):
        if password_service_name.data != '' and self.pin_code.data == '':
            raise ValidationError('You must give new pin code to the new password.')

    service_name = StringField(label='Service name', validators=[Length(max=50)])
    pin_code = StringField(label='Pin Code', validators=[Length(max=10)])
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


class RequestResetPasswordForm(FlaskForm):
    def validate_email(self, email_to_check):
        user = User.query.filter_by(email_address=email_to_check.data).first()
        if user is None:
            raise ValidationError('Account with that email does not exist!')

    email = StringField(label='Email', validators=[Email(), DataRequired()])
    submit = SubmitField(label='Send email')


class ResetPasswordForm(FlaskForm):
    def validate_password(self, password_to_check):
        reg_pass = "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*\W|.*[_])(\S)*$"
        if not re.search(reg_pass, password_to_check.data):
            raise ValidationError('Password must contain at least one lowercase letter, one uppercase letter, '
                                  'one number and one special character!')

    password = PasswordField(label='Password', validators=[Length(min=8), DataRequired()])
    confirm_password = PasswordField(label='Confirm password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Reset password')


class ChangePasswordForm(FlaskForm):
    def validate_actual_password(self, actual_password_to_check):
        if not current_user.is_password_correct(password=actual_password_to_check.data):
            raise ValidationError('Invalid password. You must enter your current password to change it.')

    def validate_password(self, password_to_check):
        reg_pass = "^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*\W|.*[_])(\S)*$"
        if not re.search(reg_pass, password_to_check.data):
            raise ValidationError('Password must contain at least one lowercase letter, one uppercase letter, '
                                  'one number and one special character!')

    actual_password = PasswordField(label='Actual password', validators=[DataRequired()])
    password = PasswordField(label=' New password', validators=[Length(min=8), DataRequired()])
    confirm_password = PasswordField(label='Confirm password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Reset password')


class ShowServicePasswordForm(FlaskForm):
    pin_code = StringField(label='Pin Code')
    submit = SubmitField(label='Show password', id='check')


def has_invalid_characters(data):
    reg_word = "^\w+$"
    reg_no_word = "^(?=.*\W)"

    if re.search(reg_word, data):
        if re.search(reg_no_word, data):
            return True
        else:
            return False
    else:
        return True
