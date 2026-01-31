# ============================================================
# Airline Occupancy Analysis
# Business Goal: Identify capacity inefficiencies in flights
# ============================================================

from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- CONNECTION ----------------
engine = create_engine(
    "postgresql+psycopg2://postgres:test@localhost:5432/demo"
)

# ============================================================
# 1. DATA EXTRACTION & PREPARATION (FOUNDATION)
# ============================================================

occupancy = pd.read_sql("""
WITH seat_capacity AS (
    SELECT aircraft_code, COUNT(*) AS total_seats
    FROM bookings.seats
    GROUP BY aircraft_code
),
booked AS (
    SELECT flight_id, COUNT(*) AS booked_seats
    FROM bookings.ticket_flights
    GROUP BY flight_id
)
SELECT
    f.flight_id,
    f.aircraft_code,
    f.departure_airport,
    f.arrival_airport,
    COALESCE(b.booked_seats, 0)::float / sc.total_seats AS occupancy_rate
FROM bookings.flights f
JOIN seat_capacity sc
  ON f.aircraft_code = sc.aircraft_code
LEFT JOIN booked b
  ON f.flight_id = b.flight_id;
""", engine)

print("Total flights analysed:", len(occupancy))
print(occupancy["occupancy_rate"].describe())

# ============================================================
# 2. EDA — UNDERSTANDING THE PROBLEM
# ============================================================

low_occupancy = occupancy[occupancy["occupancy_rate"] < 0.5]

print("\nLow-occupancy flights (<50%):", len(low_occupancy))
print(
    "Percentage low-occupancy:",
    round(len(low_occupancy) / len(occupancy) * 100, 2),
    "%"
)

# -------- CHART 1: OCCUPANCY DISTRIBUTION --------
plt.figure()
plt.hist(occupancy["occupancy_rate"], bins=30)
plt.title("Distribution of Flight Occupancy Rates")
plt.xlabel("Occupancy Rate")
plt.ylabel("Number of Flights")
plt.tight_layout()
plt.show()

# ============================================================
# 3. ANALYTICS — AIRCRAFT-LEVEL PERFORMANCE
# ============================================================

aircraft_analysis = (
    occupancy.groupby("aircraft_code")
    .agg(
        avg_occupancy=("occupancy_rate", "mean"),
        flights=("flight_id", "count"),
        low_occ_flights=("occupancy_rate", lambda x: (x < 0.5).sum())
    )
    .reset_index()
    .sort_values("avg_occupancy")
)

print("\nAircraft-level performance:")
print(aircraft_analysis)

# -------- CHART 2: BOX PLOT (DISTRIBUTION BY AIRCRAFT) --------
plt.figure(figsize=(10, 5))
occupancy.boxplot(
    column="occupancy_rate",
    by="aircraft_code",
    grid=False
)
plt.title("Occupancy Distribution by Aircraft Type")
plt.suptitle("")
plt.xlabel("Aircraft Type")
plt.ylabel("Occupancy Rate")
plt.tight_layout()
plt.show()

# ============================================================
# 4. ANALYTICS — PRIORITIZATION (WHERE TO ACT FIRST)
# ============================================================

top_aircraft = (
    low_occupancy
    .groupby("aircraft_code")
    .size()
    .reset_index(name="low_occ_flights")
    .sort_values("low_occ_flights", ascending=False)
    .head(5)
)

print("\nTop aircraft contributing to low occupancy:")
print(top_aircraft)

# -------- CHART 3: TOP CONTRIBUTORS --------
plt.figure()
plt.bar(
    top_aircraft["aircraft_code"],
    top_aircraft["low_occ_flights"]
)
plt.title("Aircraft Types Contributing Most to Low-Occupancy Flights")
plt.xlabel("Aircraft Type")
plt.ylabel("Number of Low-Occupancy Flights")
plt.tight_layout()
plt.show()

# ============================================================
# 5. KEY TAKEAWAYS (FOR REPORT)
# ============================================================

print("\nKEY INSIGHTS:")
print("- Over half of flights operate below 50% occupancy.")
print("- Low occupancy is concentrated in specific aircraft types.")
print("- Targeted fleet reassignment can improve utilization efficiently.")
