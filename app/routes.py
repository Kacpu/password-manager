from app import app
from flask import render_template, redirect, url_for, flash
from app.models import Service, User
from app.forms import RegisterForm, LoginForm, AddServiceForm
from app import db
from flask_login import login_user, logout_user, login_required


@app.route('/')
@app.route('/home')
@login_required
def home_page():
    services = Service.query.all()
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


@app.route('/add-service', methods=['GET', 'POST'])
@login_required
def add_service():
    form = AddServiceForm()
    if form.validate_on_submit():
        service_to_create = Service(name=form.service_name.data,
                                    password_hash=form.password.data)
        db.session.add(service_to_create)
        db.session.commit()
        flash('Service added successfully!', category='success')
        return redirect(url_for('home_page'))
    return render_template('add_service.html', form=form)
