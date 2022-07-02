# Password Manager
Project made for Data Security course. Its purpose was to learn about mechanisms and best practises for creating secure web apps. It includes authentication, secure password storage and sharing passwords with other users.

Security used:
* hashing the user's password with sha256 followed by hashing with bcrypt,
* slowing down password verification,
* symmetric encryption of stored passwords to services with the AES algorithm,
* session consistency check using CSRF tokens,
* monitoring of failed login attempts.

## Technologies
Project is made with:
* Python 3.9
* Flask
* Jinja2
* SQLite

[All requirements](requirements.txt)

## Setup local environment
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

## Features
<ul>
  <li>
    <p>Form data validation</p>
    <img width="600" height="auto" src="./screenshots/form_validation.png">
  </li>
  <li>
    <p>Password quality checking</p>
    <div>
      <img width="400" height="100" src="./screenshots/password_entropy1.png"></br>  
      <img width="400" height="100" src="./screenshots/password_entropy2.png"></br>
      <img width="400" height="100" src="./screenshots/password_entropy3.png">
    </div>
  </li>
  <li>
    <p>Adding passwords to services</p>
    <img width="600" height="auto" src="./screenshots/add_service_password.png">
  </li>
  <li>
    <p>Managing saved passwords</p>
    <img width="600" height="auto" src="./screenshots/save_passwords.png">
  </li>
  <li>
    <p>Sharing passwords to services with other users</p>
    <img width="600" height="auto" src="./screenshots/sharing_password.png">
    <img width="600" height="auto" src="./screenshots/users_with_access.png">
  </li>
  <li>
    <p>Viewing passwords from other users</p>
    <img width="600" height="auto" src="./screenshots/provided_passwords.png">
  </li>
  <li>
    <p>Hiding/showing passwords</p>
    <img width="600" height="auto" src="./screenshots/hidden_password.png">
    <img width="400" height="auto" src="./screenshots/giving_pin_to_show_password.png">
    <img width="600" height="auto" src="./screenshots/showed_password.png">
  </li>
  <li>
    <p>Password change</p>
    <img width="600" height="auto" src="./screenshots/password_changing.png">
  </li>
  <li>
    <p>Resetting a lost password</p>
    <img width="600" height="auto" src="./screenshots/reseting_password.png"></br></br>
    <img width="500" height="auto" src="./screenshots/reset_email.png"></br></br>
    <img width="600" height="auto" src="./screenshots/reseting_password2.png">
  </li>
</ul>



