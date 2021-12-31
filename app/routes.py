from app import app
from flask import render_template, redirect, url_for
from app.models import Service, User
from app.forms import RegisterForm
from app import db


@app.route('/')
@app.route('/home')
def home_page():
    username = 'Kacper'
    services = Service.query.all()
    return render_template('home.html', username=username, services=services)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email.data,
                              password_hash=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('home_page'))

    return render_template('register.html', form=form)
