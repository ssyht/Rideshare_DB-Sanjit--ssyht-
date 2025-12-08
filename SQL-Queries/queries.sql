CREATE DATABASE IF NOT EXISTS rideshare_db;
USE rideshare_db;

SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS reservations;
DROP TABLE IF EXISTS trips;
DROP TABLE IF EXISTS vehicles;
DROP TABLE IF EXISTS users;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE users (
    user_id     INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(150) NOT NULL UNIQUE,
    phone       VARCHAR(20),
    role        ENUM('driver','passenger','both') NOT NULL,
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    avg_rating  DECIMAL(3,2)
);

CREATE TABLE vehicles (
    vehicle_id     INT AUTO_INCREMENT PRIMARY KEY,
    owner_user_id  INT NOT NULL,
    plate_no       VARCHAR(20) NOT NULL UNIQUE,
    make           VARCHAR(50),
    model          VARCHAR(50),
    year           INT CHECK (year >= 1990 AND year <= YEAR(CURDATE())),
    color          VARCHAR(30),
    capacity       INT NOT NULL CHECK (capacity > 0),

    CONSTRAINT fk_vehicle_owner
        FOREIGN KEY (owner_user_id)
        REFERENCES users(user_id)
        ON DELETE CASCADE
);

CREATE TABLE trips (
    trip_id        INT AUTO_INCREMENT PRIMARY KEY,
    driver_user_id INT NOT NULL,
    vehicle_id     INT NOT NULL,
    origin         VARCHAR(100) NOT NULL,
    destination    VARCHAR(100) NOT NULL,
    departure_time DATETIME NOT NULL,
    arrival_time   DATETIME,
    seat_price     DECIMAL(8,2) NOT NULL,
    seats_total    INT NOT NULL CHECK (seats_total > 0),

    CONSTRAINT fk_trip_driver
        FOREIGN KEY (driver_user_id)
        REFERENCES users(user_id),

    CONSTRAINT fk_trip_vehicle
        FOREIGN KEY (vehicle_id)
        REFERENCES vehicles(vehicle_id)
);

CREATE TABLE reservations (
    reservation_id    INT AUTO_INCREMENT PRIMARY KEY,
    trip_id           INT NOT NULL,
    passenger_user_id INT NOT NULL,
    seats_reserved    INT NOT NULL CHECK (seats_reserved > 0),
    reserved_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status            ENUM('pending','confirmed','cancelled')
                      NOT NULL DEFAULT 'pending',

    CONSTRAINT fk_res_trip
        FOREIGN KEY (trip_id)
        REFERENCES trips(trip_id),

    CONSTRAINT fk_res_passenger
        FOREIGN KEY (passenger_user_id)
        REFERENCES users(user_id)
);

CREATE TABLE payments (
    payment_id     INT AUTO_INCREMENT PRIMARY KEY,
    reservation_id INT NOT NULL UNIQUE,
    payer_user_id  INT NOT NULL,
    amount         DECIMAL(8,2) NOT NULL CHECK (amount >= 0),
    method         ENUM('card','cash','paypal') NOT NULL,
    status         ENUM('initiated','captured','refunded')
                   NOT NULL DEFAULT 'captured',
    paid_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_payment_reservation
        FOREIGN KEY (reservation_id)
        REFERENCES reservations(reservation_id),

    CONSTRAINT fk_payment_payer
        FOREIGN KEY (payer_user_id)
        REFERENCES users(user_id)
);

CREATE TABLE feedback (
    feedback_id       INT AUTO_INCREMENT PRIMARY KEY,
    trip_id           INT NOT NULL,
    reviewer_user_id  INT NOT NULL,
    reviewee_user_id  INT NOT NULL,
    rating            TINYINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comments          TEXT,
    created_at        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_feedback_reviewer_trip
        UNIQUE (trip_id, reviewer_user_id),

    CONSTRAINT fk_fb_trip
        FOREIGN KEY (trip_id)
        REFERENCES trips(trip_id),

    CONSTRAINT fk_fb_reviewer
        FOREIGN KEY (reviewer_user_id)
        REFERENCES users(user_id),

    CONSTRAINT fk_fb_reviewee
        FOREIGN KEY (reviewee_user_id)
        REFERENCES users(user_id)
);


INSERT INTO users (user_id, name, email, phone, role, created_at, avg_rating)
VALUES
(1, 'John Miller',    'john.miller@example.com',   '555-1010', 'driver',    '2025-11-30 09:00:00', 4.8),
(2, 'Sarah Kim',      'sarah.kim@example.com',     '555-2020', 'passenger','2025-11-30 09:05:00', 4.6),
(3, 'David Lee',      'david.lee@example.com',     '555-3030', 'both',     '2025-11-30 09:10:00', 4.9),
(4, 'Emily Rodriguez','emily.r@example.com',       '555-4040', 'passenger','2025-11-30 09:15:00', 4.7),
(5, 'Michael Brown',  'mike.b@example.com',        '555-5050', 'driver',   '2025-11-30 09:20:00', 4.5);


INSERT INTO vehicles (vehicle_id, owner_user_id, plate_no, make, model, year, color, capacity)
VALUES
(1, 1, 'ABC123', 'Toyota', 'Camry',   2018, 'Silver', 4),
(2, 3, 'XYZ789', 'Honda',  'Civic',   2020, 'Blue',   4),
(3, 5, 'JKL456', 'Tesla',  'Model 3', 2021, 'White',  5);


INSERT INTO trips (trip_id, driver_user_id, vehicle_id, origin, destination,
                   departure_time, arrival_time, seat_price, seats_total)
VALUES
(1, 1, 1,
 'Columbia, MO', 'Kansas City, MO',
 '2025-12-10 09:00:00', '2025-12-10 11:00:00',
 25.00, 4),

(2, 3, 2,
 'Columbia, MO', 'St. Louis, MO',
 '2025-12-12 14:00:00', '2025-12-12 16:00:00',
 30.00, 4),

(3, 5, 3,
 'Columbia, MO', 'Jefferson City, MO',
 '2025-12-15 08:30:00', '2025-12-15 09:10:00',
 15.00, 5);


INSERT INTO reservations (reservation_id, trip_id, passenger_user_id,
                          seats_reserved, reserved_at, status)
VALUES
(1, 1, 2, 1, '2025-11-30 09:30:00', 'confirmed'),
(2, 1, 4, 1, '2025-11-30 09:40:00', 'pending'),
(3, 2, 2, 2, '2025-12-01 13:00:00', 'confirmed'),
(4, 3, 4, 1, '2025-12-02 08:00:00', 'confirmed');


INSERT INTO payments (payment_id, reservation_id, payer_user_id,
                      amount, method, status, paid_at)
VALUES
(1, 1, 2, 25.00, 'card',   'captured', '2025-12-01 10:00:00'),
(2, 3, 2, 60.00, 'paypal', 'captured', '2025-12-02 14:05:00'),
(3, 4, 4, 15.00, 'cash',   'captured', '2025-12-03 09:20:00'),
(4, 2, 4, 25.00, 'card',   'captured', '2025-12-07 18:09:29');


INSERT INTO feedback (feedback_id, trip_id, reviewer_user_id,
                      reviewee_user_id, rating, comments, created_at)
VALUES
(1, 1, 2, 1, 5, 'Great driver, smooth ride!',       '2025-12-11 12:00:00'),
(2, 2, 2, 3, 4, 'Comfortable trip, a bit delayed.', '2025-12-13 17:30:00'),
(3, 3, 4, 5, 5, 'Fast and clean car!',              '2025-12-15 10:00:00');
