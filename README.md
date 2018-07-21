# Polls
Voting app.
[![Build Status](https://travis-ci.org/PetrushynskyiOleksii/polls.svg?branch=master)](https://travis-ci.org/PetrushynskyiOleksii/polls)

## Requirements
- python 3.6.5
## User stories
- An authenticated user can create questions, delete/update questions created by him.
- An authenticated user can get details of the question
- An authenticated user can vote.
- An unauthenticated user can get list of all existing questions.

## Endpoints
| Method | URL                                          | Description                                     |
|--------|----------------------------------------------|-------------------------------------------------|
| POST   | /users/signup/                               | Create a new user and return token              |
| POST   | /users/login/                                | Authenticate a user and return token            |
| GET    | /question/                                   | Return list of all existing questions           |
| POST   | /question/                                   | Create a new question's instance                |
| GET    | /question/{pk}/                              | Retrieve question's instance                    |
| PUT    | /question/{pk}/                              | Update question's instance (*Look note bellow*) |
| DELETE | /question/{pk}/                              | Delete question's instance                      |
| POST   | /question/{question_pk}/votefor/{answer_pk}/ | Create a vote to the corresponding answer       |
| GET    | /question/{question_pk}/{pk}                 | Retrieve answer's instance                      |
| PUT    | /question/{question_pk}/{pk}                 | Update answer's instance                        |
| DELETE | /question/{question_pk}/{pk}                 | Delete answer's instance                        |

>Note: This way of update will create new instances for every modified answer, as a result of which will change
id and vote_count will nullified. **Strongly recommended** to use endpoint for update particular answer.

*For more information about opportunities you need to go through the following section, especially point 8.*
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
5. Run migrate : `python ./src/manage.py migrate`
6. Run server : `python ./src/manage.py runserver`
7. Create superuser for admin page : `python ./src/manage.py createsuperuser`
8. To read the api documentation, open in browser `http://localhost:8000/api/`
