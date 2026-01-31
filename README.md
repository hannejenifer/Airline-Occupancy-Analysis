# Airline Flight Occupancy Analysis  
**SQL & Python Data Analytics Project**

---

## 📌 Project Overview

This project analyzes airline flight occupancy data to identify **low-performing flights** and uncover **capacity optimization opportunities** that can improve airline profitability.

Using **PostgreSQL** for data querying and **Python** for analysis and visualization, the project focuses on understanding how aircraft type, routes, and seat utilization impact overall flight performance.

The analysis is framed from a **business decision-making perspective**, addressing questions such as:
- Where is capacity being underutilized?
- Which aircraft types contribute most to low occupancy?
- Which routes consistently underperform?

---

## 🎯 Business Problem

Airlines operate with high fixed costs, making **seat occupancy** a critical driver of profitability.

Low-occupancy flights result in:
- Wasted fuel and crew costs  
- Inefficient aircraft allocation  
- Reduced operating margins  

**Objective:**  
Identify low-occupancy flights and structural patterns in aircraft usage and routes to support better scheduling, fleet assignment, and demand stimulation strategies.

---

## 🗂 Dataset Overview

- **Source:** Public airline booking dataset (PostgreSQL format)  
- **Database Size:** ~21 million records  

### Core Tables Used
- `flights`
- `seats`
- `ticket_flights`
- `aircrafts_data`
- `airports_data`

> Raw dataset files are intentionally **not included** in this repository due to size constraints.

---

## 🛠 Tools & Technologies

- **PostgreSQL** – relational database querying  
- **SQL** – joins, aggregations, CTEs  
- **Python** – data analysis and visualization  
- **Pandas** – data manipulation  
- **Matplotlib** – exploratory and analytical charts  
- **Git & GitHub** – version control and project management  

---

## ⭐ North Star Metric (NSM)

**Percentage of Flights Operating Above 50% Occupancy**

This metric represents the core business objective:
- Maximizing effective seat utilization across the airline network  
- All analyses aim to understand and improve this metric  

---

## 🔬 Methodology

### 1. Data Understanding & Validation
- Explored database schemas and table relationships  
- Verified seat capacity and booking consistency  
- Confirmed data completeness at the flight level  

### 2. Feature Construction
- Calculated seat capacity per aircraft  
- Aggregated booked seats per flight  
- Derived **flight-level occupancy rate**  

### 3. Exploratory Data Analysis (EDA)
- Distribution analysis of occupancy rates  
- Identification of low-occupancy thresholds  
- Aircraft-level and route-level performance comparison  

### 4. Advanced Analysis
- Pareto analysis to identify aircraft types contributing most to low occupancy  
- Box plots and histograms to analyze variability and skew  
- Route ranking to identify persistently underperforming segments  

### 5. Visualization & Reporting
- Decision-oriented charts  
- Focus on interpretability over decorative visuals  
- Insights communicated in business terms  

---

## 📊 Key Insights

- ~58% of flights operate below 50% occupancy, indicating widespread inefficiency  
- A small subset of aircraft types contributes disproportionately to low-occupancy flights  
- Certain routes consistently show very low or near-zero average occupancy  
- Larger aircraft types generally achieve higher utilization than smaller regional aircraft  

---

## 💡 Business Recommendations

- **Fleet Optimization:** Assign smaller aircraft to consistently low-demand routes  
- **Route Review:** Re-evaluate or consolidate routes with persistent low occupancy  
- **Scheduling Adjustments:** Reduce frequency or reschedule flights during low-demand periods  
- **Revenue Strategy Support:** Use occupancy patterns to guide pricing, promotions, and demand stimulation initiatives  

---

## 📈 Results & Impact

- Identified **124,000+ low-occupancy flights**  
- Quantified aircraft-level contribution to inefficiency  
- Highlighted routes with chronic underperformance  
- Provided a data-backed foundation for capacity optimization decisions  

---

## 🧠 Skills Demonstrated
 - SQL analytics on large-scale datasets
 - Translating operational data into business metrics
 - Analytical thinking focused on decision support
 - Clear technical documentation
 - End-to-end analytics workflow using Python and PostgreSQL

## 🧾 Summary & Insights

This project demonstrates how airline operational data can be transformed into actionable business insights. By focusing on seat occupancy as a profitability driver, the analysis identifies inefficiencies at the flight, aircraft, and route levels and provides data-backed recommendations for optimization.

The project reflects real-world analytics workflows while showcasing strong documentation and communication skills, making it suitable for both data analyst and technical writer roles.
