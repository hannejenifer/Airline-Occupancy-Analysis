from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

# ---------------- DATABASE CONNECTION ----------------
load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

# ============================================================
# 1. LOAD CORE DATA (FROM SQL LOGIC)
# ============================================================

occupancy = pd.read_sql("""
SELECT
    f.flight_id,
    f.aircraft_code,
    f.departure_airport,
    f.arrival_airport,
    COALESCE(b.booked_seats, 0)::float / sc.total_seats AS occupancy_rate
FROM bookings.flights f
JOIN (
    SELECT aircraft_code, COUNT(*) AS total_seats
    FROM bookings.seats
    GROUP BY aircraft_code
) sc ON f.aircraft_code = sc.aircraft_code
LEFT JOIN (
    SELECT flight_id, COUNT(*) AS booked_seats
    FROM bookings.ticket_flights
    GROUP BY flight_id
) b ON f.flight_id = b.flight_id;
""", engine)

print("Total flights analysed:", len(occupancy))

# ============================================================
# 2. EDA — OCCUPANCY DISTRIBUTION
# ============================================================

plt.figure()
plt.hist(occupancy["occupancy_rate"], bins=30)
plt.title("Distribution of Flight Occupancy Rates")
plt.xlabel("Occupancy Rate")
plt.ylabel("Number of Flights")
plt.tight_layout()
plt.show()

# ============================================================
# 3. AIRCRAFT-LEVEL PERFORMANCE
# ============================================================

aircraft_perf = (
    occupancy.groupby("aircraft_code")
    .agg(
        avg_occupancy=("occupancy_rate", "mean"),
        total_flights=("flight_id", "count"),
        low_occupancy_flights=("occupancy_rate", lambda x: (x < 0.5).sum())
    )
    .sort_values("avg_occupancy")
)

print("\nAircraft Performance Summary:")
print(aircraft_perf)

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
# 4. PRIORITIZATION — WHERE TO ACT FIRST
# ============================================================

top_contributors = (
    aircraft_perf
    .sort_values("low_occupancy_flights", ascending=False)
    .head(5)
)

plt.figure()
plt.bar(
    top_contributors.index,
    top_contributors["low_occupancy_flights"]
)
plt.title("Aircraft Types Contributing Most to Low-Occupancy Flights")
plt.xlabel("Aircraft Type")
plt.ylabel("Low-Occupancy Flights")
plt.tight_layout()
plt.show()

# ============================================================
# 5. KEY TAKEAWAYS (LOGGED)
# ============================================================

print("\nKEY INSIGHTS:")
print("- Majority of flights operate below optimal occupancy.")
print("- Low occupancy is concentrated in specific aircraft types.")
print("- Targeted fleet reassignment offers high-impact optimization.")
