import csv
import mysql.connector

# -------------------------------------
# 1. CONNECT TO YOUR DATABASE
# -------------------------------------
cnx = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Discobear-13",
    database="rideshare_db"
)

cursor = cnx.cursor()

# -------------------------------------
# 2. LIST OF TABLES TO EXPORT
# -------------------------------------
tables = [
    "users",
    "vehicles",
    "trips",
    "reservations",
    "payments",
    "feedback"
]

# -------------------------------------
# 3. EXPORT EACH TABLE AS CSV
# -------------------------------------
for table in tables:
    query = f"SELECT * FROM {table};"
    cursor.execute(query)
    rows = cursor.fetchall()

    # column names
    headers = [desc[0] for desc in cursor.description]

    filename = f"{table}.csv"
    print(f"Saving {filename} ...")

    # Write CSV file
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)   # write header row
        writer.writerows(rows)     # write all data

print("\nAll tables exported successfully!")

cursor.close()
cnx.close()

