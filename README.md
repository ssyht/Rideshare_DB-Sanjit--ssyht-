# Rideshare_DB-Sanjit--ssyht-
This repo contains all the required files from the Phase 3: Application for the rideshare database with a UI for demo purposes.

**This project is a RideShare Management System that supports:**

* Trip Searching
* Reservation management
* Payment processing
* Driver/passenger feedback
* A full MySQL relational database
* A console-based application
* A Flask Web UI

## 1.1 Connection Used for this Project: 
```bash
host: 127.0.0.1
port: 3306
user: root
password: Discobear-13
database: rideshare_db
```

## 1.2 Source Code: 

```bash
SOURCE rideshare_schema_and_queries.sql;
```

## 1.3 Python Virtual Environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

## 1.4 Running the Console Application: 

* Within in the project root folder, run: 

```bash
(venv) python app.py
```

* The following output should be:

```bash
1. Search Trips
2. Make Reservation
3. Make Payment
4. Leave Feedback
5. Cancel Reservation
6. Exit
```

## 1.5 For Web UI: 

* Change the directory within the same terminal:

```bash
python3 web/flask_app.py
```

* You should see:
```bash
 * Running on http://127.0.0.1:5000
```

* Open the URL and you should be able to see the Web UI.

## Sample Tests: 

* You can sample test it using the synthetic data that is present in the ``Data`` folder within in this GitHub Repository.


By Sanjit Subhash - University of Missouri Columbia



