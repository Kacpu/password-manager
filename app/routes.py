from app import app, db, mail
from flask import render_template, redirect, url_for, flash, request, jsonify, make_response
from app.models import Service, User, UserService
from app.forms import RegisterForm, LoginForm, AddServiceForm, UpdateServiceForm, AddPermissionForm, ShowPasswordForm, \
    RequestResetPasswordForm, ResetPasswordForm
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message


@app.route('/')
@app.route('/home')
@login_required
def home_page():
    admin_services = current_user.admin_services
    provided_services = current_user.get_provided_services()
    password_form = ShowPasswordForm()
    password_form.password.data = 'fake'
    return render_template('home.html', admin_services=admin_services, provided_services=provided_services,
                           password_form=password_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RegisterForm()
    # password_strength = ''
    # if form.is_submitted():
    #     password_strength = form.check_password_strength()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email.data,
                              password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash('Account created successfully!', category='success')
        return redirect(url_for('home_page'))

    # if form.errors != {}:
    #     for err_msg in form.errors.values():
    #         flash(f'{err_msg}', category='error')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.is_password_correct(password=form.password.data):
            login_user(attempted_user)
            return redirect(url_for('home_page'))
        else:
            flash('Invalid username or password!', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    return redirect(url_for('login_page'))


@app.route('/services/add', methods=['GET', 'POST'])
@login_required
def add_service():
    form = AddServiceForm()
    if form.validate_on_submit():
        service_to_create = Service(name=form.service_name.data,
                                    password_hash=form.password.data,
                                    admin_id=current_user.id,
                                    status='Private')
        db.session.add(service_to_create)
        db.session.commit()
        # user_service = UserService(user_id=current_user.id, service_id=service_to_create.id)
        # db.session.add(user_service)
        # db.session.commit()
        flash('Service has been added successfully!', category='success')
        return redirect(url_for('home_page'))
    return render_template('add_service.html', form=form)


@app.route('/services/<int:service_id>/update', methods=['GET', 'POST'])
@login_required
def update_service(service_id):
    service = Service.query.get(service_id)
    if not check_service(service):
        return redirect(url_for('home_page'))
    form = UpdateServiceForm(service.name)
    if request.method == 'GET':
        form.service_name.data = service.name
        form.password.data = service.password_hash
        print(form.password)
        return render_template('edit_service.html', form=form, legend='Update service')
    if form.validate_on_submit():
        if form.service_name.data:
            service.name = form.service_name.data
        if form.password.data:
            service.password_hash = form.password.data
        db.session.commit()
        flash(f'Service has been updated successfully!', category='success')
        return redirect(url_for('home_page'))
    return render_template('edit_service.html', form=form)


@app.route('/services/<int:service_id>/delete', methods=['Post'])
@login_required
def delete_service(service_id):
    service = Service.query.get(service_id)
    if not check_service(service):
        return redirect(url_for('home_page'))
    UserService.query.filter_by(service_id=service.id).delete()
    db.session.delete(service)
    db.session.commit()
    flash(f'Service {service.name} has been deleted successfully!', category='success')
    return redirect(url_for('home_page'))


@app.route('/services/<int:service_id>/permissions')
@login_required
def permissions_page(service_id):
    service = Service.query.get(service_id)
    if not check_service(service):
        return redirect(url_for('home_page'))
    return render_template('permissions.html', service=service)


@app.route('/services/<int:service_id>/permissions/add', methods=['GET', 'POST'])
@login_required
def add_permission(service_id):
    service = Service.query.get(service_id)
    if not check_service(service):
        return redirect(url_for('home_page'))
    form = AddPermissionForm(service_id)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        permission = UserService(user_id=user.id, service_id=service.id)
        db.session.add(permission)
        service.check_permissions_number()
        db.session.commit()
        flash(f'Permission for user {user.username} has been added successfully!', category='success')
        return redirect(url_for('permissions_page', service_id=service_id))
    return render_template('permissions.html', form=form, service=service, add_permission=True)


@app.route('/permissions/<int:user_id>/<int:service_id>/delete', methods=['Post'])
@login_required
def delete_permission(user_id, service_id):
    permission = UserService.query.get([user_id, service_id])
    username = permission.user.username
    if not check_permission(permission):
        return redirect(url_for('home_page'))
    db.session.delete(permission)
    permission.service.check_permissions_number()
    db.session.commit()
    flash(f'Permission to user {username} has been deleted successfully!', category='success')
    return redirect(url_for('permissions_page', service_id=service_id))


@app.route('/services/<int:service_id>/show-password')
@login_required
def show_password(service_id):
    service = Service.query.get(service_id)
    if not service:
        flash('Service does not exist!', category='danger')
        return redirect(url_for('home_page'))
    if service.admin_id == current_user.id:
        response_data = jsonify({'password': service.password_hash})
        resp = make_response(response_data, 200)
        return resp
    for permission in service.users:
        if permission.user_id == current_user.id:
            response_data = jsonify({'password': service.password_hash})
            resp = make_response(response_data, 200)
            return resp
    flash('Access denied!', category='danger')
    return redirect(url_for('home_page'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='pass_manager_byKT@gmail.com', recipients=[user.email_address])
    msg.body = f'''If you did not request for email reset ignore this email!
    
To reset your password click on the following link:
    
{url_for('reset_password', token=token, _external=True)}
'''
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RequestResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email_address=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to reset password.', 'info')
        redirect(url_for('login_page'))
    return render_template('reset_password_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That token is invalid or expired.", "warning")
        return redirect(url_for("reset_password_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash('Your password has been updated!', category='success')
        return redirect(url_for('login_page'))
    return render_template('reset_password.html', form=form)


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        current_user.password = form.password.data
        db.session.commit()
        flash('Your password has been updated!', category='success')
        return redirect(url_for('home_page'))
    return render_template('reset_password.html', form=form)


def check_service(service):
    if not service:
        flash('Service does not exist!', category='danger')
        return False
    if service.admin_id != current_user.id:
        flash('Access denied!', category='danger')
        return False
    return True


def check_permission(permission):
    if not permission:
        flash('Permission does not exist!', category='danger')
        return False
    if permission.service.admin_id != current_user.id:
        flash('Access denied!', category='danger')
        return False
    return True


@app.context_processor
def example():
    def get_sth(sid):
        service = Service.query.get(sid)
        return service.password_hash

    return dict(myf=get_sth)


@app.route('/get_pass_str', methods=['POST'])
def pass_str():
    password = request.json['password']
    response_data = jsonify({'str_pass': RegisterForm.check_password_strength(password)})
    resp = make_response(response_data, 200)
    return resp
