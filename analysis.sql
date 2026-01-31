-- ============================================================
-- AIRLINE FLIGHT OCCUPANCY ANALYSIS
-- ============================================================
-- Business Objective:
-- Identify structural inefficiencies in flight capacity
-- to improve seat utilization and airline profitability.
--
-- Database: PostgreSQL
-- Schema  : bookings
-- Grain   : One row per flight
-- ============================================================


-- ============================================================
-- 1. CREATE TEMP TABLE: FLIGHT OCCUPANCY
-- ============================================================
-- TEMP TABLE allows reuse across multiple queries
-- without repeating complex joins.
-- ============================================================

DROP TABLE IF EXISTS flight_occupancy;

CREATE TEMP TABLE flight_occupancy AS
SELECT
    f.flight_id,
    f.aircraft_code,
    f.departure_airport,
    f.arrival_airport,
    COALESCE(b.booked_seats, 0)::FLOAT / sc.total_seats AS occupancy_rate
FROM bookings.flights f
JOIN (
    SELECT
        aircraft_code,
        COUNT(*) AS total_seats
    FROM bookings.seats
    GROUP BY aircraft_code
) sc
    ON f.aircraft_code = sc.aircraft_code
LEFT JOIN (
    SELECT
        flight_id,
        COUNT(*) AS booked_seats
    FROM bookings.ticket_flights
    GROUP BY flight_id
) b
    ON f.flight_id = b.flight_id;


-- ============================================================
-- 2. OVERALL BUSINESS HEALTH CHECK
-- ============================================================

SELECT
    COUNT(*) AS total_flights,
    COUNT(*) FILTER (WHERE occupancy_rate < 0.50) AS low_occupancy_flights,
    ROUND(
        COUNT(*) FILTER (WHERE occupancy_rate < 0.50)::NUMERIC
        / COUNT(*) * 100,
        2
    ) AS pct_low_occupancy
FROM flight_occupancy;


-- ============================================================
-- 3. OCCUPANCY DISTRIBUTION (EDA)
-- ============================================================

SELECT
    CASE
        WHEN occupancy_rate < 0.25 THEN '0–25%'
        WHEN occupancy_rate < 0.50 THEN '25–50%'
        WHEN occupancy_rate < 0.75 THEN '50–75%'
        ELSE '75–100%'
    END AS occupancy_bucket,
    COUNT(*) AS flights
FROM flight_occupancy
GROUP BY occupancy_bucket
ORDER BY flights DESC;


-- ============================================================
-- 4. AIRCRAFT-LEVEL PERFORMANCE
-- ============================================================

SELECT
    aircraft_code,
    COUNT(*) AS total_flights,
    ROUND(AVG(occupancy_rate)::NUMERIC, 3) AS avg_occupancy,
    COUNT(*) FILTER (WHERE occupancy_rate < 0.50) AS low_occ_flights
FROM flight_occupancy
GROUP BY aircraft_code
ORDER BY avg_occupancy;


-- ============================================================
-- 5. PARETO ANALYSIS (PRIORITIZATION)
-- ============================================================

WITH aircraft_low_occ AS (
    SELECT
        aircraft_code,
        COUNT(*) AS low_occ_flights
    FROM flight_occupancy
    WHERE occupancy_rate < 0.50
    GROUP BY aircraft_code
)
SELECT
    aircraft_code,
    low_occ_flights,
    ROUND(
        SUM(low_occ_flights) OVER (
            ORDER BY low_occ_flights DESC
        )::NUMERIC
        / SUM(low_occ_flights) OVER () * 100,
        2
    ) AS cumulative_percentage
FROM aircraft_low_occ
ORDER BY low_occ_flights DESC;


-- ============================================================
-- 6. ROUTE-LEVEL STRUCTURAL ANALYSIS (TOP 20 WORST)
-- ============================================================

SELECT
    departure_airport,
    arrival_airport,
    COUNT(*) AS total_flights,
    ROUND(AVG(occupancy_rate)::NUMERIC, 3) AS avg_occupancy
FROM flight_occupancy
GROUP BY departure_airport, arrival_airport
HAVING COUNT(*) >= 30
ORDER BY avg_occupancy
LIMIT 10;


-- ============================================================
-- 7. WORST AIRCRAFT–ROUTE COMBINATIONS (TOP 20)
-- ============================================================

SELECT
    aircraft_code,
    departure_airport,
    arrival_airport,
    COUNT(*) AS flights,
    ROUND(AVG(occupancy_rate)::NUMERIC, 3) AS avg_occupancy
FROM flight_occupancy
GROUP BY aircraft_code, departure_airport, arrival_airport
HAVING COUNT(*) >= 20
ORDER BY avg_occupancy
LIMIT 10;


-- ============================================================
-- END OF ANALYSIS
-- ============================================================
