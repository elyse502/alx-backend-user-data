# 0x03. User authentication service

![4cb3c8c607afc1d1582d](https://github.com/elyse502/alx-backend-user-data/assets/125453474/fc7f0d9b-deab-423e-97ec-75f38b0690b2)

In the industry, you should **not** implement your own authentication system and use a module or framework that doing it for you (like in Python-Flask: [Flask-User](https://flask-user.readthedocs.io/en/latest/)). Here, for the learning purpose, we will walk through each step of this mechanism to understand it by doing.

# Resources🏗️
<b>Read or watch:</b>
* [Flask documentation](https://flask.palletsprojects.com/en/1.1.x/quickstart/)
* [Requests module](https://requests.kennethreitz.org/en/latest/user/quickstart/)
* [HTTP status codes](https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html)

# Learning Objectives 📖
At the end of this project, you are expected to be able to [explain to anyone](https://fs.blog/feynman-learning-technique/), **without the help of Google**:
* How to declare API routes in a Flask app
* How to get and set cookies
* How to retrieve request form data
* How to return various HTTP status codes

# Requirements 🏛️
* Allowed editors: `vi`, `vim`, `emacs`
* All your files will be interpreted/compiled on Ubuntu 18.04 LTS using `python3` (version 3.7)
* All your files should end with a new line
* The first line of all your files should be exactly `#!/usr/bin/env python3`
* A `README.md` file, at the root of the folder of the project, is mandatory
* Your code should use the `pycodestyle` style (version 2.5)
* You should use `SQLAlchemy` 1.3.x
* All your files must be executable
* The length of your files will be tested using `wc`
* All your modules should have a documentation (`python3 -c 'print(__import__("my_module").__doc__)'`)
* All your classes should have a documentation (`python3 -c 'print(__import__("my_module").MyClass.__doc__)'`)
* All your functions (inside and outside a class) should have a documentation (`python3 -c 'print(__import__("my_module").my_function.__doc__)'` and `python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'`)
* A documentation is not a simple word, it’s a real sentence explaining what’s the purpose of the module, class or method (the length of it will be verified)
* All your functions should be type annotated
* The flask app should only interact with `Auth` and never with `DB` directly.
* Only public methods of `Auth` and `DB` should be used outside these classes

# Setup 🏢🏤🏣
You will need to install `bcrypt`
```groovy
pip3 install bcrypt
```
* To Install **Dependencies** used:
```groovy
pip3 install -r requirements.txt
```

# Tasks 📃
## 0. User model: [user.py](user.py)
In this task you will create a SQLAlchemy model named `User` for a database table named `users` (by using the [mapping declaration](https://docs.sqlalchemy.org/en/13/orm/tutorial.html#declare-a-mapping) of SQLAlchemy).

The model will have the following attributes:

* `id`, the integer primary key
* `email`, a non-nullable string
* `hashed_password`, a non-nullable string
* `session_id`, a nullable string
* `reset_token`, a nullable string
```groovy
bob@dylan:~$ cat main.py
#!/usr/bin/env python3
"""
Main file
"""
from user import User

print(User.__tablename__)

for column in User.__table__.columns:
    print("{}: {}".format(column, column.type))

bob@dylan:~$ python3 main.py
users
users.id: INTEGER
users.email: VARCHAR(250)
users.hashed_password: VARCHAR(250)
users.session_id: VARCHAR(250)
users.reset_token: VARCHAR(250)
bob@dylan:~$
```


































































