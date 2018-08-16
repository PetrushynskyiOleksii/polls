# Polls
Voting app.
[![Build Status](https://travis-ci.org/PetrushynskyiOleksii/polls.svg?branch=master)](https://travis-ci.org/PetrushynskyiOleksii/polls)

## Requirements
- python 3.6.5
- docker & docker-compose

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
| GET    | /question/top/                               | Return top 10 popular questions                 |
| GET    | /question/{pk}/                              | Retrieve question's instance                    |
| PUT    | /question/{pk}/                              | Update question's instance (*Look note bellow*) |
| DELETE | /question/{pk}/                              | Delete question's instance                      |
| POST   | /question/{question_pk}/votefor/{answer_pk}/ | Create a vote to the corresponding answer       |
| GET    | /question/{question_pk}/{pk}                 | Retrieve answer's instance                      |
| PUT    | /question/{question_pk}/{pk}                 | Update answer's instance                        |
| DELETE | /question/{question_pk}/{pk}                 | Delete answer's instance                        |

>Note: This way of update will create new instances for every modified answer, as a result of which will change
id and vote_count will nullified. **Strongly recommended** to use endpoint for update particular answer.

*For more information about opportunities you need to go through the following section.*
## How to run it locally?
1. Clone this repository and cd into the cloned folder.
   - SSH - `$ git clone git@github.com:PetrushynskyiOleksii/polls.git`
   - HTTPS - `$ git clone https://github.com/PetrushynskyiOleksii/polls.git`
2. Create a file `touch src/main/.env` with following variables like as::
    ```bash
       DB_NAME=pollsdb
       DB_USER=pollsuser
       DB_PASSWORD=pollspassword
       PG_HOST=postgres
       PG_PORT=5432
       SECRET_KEY=secretdjangokey
    ```
3. Run docker-compose: `$ docker-compose up -d`
4. API documentation endpoint: `http://localhost:8000/api/`

- Create super user: `$ docker exec -ti polls python ./src/manage.py createsuperuser `
- For shell accessing: `$ docker exec -ti <container> bash`
- For logs: `$ docker-compose logs <container>`
