from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home_page():
    username = 'Kacper'
    items = [{'id': 1, 'app_name': 'Facebook', 'password': '1234'},
             {'id': 2, 'app_name': 'Instagram', 'password': 'miaumiau'}]
    return render_template('home.html', username=username, items=items)


if __name__ == '__main__':
    app.run()
