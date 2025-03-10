# Re-initialize the dataset after execution state reset

import pandas as pd
import random

# Define sample UK cities for transport routes
uk_cities = ["London", "Manchester", "Birmingham", "Liverpool", "Edinburgh", "Glasgow", "Bristol", "Leeds", "Sheffield", "Newcastle"]

# Generate random shipment data
num_shipments = 50
shipments = []
for _ in range(num_shipments):
    origin, destination = random.sample(uk_cities, 2)
    priority = random.choice([6, 12, 24, 48])  # Delivery time in hours
    fragile = random.choice([True, False])
    distance = random.randint(100, 600)  # Distance in KM

    shipments.append([f"PN{random.randint(1000, 9999)}", origin, destination, priority, fragile, distance])

# Create DataFrame for shipment data
shipments_df = pd.DataFrame(shipments, columns=["Product_Number", "Origin_City", "Destination_City", "Priority_Hours", "Fragile", "Distance_KM"])

# Define transport cost table (Fuel cost + transport charge per KM)
transport_modes = {
    "Land": {"Cost_per_KM": 0.5, "Fragile_Security": "Likely to break", "Time_per_KM": 1.2},
    "Airplane": {"Cost_per_KM": 2.0, "Fragile_Security": "More secure", "Time_per_KM": 0.5},
    "Train": {"Cost_per_KM": 0.8, "Fragile_Security": "Least secure", "Time_per_KM": 1.0}
}

# Create DataFrame for transport costs
cost_data = []
for mode, values in transport_modes.items():
    cost_data.append([mode, values["Cost_per_KM"], values["Fragile_Security"], values["Time_per_KM"]])

cost_df = pd.DataFrame(cost_data, columns=["Route", "Cost_per_KM", "Fragile_Security", "Time_per_KM"])

# Function to estimate cost and time for each transport mode
def estimate_cost_time(row):
    distance = row["Distance_KM"]
    fragile = row["Fragile"]
    priority = row["Priority_Hours"]
    
    estimates = []
    
    for _, mode in cost_df.iterrows():
        route_type = mode["Route"]
        cost_per_km = mode["Cost_per_KM"]
        time_per_km = mode["Time_per_KM"]
        fragile_security = mode["Fragile_Security"]
        
        # Calculate total cost
        total_cost = distance * cost_per_km
        
        # Calculate total time
        total_time = distance * time_per_km
        
        # Apply penalty for fragile items if using insecure transport
        if fragile and fragile_security == "Likely to break":
            total_cost *= 1.2  # Adding a 20% penalty
        
        if fragile and fragile_security == "Least secure":
            total_cost *= 1.1  # Adding a 10% penalty
        
        # Store results
        estimates.append({
            "Product_Number": row["Product_Number"],
            "Origin_City": row["Origin_City"],
            "Destination_City": row["Destination_City"],
            "Transport_Mode": route_type,
            "Total_Cost (£)": round(total_cost, 2),
            "Total_Time (Hours)": round(total_time, 2),
            "Meets_Priority": total_time <= priority
        })
    
    return estimates

# Apply cost estimation for each shipment
all_estimations = []
for _, shipment in shipments_df.iterrows():
    all_estimations.extend(estimate_cost_time(shipment))

# Convert to DataFrame
estimations_df = pd.DataFrame(all_estimations)

# Function to select the best transport mode based on user's preference
def select_best_route(preference):
    selected_routes = []

    for product_number in estimations_df["Product_Number"].unique():
        product_data = estimations_df[estimations_df["Product_Number"] == product_number]

        if preference == "Fastest":
            # Choose the mode with the least time
            best_option = product_data.nsmallest(1, "Total_Time (Hours)")

        elif preference == "Safest":
            # Choose the mode that is safest for fragile items
            best_option = product_data.copy()
            best_option["Safety_Score"] = best_option["Transport_Mode"].map(
                {"Land": 1, "Train": 2, "Airplane": 3})  # Higher score = safer
            best_option = best_option.nlargest(1, "Safety_Score")

        elif preference == "Balanced":
            # Choose a mode that balances cost and time (Weighted Average)
            best_option = product_data.copy()
            best_option["Balance_Score"] = (
                (1 / (best_option["Total_Time (Hours)"] + 1)) * 0.5 +
                (1 / (best_option["Total_Cost (£)"] + 1)) * 0.5
            )
            best_option = best_option.nlargest(1, "Balance_Score")

        else:
            continue

        selected_routes.append(best_option.iloc[0])

    return pd.DataFrame(selected_routes)

# Generate best route recommendations for each user preference
fastest_routes = select_best_route("Fastest")
safest_routes = select_best_route("Safest")
balanced_routes = select_best_route("Balanced")

estimations_df.to_csv("data/estimations.csv", index=False)
