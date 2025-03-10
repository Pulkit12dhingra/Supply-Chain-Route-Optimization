import pandas as pd
import numpy as np
import random
import openrouteservice
import time

# Initialize OpenRouteService client (Replace 'YOUR_API_KEY' with a valid key)
API_KEY = "<>"
client = openrouteservice.Client(key=API_KEY)

# Function to get real-time distance between cities with API rate limiting
def get_distance_time(origin, destination, mode):
    try:
        coords = [(origin[1], origin[0]), (destination[1], destination[0])]
        route = client.directions(coords, profile=mode, format="geojson")
        distance_km = route['features'][0]['properties']['segments'][0]['distance'] / 1000  # Convert meters to km
        duration_hours = route['features'][0]['properties']['segments'][0]['duration'] / 3600  # Convert seconds to hours
        time.sleep(1.5)  # Sleep to avoid exceeding API quota
        return round(distance_km, 2), round(duration_hours, 2)
    except:
        return None, None

# Define sample UK cities with approximate latitude & longitude
uk_cities = {
    "London": (51.5074, -0.1278), "Manchester": (53.4808, -2.2426), "Birmingham": (52.4862, -1.8904),
    "Liverpool": (53.4084, -2.9916), "Edinburgh": (55.9533, -3.1883), "Glasgow": (55.8642, -4.2518),
    "Bristol": (51.4545, -2.5879), "Leeds": (53.8008, -1.5491), "Sheffield": (53.3811, -1.4701), "Newcastle": (54.9783, -1.6174)
}

# Generate shipment data
num_shipments = 50
shipments = []
for _ in range(num_shipments):
    origin, destination = random.sample(list(uk_cities.keys()), 2)
    priority = random.choice([6, 12, 24, 48])  # Delivery time in hours
    fragile = random.choice([True, False])
    distance, duration = get_distance_time(uk_cities[origin], uk_cities[destination], "driving-car")
    if distance is None:
        continue  # Skip if API fails to return distance

    shipments.append([f"PN{random.randint(1000, 9999)}", origin, destination, priority, fragile, distance, duration, 
                      uk_cities[origin][0], uk_cities[origin][1], uk_cities[destination][0], uk_cities[destination][1]])

# Create DataFrame for shipment data
shipments_df = pd.DataFrame(shipments, columns=["Product_Number", "Origin_City", "Destination_City", "Priority_Hours", "Fragile", "Distance_KM", "Estimated_Time_Hours", "Origin_City_Lat", "Origin_City_Lon", "Destination_City_Lat", "Destination_City_Lon"])

# Define transport cost table (Fuel cost + transport charge per KM)
transport_modes = {
    "Land": {"Cost_per_KM": 0.5, "Fragile_Security": "Likely to break", "Speed_KM_H": 90},
    "Airplane": {"Cost_per_KM": 2.0, "Fragile_Security": "More secure", "Speed_KM_H": 800},
    "Train": {"Cost_per_KM": 0.8, "Fragile_Security": "Least secure", "Speed_KM_H": 150}
}

# Generate cost estimations
cost_data = []
for _, row in shipments_df.iterrows():
    for mode, values in transport_modes.items():
        cost = row["Distance_KM"] * values["Cost_per_KM"]
        time = row["Distance_KM"] / values["Speed_KM_H"]
        if row["Fragile"] and values["Fragile_Security"] == "Likely to break":
            cost *= 1.2  # 20% penalty
        if row["Fragile"] and values["Fragile_Security"] == "Least secure":
            cost *= 1.1  # 10% penalty
        cost_data.append([row["Product_Number"], row["Origin_City"], row["Destination_City"], mode, round(cost, 2), round(time, 2), row["Origin_City_Lat"], row["Origin_City_Lon"], row["Destination_City_Lat"], row["Destination_City_Lon"]])

# Create DataFrame for cost estimations
estimations_df = pd.DataFrame(cost_data, columns=["Product_Number", "Origin_City", "Destination_City", "Transport_Mode", "Total_Cost (£)", "Total_Time (Hours)", "Origin_City_Lat", "Origin_City_Lon", "Destination_City_Lat", "Destination_City_Lon"])

# Save data to CSV
shipments_df.to_csv("shipments.csv", index=False)
estimations_df.to_csv("estimations.csv", index=False)

print("Data generation completed. CSV files saved.")
