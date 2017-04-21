# Build2myprint
Example of Hello World in Django with Tequila Authentication


## How to make it work

### Virtualenv
Create and activate a virtualenv for the project:
    * `sudo pip3
    * `virtualenv ./.venv` in the project folder
    * `source ./.venv/bin/activate` to activate the virtualenv (on linux)
Then run: `pip install -r requirements/base.txt`

### Database
* Install MySQL on your system
* Create a database named `django_examples` (`CREATE DATABASE django_example;`)
* Create a user named `django_example` (`CREATE USER "django_example"@"localhost"`)
* Set the password for user `django_example` (`SET password FOR "django_example"@"localhost" = password('db_password')`)
* Give all the rights on the database `django_example` to the user `django_example` (`GRANT ALL ON django_example.* TO "django_example"@"localhost"`)

### Secrets file
Create a file named secrets.json in the `django_example` folder containing the following :

```
{
    "SECRET_KEY": "what_you_want",
    "DB_PASSWORD": "db_password"
}
```

This file is used to avoid having passwords in the git repository. The SECRET_KEY can be anything (it is "abcde" on my dev machine), it just needs to be unique and long in the production server.

### Last setups
* Apply migrations to let Django setup the database. Inside the folder `django_example` with the virtualenv activated, run :
    * `python manage.py makemigrations`
    * `python manage.py migrate`
* Giving yourself login rights to the `logged` page and to the admin : `python manage.py createsuperuser --username=<username_tequila> --email=<email_epfl>`


### Make it run
* `python manage.py runserver`
* In a browser go to `http://localhost:8000/hello_world/`
* The admin can be found on `http://localhost:8000/admin/`


## Differences between this code and django tutorial
In this example we adopt a different project layout from the tutorial, following a set of good practices used on other EPFL projects and presented in the book `Two scoops of Django`. Here are the changes :
* All the requirements file are under the requirements folder. The `base.txt` contains the packages needed on all the systems in which the project might run (dev computer, test server, production server). We can in the future create new requirements file for specific purposes, for example a `ci.txt` file to setup specific packages for continuous integration not needed in other setups (coverage, flake8, etc...)
* the base `urls.py` file and the `wsgi.py` file are under the config folder.
* the `settings.py` file is now under `config/base.py` for exactly the same reasons as the requirements, in the futur we will need different configs depending on the environment


## Django-tequila

You can find django-tequila documentation [here](https://pypi.python.org/pypi/django-tequila/2.1.7)


## Contact
Made by Gil Brechbühler. E-Mail : gil.brechbuhler@epfl.ch, do not hesitate to ask any question.
