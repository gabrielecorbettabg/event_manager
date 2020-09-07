# EVENT MANAGER
This Django project consists of two apps: `events` contains the logic for event management,
while`users` the logic related to user registration,login and logout.

## Prerequisites
You will need to have `python3.7` installed.

## Install
After cloning the repo, follow the steps below:

1. Set up virtual environment
```shell
$ python3.7 -m virtualenv venv
``` 
then activate it 
```shell
source ./venv/bin/activate
```
and finally install the requirements
```shell
pip install -r requirements.txt
```
2
. Create a database by running, from inside the deeper `event_manager` directory,
```shell
python manage.py migrate
```
3
. You can create a database admin super user by running
```shell
python manage.py createsuperuser
```

## Usage
From within the deeper `event_manager` folder, run:
```shell
python manage.py runserver
```
and go to localhost:8000/

## Tests
Tests are located in the tests folder in each application folder.
You can run the full suite by executing
```shell
python manage.py test
```
You can run the tests for each app separately by running:
 ```shell
python manage.py test <app_name>.tests
```
where `<app_name>` is either `users` or `events`. 