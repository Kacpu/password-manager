# Password Manager
Project made for Data Security classes. Its purpose was to learn about mechanisms and best practises for creating secure web apps. It includes secure authentication, password storage and sharing passwords with other users.

## Technologies
Project is created with:
* Python 3.9
* Flask
* Jinja2!

* SQLite

[All requirements](requirements.txt)

## Features
* Form data validation


## Setup
Install all requirements:

```shell
pip install -r requirements.txt
```

Create database from the python shell:
```shell
>>> from app import db
>>> db.create_all()
```

Run the app:

```shell
python -m flask run
```
