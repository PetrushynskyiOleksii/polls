# Polls
Voting app.
[![Build Status](https://travis-ci.org/PetrushynskyiOleksii/polls.svg?branch=master)](https://travis-ci.org/PetrushynskyiOleksii/polls)

## Requirements
- python 3.6.5

## How to run it locally?
   1. Clone this repository and cd into the cloned folder.
       - SSH - `$ git clone git@github.com:PetrushynskyiOleksii/polls.git`
       - HTTPS - `$ git clone https://github.com/PetrushynskyiOleksii/polls.git`
   2. Install virtual virtual environment.
       - using [pyenv](https://github.com/pyenv/pyenv) - `$ pyenv virtualenv 3.6.5 <name of virtualenv>`
       - using [venv](https://docs.python.org/3/library/venv.html#creating-virtual-environments) - `$ python3 -m venv /path/to/new/virtual/environment`
   3. Activate virtual environment.
       - pyenv - `$ pyenv local <name of virtualenv>`
       - venv - `$ source <venv>/bin/activate`
   4. Install project requirements.
      - Base: `$ pip install -r requirements.txt`
      - Dev: `$ pip install -r requirements-dev.txt`
   5. Run migrate : `python manage.py migrate`
   6. Run server : `python manage.py runserver`
   7. Create superuser for admin page : `python manage.py createsuperuser`
