# Polls
###### The mini voting app.
[![Build Status](https://travis-ci.org/PetrushynskyiOleksii/polls.svg?branch=master)](https://travis-ci.org/PetrushynskyiOleksii/polls)

#### Requirements
- [pyenv](https://github.com/pyenv/pyenv#installation)
- [pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv#installation)
- python 3.6.5
- django 1.11

#### How to run it locally?
1. Clone this repository and cd into cloned folder
2. Install Python 3.6.5 using pyenv: `pyenv install 3.6.5`
3. Create a new virtual environment : `pyenv virtualenv 3.6.5 <name of virtualenv>`
4. Activate virtual environment : `pyenv local <name of virtualenv>`
5. Install requirements for a project : `pip install -r requirements.txt`
6. Run migrate : `python manage.py migrate`
7. Run server : `python manage.py runserver`

   Also you can create superuser for admin page : `python manage.py createsuperuser`
