import mysql.connector
from mysql.connector import Error

# ------------------------------
# Database Connection
# ------------------------------

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Discobear-13",
            database="rideshare_db"
        )
        return conn
    except Error as e:
        print("Error connecting to MySQL:", e)
        return None


# ------------------------------
# Function 1: Search available trips
# ------------------------------

def search_trips():
    origin = input("Enter origin: ")
    destination = input("Enter destination: ")

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT 
        t.trip_id, u.name AS driver_name, v.make, v.model, 
        t.origin, t.destination, t.departure_time, t.seat_price,
        (t.seats_total - COALESCE(st.seats_taken, 0)) AS seats_available
    FROM trips t
    JOIN users u ON u.user_id = t.driver_user_id
    JOIN vehicles v ON v.vehicle_id = t.vehicle_id
    LEFT JOIN (
        SELECT trip_id, SUM(seats_reserved) AS seats_taken
        FROM reservations
        WHERE status = 'confirmed'
        GROUP BY trip_id
    ) st ON st.trip_id = t.trip_id
    WHERE t.origin = %s AND t.destination = %s;
    """

    cursor.execute(query, (origin, destination))
    results = cursor.fetchall()

    print("\n--- Available Trips ---")
    for row in results:
        print(f"Trip ID: {row[0]}, Driver: {row[1]}, Car: {row[2]} {row[3]}, "
              f"Departs: {row[6]}, Price: ${row[7]}, Seats Left: {row[8]}")

    cursor.close()
    conn.close()


# ------------------------------
# Function 2: Create a reservation
# ------------------------------

def make_reservation():
    trip_id = input("Trip ID: ")
    user_id = input("Passenger User ID: ")
    seats = int(input("Seats to reserve: "))

    conn = get_connection()
    cursor = conn.cursor()

    # Check available seats
    check_query = """
    SELECT (t.seats_total - COALESCE(st.seats_taken,0)) AS seats_available
    FROM trips t
    LEFT JOIN (
        SELECT trip_id, SUM(seats_reserved) AS seats_taken
        FROM reservations
        WHERE status='confirmed'
        GROUP BY trip_id
    ) st ON st.trip_id = t.trip_id
    WHERE t.trip_id = %s;
    """

    cursor.execute(check_query, (trip_id,))
    result = cursor.fetchone()

    if not result:
        print("Trip not found.")
    elif result[0] < seats:
        print(f"Not enough seats available. Only {result[0]} left.")
    else:
        insert_query = """
        INSERT INTO reservations (trip_id, passenger_user_id, seats_reserved, status)
        VALUES (%s, %s, %s, 'confirmed');
        """
        cursor.execute(insert_query, (trip_id, user_id, seats))
        conn.commit()
        print("Reservation created successfully!")

    cursor.close()
    conn.close()


# ------------------------------
# Function 3: Record a payment
# ------------------------------

def make_payment():
    reservation_id = input("Reservation ID: ")
    payer_id = input("Payer User ID: ")

    conn = get_connection()
    cursor = conn.cursor()

    # Compute total amount
    compute_query = """
    SELECT (r.seats_reserved * t.seat_price) AS amount
    FROM reservations r
    JOIN trips t ON t.trip_id = r.trip_id
    WHERE r.reservation_id = %s;
    """

    cursor.execute(compute_query, (reservation_id,))
    result = cursor.fetchone()

    if not result:
        print("Reservation not found.")
        return

    amount = result[0]
    method = input("Payment method (card/cash/paypal): ")

    insert_payment = """
    INSERT INTO payments (reservation_id, payer_user_id, amount, method, status, paid_at)
    VALUES (%s, %s, %s, %s, 'captured', NOW());
    """

    cursor.execute(insert_payment, (reservation_id, payer_id, amount, method))
    conn.commit()
    print(f"Payment of ${amount} completed successfully!")

    cursor.close()
    conn.close()


# ------------------------------
# Function 4: Leave feedback
# ------------------------------

def leave_feedback():
    reservation_id = input("Reservation ID: ")
    rating = input("Rating (1-5): ")
    comment = input("Comment: ")

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO feedback (trip_id, reviewer_user_id, reviewee_user_id, rating, comments)
    SELECT t.trip_id, r.passenger_user_id, t.driver_user_id, %s, %s
    FROM reservations r
    JOIN trips t ON t.trip_id = r.trip_id
    WHERE r.reservation_id = %s;
    """

    cursor.execute(query, (rating, comment, reservation_id))
    conn.commit()

    print("Feedback submitted successfully!")

    cursor.close()
    conn.close()


# ------------------------------
# Function 5: Cancel a reservation
# ------------------------------

def cancel_reservation():
    reservation_id = input("Reservation ID: ")

    conn = get_connection()
    cursor = conn.cursor()

    update_query = """
    UPDATE reservations
    SET status = 'cancelled'
    WHERE reservation_id = %s;
    """

    cursor.execute(update_query, (reservation_id,))
    conn.commit()

    print("Reservation cancelled.")

    cursor.close()
    conn.close()


# ------------------------------
# Menu
# ------------------------------

def main_menu():
    while True:
        print("\n------------------------------")
        print(" RideShare System Menu")
        print("------------------------------")
        print("1. Search Trips")
        print("2. Make Reservation")
        print("3. Make Payment")
        print("4. Leave Feedback")
        print("5. Cancel Reservation")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            search_trips()
        elif choice == "2":
            make_reservation()
        elif choice == "3":
            make_payment()
        elif choice == "4":
            leave_feedback()
        elif choice == "5":
            cancel_reservation()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

# Run program
main_menu()

