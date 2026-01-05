-- 1. Total number of rides
SELECT COUNT(*) AS total_rides
FROM ola_rides;

-- 2. Total revenue
SELECT SUM(Booking_Value) AS total_revenue
FROM ola_rides;

-- 3. Average ride distance
SELECT AVG(Ride_Distance) AS avg_distance
FROM ola_rides;

-- 4. Booking status wise ride count
SELECT Booking_Status, COUNT(*) AS total
FROM ola_rides
GROUP BY Booking_Status;

-- 5. Vehicle type wise ride count
SELECT Vehicle_Type, COUNT(*) AS total
FROM ola_rides
GROUP BY Vehicle_Type;

-- 6. Vehicle type wise revenue
SELECT Vehicle_Type, SUM(Booking_Value) AS revenue
FROM ola_rides
GROUP BY Vehicle_Type;

-- 7. Daily revenue trend
SELECT Booking_Date, SUM(Booking_Value) AS daily_revenue
FROM ola_rides
GROUP BY Booking_Date
ORDER BY Booking_Date;

-- 8. Average driver rating
SELECT AVG(Driver_Rating) AS avg_driver_rating
FROM ola_rides;

-- 9. Average customer rating
SELECT AVG(Customer_Rating) AS avg_customer_rating
FROM ola_rides;

-- 10. Cancelled rides
SELECT COUNT(*) 
FROM ola_rides
WHERE Booking_Status LIKE 'Cancelled%';
