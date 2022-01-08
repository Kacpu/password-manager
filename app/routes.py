from app import app
from flask import render_template, redirect, url_for, flash, request
from app.models import Service, User, UserService
from app.forms import RegisterForm, LoginForm, AddServiceForm, UpdateServiceForm
from app import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
@login_required
def home_page():
    services = current_user.get_services()
    return render_template('home.html', services=services)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
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


@app.route('/service/add', methods=['GET', 'POST'])
@login_required
def add_service():
    form = AddServiceForm()
    if form.validate_on_submit():
        service_to_create = Service(name=form.service_name.data,
                                    password_hash=form.password.data)
        db.session.add(service_to_create)
        db.session.commit()
        user_service = UserService(user_id=current_user.id, service_id=service_to_create.id)
        db.session.add(user_service)
        db.session.commit()
        flash('Service has been added successfully!', category='success')
        return redirect(url_for('home_page'))
    return render_template('add_service.html', form=form, legend='Add password to service')


@app.route('/service/<int:service_id>/update', methods=['GET', 'POST'])
@login_required
def update_service(service_id):
    service = Service.query.get(service_id)
    if not check_service(service):
        return redirect(url_for('home_page'))
    form = UpdateServiceForm(service.name)
    if request.method == 'GET':
        form.service_name.data = service.name
        form.password.data = service.password_hash
        return render_template('add_service.html', form=form, legend='Update service')
    if form.validate_on_submit():
        service.name = form.service_name.data
        service.password_hash = form.password.data
        db.session.commit()
        flash(f'Service has been updated successfully!', category='success')
        return redirect(url_for('home_page'))
    return render_template('add_service.html', form=form, legend='Update service')


@app.route('/service/<int:service_id>/delete', methods=['Post'])
@login_required
def delete_service(service_id):
    service = Service.query.get(service_id)
    if not check_service(service):
        return redirect(url_for('home_page'))
    us = UserService.query.get([current_user.id, service.id])
    db.session.delete(us)
    db.session.delete(service)
    db.session.commit()
    flash(f'Service {service.name} has been deleted successfully!', category='success')
    return redirect(url_for('home_page'))


def check_service(service):
    if not service:
        flash('Service does not exist!', category='danger')
        return False
    if not UserService.query.get([current_user.id, service.id]):
        flash('Access denied!', category='danger')
        return False
    return True
