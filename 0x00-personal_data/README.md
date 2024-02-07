# 0x00. Personal data

![5c48d4f6d4dd8081eb48](https://github.com/elyse502/alx-backend-user-data/assets/125453474/8bf68917-255c-4b6e-867f-e27671a54223)

# Resources🏗️
### Read or watch:
* [What Is PII, non-PII, and Personal Data?](https://piwik.pro/blog/what-is-pii-personal-data/)
* [logging documentation](https://docs.python.org/3/library/logging.html)
* [bcrypt package](https://github.com/pyca/bcrypt/)
* [Logging to Files, Setting Levels, and Formatting](https://www.youtube.com/watch?v=-ARI4Cz-awo)

# Learning Objectives 📖
At the end of this project, you are expected to be able to [explain to anyone](https://fs.blog/feynman-learning-technique/), **without the help of Google**:
* Examples of Personally Identifiable Information (PII)
* How to implement a log filter that will obfuscate PII fields
* How to encrypt a password and check the validity of an input password
* How to authenticate to a database using environment variables

# Requirements 🏛️
* All your files will be interpreted/compiled on Ubuntu 18.04 LTS using `python3` (version 3.7)
* All your files should end with a new line
* The first line of all your files should be exactly `#!/usr/bin/env python3`
* A `README.md` file, at the root of the folder of the project, is mandatory
* Your code should use the `pycodestyle` style (version 2.5)
* All your files must be executable
* The length of your files will be tested using `wc`
* All your modules should have a documentation (`python3 -c 'print(__import__("my_module").__doc__)'`)
* All your classes should have a documentation (`python3 -c 'print(__import__("my_module").MyClass.__doc__)'`)
* All your functions (inside and outside a class) should have a documentation (`python3 -c 'print(__import__("my_module").my_function.__doc__)'` and `python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'`)
* A documentation is not a simple word, it’s a real sentence explaining what’s the purpose of the module, class or method (the length of it will be verified)
* All your functions should be type annotated

# Tasks 📃
## 0. Regex-ing: [filtered_logger.py](filtered_logger.py)
Write a function called `filter_datum` that returns the log message obfuscated:

* Arguments:
  * `fields`: a list of strings representing all fields to obfuscate
  * `redaction`: a string representing by what the field will be obfuscated
  * `message`: a string representing the log line
  * `separator`: a string representing by which character is separating all fields in the log line (`message`)
* The function should use a regex to replace occurrences of certain field values.
* `filter_datum` should be less than 5 lines long and use `re.sub` to perform the substitution with a single regex.
```groovy
bob@dylan:~$ cat 0-main.py
#!/usr/bin/env python3
"""
Main file
"""

filter_datum = __import__('filtered_logger').filter_datum

fields = ["password", "date_of_birth"]
messages = ["name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;", "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"]

for message in messages:
    print(filter_datum(fields, 'xxx', message, ';'))

bob@dylan:~$
bob@dylan:~$ ./0-main.py
name=egg;email=eggmin@eggsample.com;password=xxx;date_of_birth=xxx;
name=bob;email=bob@dylan.com;password=xxx;date_of_birth=xxx;
bob@dylan:~$
```

## 1. Log formatter: [filtered_logger.py](filtered_logger.py)
Copy the following code into `filtered_logger.py`.
```groovy
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self):
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        NotImplementedError
```
Update the class to accept a list of strings `fields` constructor argument.

Implement the `format` method to filter values in incoming log records using `filter_datum`. Values for fields in `fields` should be filtered.

DO NOT extrapolate `FORMAT` manually. The `format` method should be less than 5 lines long.
```groovy
bob@dylan:~$ cat 1-main.py
#!/usr/bin/env python3
"""
Main file
"""

import logging
import re

RedactingFormatter = __import__('filtered_logger').RedactingFormatter

message = "name=Bob;email=bob@dylan.com;ssn=000-123-0000;password=bobby2019;"
log_record = logging.LogRecord("my_logger", logging.INFO, None, None, message, None, None)
formatter = RedactingFormatter(fields=("email", "ssn", "password"))
print(formatter.format(log_record))

bob@dylan:~$
bob@dylan:~$ ./1-main.py
[HOLBERTON] my_logger INFO 2019-11-19 18:24:25,105: name=Bob; email=***; ssn=***; password=***;
bob@dylan:~$
```

## 2. Create logger: [filtered_logger.py](filtered_logger.py)
Use [user_data.csv](https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/misc/2019/11/a2e00974ce6b41460425.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20240207%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240207T085340Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=7027e9b974107c77c5073a52fa867a23ac72008fe30214b6359a4f2e8dc296d3) for this task

Implement a `get_logger` function that takes no arguments and returns a `logging.Logger` object.

The logger should be named `"user_data"` and only log up to `logging.INFO` level. It should not propagate messages to other loggers. It should have a `StreamHandler` with `RedactingFormatter` as formatter.

Create a tuple `PII_FIELDS` constant at the root of the module containing the fields from `user_data.csv` that are considered PII. `PII_FIELDS` can contain only 5 fields - choose the right list of fields that can are considered as “important” PIIs or information that you **must hide** in your logs. Use it to parameterize the formatter.

**Tips:**

* [What Is PII, non-PII, and personal data?](https://piwik.pro/blog/what-is-pii-personal-data/)
* [Uncovering Password Habits](https://www.digitalguardian.com/blog/uncovering-password-habits-are-users-password-security-habits-improving-infographic)
```groovy
bob@dylan:~$ cat 2-main.py
#!/usr/bin/env python3
"""
Main file
"""

import logging

get_logger = __import__('filtered_logger').get_logger
PII_FIELDS = __import__('filtered_logger').PII_FIELDS

print(get_logger.__annotations__.get('return'))
print("PII_FIELDS: {}".format(len(PII_FIELDS)))

bob@dylan:~$
bob@dylan:~$ ./2-main.py
<class 'logging.Logger'>
PII_FIELDS: 5
bob@dylan:~$
```

## 3. Connect to secure database: [filtered_logger.py](filtered_logger.py)
Database credentials should NEVER be stored in code or checked into version control. One secure option is to store them as environment variable on the application server.

In this task, you will connect to a secure `holberton` database to read a `users` table. The database is protected by a username and password that are set as environment variables on the server named `PERSONAL_DATA_DB_USERNAME` (set the default as “root”), `PERSONAL_DATA_DB_PASSWORD` (set the default as an empty string) and `PERSONAL_DATA_DB_HOST` (set the default as “localhost”).

The database name is stored in `PERSONAL_DATA_DB_NAME`.

Implement a `get_db` function that returns a connector to the database (`mysql.connector.connection.MySQLConnection object`).

* Use the `os` module to obtain credentials from the environment
* Use the module `mysql-connector-python` to connect to the MySQL database (`pip3 install mysql-connector-python`)
```groovy
bob@dylan:~$ cat 3-main.sql
-- setup mysql server
-- configure permissions
CREATE DATABASE IF NOT EXISTS my_db;
CREATE USER IF NOT EXISTS root@localhost IDENTIFIED BY 'root';
GRANT ALL PRIVILEGES ON my_db.* TO 'root'@'localhost';

USE my_db;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    email VARCHAR(256)
);

INSERT INTO users(email) VALUES ("bob@dylan.com");
INSERT INTO users(email) VALUES ("bib@dylan.com");

bob@dylan:~$ 
bob@dylan:~$ cat 3-main.sql | mysql -uroot -p
Enter password: 
bob@dylan:~$ 
bob@dylan:~$ echo "SELECT COUNT(*) FROM users;" | mysql -uroot -p my_db
Enter password: 
2
bob@dylan:~$ 
bob@dylan:~$ cat 3-main.py
#!/usr/bin/env python3
"""
Main file
"""

get_db = __import__('filtered_logger').get_db

db = get_db()
cursor = db.cursor()
cursor.execute("SELECT COUNT(*) FROM users;")
for row in cursor:
    print(row[0])
cursor.close()
db.close()

bob@dylan:~$
bob@dylan:~$ PERSONAL_DATA_DB_USERNAME=root PERSONAL_DATA_DB_PASSWORD=root PERSONAL_DATA_DB_HOST=localhost PERSONAL_DATA_DB_NAME=my_db ./3-main.py
2
bob@dylan:~$
```






























































