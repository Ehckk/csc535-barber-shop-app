# csc535-barber-shop-app
Term Project for CSC-535

## Dependencies

### Required

MySQL Server    >= 8.0.34   [Download](https://dev.mysql.com/downloads/installer/)

Python          >= 3.11.8   [Download](https://www.python.org/downloads/)

## Creating .flaskenv
Create a `.flaskenv` file in the root folder of the project. 

Within the  `.flaskenv` file, add the following contents:
```
FLASK_APP='main.py'
FLASK_DEBUG=1
MYSQL_IP='127.0.0.1'
MYSQL_PORT=3306
MYSQL_USER='root'
MYSQL_PASSWORD='YOUR_MYSQL_ROOT_PASSWORD'
MYSQL_DB='csc535_barber'
```

This file is **ignored by git**

## Creating a virtual environment
Create a python virtual environment for the project:
```
python -m venv venv
```
The virtual environment is **ignored by git**

Activate the virtual environment:
- Windows:
	```
	venv/Scripts/activate
	```
- MacOS or Linux:
	```
	source venv/bin/activate
	```

Install the project dependencies to the project:
```
pip install -r requirements.txt
```

Run the application
```
flask run
```

See [this link](https://docs.python.org/3/library/venv.html) for more information.
