Live Link to the application:- https://supply-chain-route-optimizationgit-deczcocnuhvdvpjkmpetxw.streamlit.app
# Route Optimization

This project aims to optimize routes and estimate costs for transporting cargo between various cities in the UK. It evaluates different modes of transport (Train, Airplane, and Truck) to determine the best route based on user preferences such as speed, safety, and cost.

## Project Structure

```
/Route Optimization
│
├── data/
│   ├── transport_costs.csv
│   ├── shipments.csv
│   └── estimations.csv
│
├── generate_Data.py
├── logic.py
└── UI.py
```

## Files

### logic.py
Contains the core logic for generating shipment data, estimating costs and times for different transport modes, and selecting the best routes based on user preferences.

### UI.py
Provides a Streamlit-based user interface for interacting with the route optimization logic. Users can select product numbers, origin and destination cities, and optimization preferences to get the best routes.

### generate_Data.py
Generates shipment data using real-time distance and duration information from the OpenRouteService API. Saves the generated data to CSV files for use in the logic and UI components.

### data/transport_costs.csv
Contains the transport cost table with details on cost per KM, fragile security, and time per KM for different transport modes.

### data/shipments.csv
Contains the generated shipment data with details on product number, origin and destination cities, priority hours, fragile status, distance, estimated time, and coordinates.

### data/estimations.csv
Contains the cost and time estimations for each shipment and transport mode, including details on product number, origin and destination cities, transport mode, total cost, total time, and coordinates.

## Setup

1. Install the required Python packages:
    ```sh
    pip install pandas streamlit openrouteservice pydeck
    ```

2. Replace the placeholder API key in `generate_Data.py` and `UI.py` with a valid OpenRouteService API key.

3. Run `generate_Data.py` to generate the shipment data and cost estimations:
    ```sh
    python generate_Data.py
    ```

4. Run `UI.py` to start the Streamlit application:
    ```sh
    streamlit run UI.py
    ```

## Getting an OpenRouteService API Token

1. Go to [OpenRouteService API](https://openrouteservice.org/dev/#/api-docs?loginSuccessful=true).
2. Sign up or log in to your account.
3. Navigate to the "API Keys" section.
4. Click on "New API Key" and follow the instructions to generate a new API key.
5. Copy the generated API key and replace the placeholder in `generate_Data.py` and `UI.py`.

## Usage

1. Open the Streamlit application in your browser.
2. Select a product number from the dropdown menu.
3. Select the origin and destination cities.
4. Choose an optimization preference (Fastest, Safest, Balanced).
5. Click "Get Best Routes" to see the optimal routes based on your preference.
6. If both origin and destination cities are selected, a map will be displayed showing the route.

## Data

### Sample Transport Costs
```plaintext
Route,Cost_per_KM,Fragile_Security,Time_per_KM
Land,0.5,Likely to break,1.2
Airplane,2.0,More secure,0.5
Train,0.8,Least secure,1.0
```

### Sample Shipments
```plaintext
Product_Number,Origin_City,Destination_City,Priority_Hours,Fragile,Distance_KM,Estimated_Time_Hours,Origin_City_Lat,Origin_City_Lon,Destination_City_Lat,Destination_City_Lon
PN5283,Newcastle,Glasgow,12,False,244.1,2.72,54.9783,-1.6174,55.8642,-4.2518
PN5479,Edinburgh,Bristol,12,False,599.28,6.48,55.9533,-3.1883,51.4545,-2.5879
PN4353,Sheffield,Manchester,24,False,61.03,1.25,53.3811,-1.4701,53.4808,-2.2426
...
```

### Sample Estimations
```plaintext
Product_Number,Origin_City,Destination_City,Transport_Mode,Total_Cost (£),Total_Time (Hours),Origin_City_Lat,Origin_City_Lon,Destination_City_Lat,Destination_City_Lon
PN5283,Newcastle,Glasgow,Land,122.05,2.71,54.9783,-1.6174,55.8642,-4.2518
PN5283,Newcastle,Glasgow,Airplane,488.2,0.31,54.9783,-1.6174,55.8642,-4.2518
PN5283,Newcastle,Glasgow,Train,195.28,1.63,54.9783,-1.6174,55.8642,-4.2518
...
```

