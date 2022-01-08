# README.md

# Paperhub: A Notes sharing webapp
Django based webapp that allows users to share notes.

## Live Demo
The webapp is already deployed on heroku.com

Live webapp: [paperhub-heroku](https://paperhub-prototype.herokuapp.com)

## Installation

### Development
I have used python-3.8.10 and [virtualenv](https://docs.python.org/3/library/venv.html) as a primary tools for development.

### Steps to manually install and start the webapp:
* Clone the repository
* Create a virtual environment 'python3 -m venv vitualenv'
* Activate the virtual environment 'source ./vitualenv/bin/activate'
* Install all the project dependencies 'pip install -r [requirements.txt](requirements.txt)'
* Migrate the changes to database (if any) 'python manage.py makemigrations && python manage.py migrate'
* Set the all the required env variables.
* Start the webapp 'python manage.py runserver'
* The webapp will be available at 'http://127.0.0.1:8000/'

