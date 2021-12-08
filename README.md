# WordUp

![logo](app/static/images/logo.png)

Group Project for CSPB3308

## Team Members

Claudia Hidrogo, Raul Ramos, Christie Hui

## Vision Statement

WordUp aims to provide a useful tool for users to be able to study vocabulary words in preparation for certain exams (e.g. the GRE) or for general vocabulary improvement.

## Motivation

The motivation behind this project is to aid users with tracking their vocabulary study progress in an efficient manner.

## Risks to project completion (tentative)

Risks to project completion include but are not limited to:
- new working environment 
- little prior experience with working with respective team members

## Mitigation Strategy for above risks

- weekly progress check-ins

## Development method

Agile, primarily using Jira for story/feature tracking

## Technologies Used

- Flask
- Python3
- PostgreSQL
- HTML & CSS

## Set Up Environment

1. Clone the repository
```shell
git clone https://github.com/chui15/wordup.git
```

2. Activate the virtual environment from one directory up, install necessary dependencies, then run the Flask application from within the wordup directory
``` shell
source wordup/bin/activate
cd wordup
pip install -r requirements.txt
export FLASK_APP=app/main.py
export FLASK_ENV=development
flask run
```