## WELCOME TO MY API
[![Build Status](https://travis-ci.org/pythonGeek/bucketlist_api.svg?branch=master)](https://travis-ci.org/pythonGeek/bucketlist_api)
[![Coverage Status](https://coveralls.io/repos/github/pythonGeek/bucketlist_api/badge.svg?branch=master)](https://coveralls.io/github/pythonGeek/bucketlist_api?branch=master)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/hyperium/hyper/master/LICENSE)
[![Issue Count](https://codeclimate.com/github/pythonGeek/bucketlist_api/badges/issue_count.svg)](https://codeclimate.com/github/pythonGeek/bucketlist_api)
#BucketList Application API

## Introduction

> This application is a Flask API for a bucket list service that allows users to create, update and delete bucket lists. It also provides programmatic access to the items added to the items created. This API is a REST API and the return format for all endpoints is JSON.

## Endpoints

1. `POST /auth/login`
2. `POST /auth/register`
3. `GET /bucketlists/`: returns all bucket listing of all buckets list
4. `GET /bucketlists/<bucketlist_id>`: returns the bucket list with the specified ID
5. `PUT /bucketlist/<bucketlist_id>`: updates the bucket list with the specified with the provided data
6. `DELETE /bucketlist/<bucketlist_id>`: deletes the bucket list with the specified ID
7. `POST /bucketlists/<bucketlist_id>/items/`: adds a new item to the bucket list with the specified ID
8. `PUT /bucketlists/<bucketlist_id>/items/<item_id>`: updates the item with the given item ID from the bucket list with the provided ID
9. `DELETE /bucketlists/<bucketlist_id>/items/<item_id>`: deletes the item with the specified item ID from the bucket list with the provided ID

## Installation & Setup
1. Download & Install Python
 	* Head over to the [Python Downloads](https://www.python.org/downloads/) Site and download a version compatible with your operating system
 	* To confirm that you have successfully installed Python:
		* Open the Command Prompt on Windows or Terminal on Mac/Linux
		* Type python
		* If the Python installation was successfull you the Python version will be printed on your screen and the python REPL will start
2. Clone the repository to your personal computer to any folder
 	* On GitHub, go to the main page of the repository [BucketList API](git@github.com:pythonGeek/bucketlist_api.git)
 	* On your right, click the green button 'Clone or download'
 	* Copy the URL
 	* Enter the terminal on Mac/Linux or Git Bash on Windows
 	* Type `git clone ` and paste the URL you copied from GitHub
 	* Press *Enter* to complete the cloning process
3. Virtual Environment Installation
 	* Install the virtual environment by typing: `pip install virtualenv` on your terminal
4. Create a virtual environment by running `virtualenv --python python bl-venv`. This will create the virtual environment in which you can run the project.
5. Activate the virtual environment by running `source bl-venv/bin/activate`
6. Enter the project directory by running `cd cp2_blapi`
7. Once inside the directory install the required modules
 	* Run `pip install -r requirements.txt`
8. Inside the application folder run the main.py file:
 * On the terminal type `python main.py` to start the application

 ## Perform migrations
```
python server.py db init
python server.py db migrate
python server.py db upgrade


## Testing
To run the tests for the app, and see the coverage, run
```
nosetests --with-coverage --cover-package=app
```

### Bucketlist's resources
The API resources are accessible at [localhost:8000/api/v1/](http://127.0.0.1:8000). They include:

| Resource URL | Methods | Description |
| -------- | ------------- | --------- |
| `/` | GET  | The index |
| `/auth/register/` | POST  | User registration |
|  `/auth/login/` | POST | User login|
| `/bucketlists/` | GET, POST | A user's bucket lists |
| `/bucketlists/<bucketlist_id>/` | GET, PUT, DELETE | A single bucket list |
| `/bucketlists/<bucketlist_id>/items/` | GET, POST | Items in a bucket list |
| GET `/bucketlists/<bucketlist_id>/items/<item_id>/` | GET, PUT, DELETE| A single bucket list item|


| Method | Description |
|------- | ----------- |
| GET | Retrieves a resource(s) |
| POST | Creates a new resource |
| PUT | Updates an existing resource |
| DELETE | Deletes an existing resource |
