import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Discobear-13",  # your password
        database="rideshare_db"
    )

