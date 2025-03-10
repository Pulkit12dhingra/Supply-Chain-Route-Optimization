import streamlit as st
import pandas as pd
import openrouteservice
import pydeck as pdk

# Initialize OpenRouteService client (Replace 'YOUR_API_KEY' with a valid key)
API_KEY = "<>"
client = openrouteservice.Client(key=API_KEY)

# Load datasets (assuming they are generated as in previous steps)
def load_data():
    shipments_df = pd.read_csv("shipments.csv")
    estimations_df = pd.read_csv("estimations.csv")
    return shipments_df, estimations_df

# Streamlit UI
def main():
    st.title("Supply Chain Route Optimizer")
    
    shipments_df, estimations_df = load_data()
    
    st.sidebar.header("User Preferences")
    
    # User input for selecting Product Number (Mandatory Dropdown)
    product_number = st.sidebar.selectbox("Select Product Number:", [None] + list(estimations_df["Product_Number"].unique()))
    
    if product_number:
        filtered_data = estimations_df[(estimations_df["Product_Number"] == product_number)]
        
        # Get origin city filter    
        origin_city_list = filtered_data["Origin_City"].unique()
        origin_city_filter = st.sidebar.selectbox("Select Origin City", [None] + list(origin_city_list))

        # Get destination city filter    
        destination_city_list = filtered_data["Destination_City"].unique()
        destination_city_filter = st.sidebar.selectbox("Select Destination City", [None] + list(destination_city_list))

        preference = st.sidebar.radio("Select Optimization Preference:", ["Fastest", "Safest", "Balanced"])
        
        if st.sidebar.button("Get Best Routes"):
            best_routes = select_best_route(preference, filtered_data, origin_city_filter, destination_city_filter)
            st.write(f"### Optimal Routes for Product {product_number} Based on {preference} Preference")
            st.dataframe(best_routes)
            
            # Show map only when both origin and destination cities are selected
            if origin_city_filter and destination_city_filter:
                origin_coords = filtered_data.iloc[0][['Origin_City_Lat', 'Origin_City_Lon']].values.tolist()
                destination_coords = filtered_data.iloc[0][['Destination_City_Lat', 'Destination_City_Lon']].values.tolist()
                
                # Create map with large markers and a dotted line route
                view_state = pdk.ViewState(
                    latitude=origin_coords[0],
                    longitude=origin_coords[1],
                    zoom=5,
                    pitch=0
                )
                
                layers = [
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=pd.DataFrame(
                            [[origin_coords[0], origin_coords[1]], [destination_coords[0], destination_coords[1]]],
                            columns=["lat", "lon"]
                        ),
                        get_position="[lon, lat]",
                        get_color="[255, 0, 0, 160]",
                        get_radius=30000,
                    ),
                    pdk.Layer(
                        "ArcLayer",
                        data=pd.DataFrame(
                            {
                                "start": [[origin_coords[1], origin_coords[0]]],
                                "end": [[destination_coords[1], destination_coords[0]]]
                            }
                        ),
                        get_source_position="start",
                        get_target_position="end",
                        get_width=3,
                        get_tilt=10,
                        get_source_color="[0, 255, 0]",
                        get_target_color="[0, 0, 255]",
                    )
                ]
                
                st.pydeck_chart(pdk.Deck(
                    map_style='mapbox://styles/mapbox/light-v9',
                    initial_view_state=view_state,
                    layers=layers
                ))

# Function to select the best transport mode based on user's preference
def select_best_route(preference, filtered_data, origin_city_filter, destination_city_filter):
    selected_routes = []
    if origin_city_filter is not None:
        filtered_data = filtered_data[(filtered_data["Origin_City"] == origin_city_filter)]
    else:    
        st.write("### You need to select Origin City")

    if destination_city_filter is not None:
        filtered_data = filtered_data[(filtered_data["Destination_City"] == destination_city_filter)]
    else:    
        st.write("### You need to select Destination City")

    for product_number in filtered_data["Product_Number"].unique():
        if origin_city_filter is None or destination_city_filter is None:
            return pd.DataFrame(filtered_data)

        product_data = filtered_data[filtered_data["Product_Number"] == product_number]
        if preference == "Fastest":
            best_option = product_data[(product_data.Transport_Mode == "Airplane")]
        elif preference == "Safest":
            best_option = product_data[(product_data.Transport_Mode == "Land")]
        elif preference == "Balanced":
            best_option = product_data[(product_data.Transport_Mode == "Train")]
        else:
            continue
        selected_routes.append(best_option.iloc[0])

    return pd.DataFrame(selected_routes)

if __name__ == "__main__":
    main()