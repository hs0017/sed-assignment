# SurreyLM

Surrey License Management System.

## Description

SurreyLM is a web-based software application for managing software licenses built for the University of Surrey. 

Many commercial software licenses require yearly renewal, so it can become difficult to keep track of these if your organisation has lots of different software packages. This is where SurreyLM can help!

## Getting Started

### Dependencies

Python3.11 with the following modules: 

* blinker v1.6.2
* click v8.1.6
* Flask v2.3.2
* Flask-Login v0.6.2
* Flask-SQLAlchemy v3.0.5
* greenlet v2.0.2
* itsdangerous v2.1.2
* Jinja2 v3.1.2
* MarkupSafe v2.1.3
* python-dateutil v2.8.2
* six v1.16.0
* SQLAlchemy v2.0.19
* typing_extensions v4.7.1
* Werkzeug v2.3.6

### Installing

* Clone the repository to your local machine
* cd into the cloned 'surreylm' directory
* Install virtualenv:
```
pip install virtualenv
```
* Create a virtual environment:
```
virtualenv venv
```
* Activate the virtual environment:
```
source venv/bin/activate
```
* Run the following command to install the dependencies:
```
pip install -r requirements.txt
```
* Run the following command to start the application:
```
FLASK_APP=main.py flask run 
```
* If you want to run the tests cd to the directory above 'surreylm' and run:
```
pip install pytest
pytest surreylm/test/test_surreylm.py
```

## Help

If you encounter errors, then please check the errorlog.txt file. 

You can also [Submit an issue](https://github.com/hs0017/sea-assignment/issues)

## Authors

Contributors names and contact info

* Holly Sherlock - [LinkedIn](https://www.linkedin.com/in/holly-sherlock/)
