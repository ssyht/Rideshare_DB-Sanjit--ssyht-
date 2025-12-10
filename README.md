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


For successful setup, clone this repository to your local device

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


### Reservations

```sql
SELECT reservation_id, trip_id, passenger_user_id, seats_reserved, status, reserved_at
FROM reservations
ORDER BY reservation_id DESC;
```

### To See a Specific Reservation

```sql
SELECT reservation_id, trip_id, seats_reserved, status, reserved_at
FROM reservations
WHERE passenger_user_id = 2
ORDER BY reserved_at DESC;
```

### After Making Payment

```sql
SELECT payment_id, reservation_id, payer_user_id, amount, method, status, paid_at
FROM payments
ORDER BY payment_id DESC;
```

### Payment for a specific reservation

```sql
SELECT payment_id, reservation_id, payer_user_id, amount, method, status, paid_at
FROM payments
WHERE reservation_id = 2;   -- change 2 to whatever you tested
```

### Join reservation + payment

```sql
SELECT 
    p.payment_id,
    p.reservation_id,
    u.name AS payer_name,
    p.amount,
    p.method,
    p.status,
    p.paid_at
FROM payments p
JOIN users u ON u.user_id = p.payer_user_id
ORDER BY p.payment_id DESC;
```

### After Leaving Feedback

```sql
SELECT feedback_id, trip_id, reviewer_user_id, reviewee_user_id, rating, comments, created_at
FROM feedback
ORDER BY feedback_id DESC;
```

***To see feedback for one trip:***

```sql
SELECT feedback_id, reviewer_user_id, reviewee_user_id, rating, comments, created_at
FROM feedback
WHERE trip_id = 1  
ORDER BY feedback_id DESC;
```












By Sanjit Subhash - University of Missouri Columbia



