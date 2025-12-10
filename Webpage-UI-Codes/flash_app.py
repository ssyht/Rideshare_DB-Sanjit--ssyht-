from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# -------------------------
# DATABASE CONNECTION
# -------------------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Discobear-13",
        database="rideshare_db"
    )

# -------------------------
# HOME PAGE
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")

# -------------------------
# SEARCH TRIPS
# -------------------------
@app.route("/search")
def search():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM trips")
    trips = cursor.fetchall()

    conn.close()
    return render_template("search.html", trips=trips)

# -------------------------
# RESERVE — SHOW TRIP DETAILS
# -------------------------
@app.route("/reserve/<int:trip_id>")
def reserve(trip_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM trips WHERE trip_id = %s", (trip_id,))
    trip = cursor.fetchone()
    conn.close()

    if not trip:
        return render_template("results.html",
                               message="Error",
                               highlight="Trip not found.")

    return render_template("reserve.html", trip=trip)

# -------------------------
# RESERVE CONFIRMATION
# -------------------------
@app.route("/reserve_confirm", methods=["POST"])
def reserve_confirm():
    trip_id = request.form["trip_id"]
    user_id = request.form["user_id"]
    seats = request.form["seats"]

    conn = get_db_connection()
    cursor = conn.cursor()

    insert = """
        INSERT INTO reservations (trip_id, passenger_user_id, seats_reserved, status)
        VALUES (%s, %s, %s, 'confirmed')
    """

    cursor.execute(insert, (trip_id, user_id, seats))
    conn.commit()
    conn.close()

    return render_template(
        "results.html",
        message="Reservation Created!",
        highlight=f"Trip #{trip_id} • User #{user_id} • {seats} seats"
    )

# -------------------------
# PAYMENT PAGE
# -------------------------
@app.route("/payment")
def payment():
    return render_template("payment.html")

# -------------------------
# PAYMENT CONFIRMATION
# -------------------------
@app.route("/payment_confirm", methods=["POST"])
def payment_confirm():
    reservation_id = request.form["reservation_id"]
    payer_id = request.form["payer_id"]
    amount = request.form["amount"]
    method = request.form["method"]

    conn = get_db_connection()
    cursor = conn.cursor()

    insert = """
        INSERT INTO payments (reservation_id, payer_user_id, amount, method, status, paid_at)
        VALUES (%s, %s, %s, %s, 'captured', %s)
    """
    cursor.execute(insert, (reservation_id, payer_id, amount, method, datetime.now()))
    conn.commit()
    conn.close()

    return render_template(
        "results.html",
        message="Payment Successful!",
        highlight=f"Reservation #{reservation_id} • ${amount} via {method}"
    )

# -------------------------
# FEEDBACK PAGE
# -------------------------
@app.route("/feedback")
def feedback():
    return render_template("feedback.html")

@app.route("/feedback_submit", methods=["POST"])
def feedback_submit():
    trip_id = request.form["trip_id"]
    reviewer_id = request.form["reviewer_id"]
    reviewee_id = request.form["reviewee_id"]
    rating = request.form["rating"]
    comments = request.form["comments"]

    conn = get_db_connection()
    cursor = conn.cursor()

    insert = """
        INSERT INTO feedback (trip_id, reviewer_user_id, reviewee_user_id, rating, comments)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(insert, (trip_id, reviewer_id, reviewee_id, rating, comments))
    conn.commit()
    conn.close()

    return render_template(
        "results.html",
        message="Feedback Submitted!",
        highlight=f"Trip #{trip_id} • Rating {rating}/5"
    )

# -------------------------
# CANCEL RESERVATION
# -------------------------
@app.route("/cancel")
def cancel():
    return render_template("cancel.html")

@app.route("/cancel_confirm", methods=["POST"])
def cancel_confirm():
    reservation_id = request.form["reservation_id"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE reservations SET status='cancelled' WHERE reservation_id=%s", (reservation_id,))
    conn.commit()
    conn.close()

    return render_template(
        "results.html",
        message="Reservation Cancelled",
        highlight=f"Reservation #{reservation_id} is now cancelled"
    )

# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
