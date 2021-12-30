from app import app
from flask import render_template
from app.models import Service


@app.route('/')
@app.route('/home')
def home_page():
    username = 'Kacper'
    services = Service.query.all()
    return render_template('home.html', username=username, services=services)
