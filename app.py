import streamlit as st
import requests
from datetime import datetime
import pydeck as pdk


# Title and description
st.title('NYC Taxi Fare Predictor')

st.markdown('''
Welcome! Enter your trip details below to estimate the taxi fare in New York City.
''')

st.markdown("## Enter ride parameters")

# User inputs
pickup_date = st.date_input("Pickup Date", value=datetime.now().date())
pickup_time = st.time_input("Pickup Time", value=datetime.now().time())
pickup_datetime = datetime.combine(pickup_date, pickup_time)
pickup_longitude = st.number_input("Pickup Longitude", value=-73.985428)
pickup_latitude = st.number_input("Pickup Latitude", value=40.748817)
dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.985428)
dropoff_latitude = st.number_input("Dropoff Latitude", value=40.748817)
passenger_count = st.number_input("Passenger Count", min_value=1, max_value=8, value=1)

# Convert datetime to string format expected by API
pickup_datetime_str = pickup_datetime.strftime("%Y-%m-%d %H:%M:%S")

# Build parameter dictionary
params = {
    "pickup_datetime": pickup_datetime_str,
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
}

# API URL
url = 'https://taxifare.lewagon.ai/predict'

# Make API request and display prediction
if st.button("Get Fare Prediction"):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        prediction = response.json()["fare"]
        st.success(f"Predicted Fare: ${prediction:.2f}")
    else:
        st.error("Error contacting the prediction API.")

# Create a DataFrame for the two points
import pandas as pd

map_data = pd.DataFrame([
    {"lat": pickup_latitude, "lon": pickup_longitude, "label": "Pickup"},
    {"lat": dropoff_latitude, "lon": dropoff_longitude, "label": "Dropoff"}
])

# Define map layer with color-coding
layer = pdk.Layer(
    "ScatterplotLayer",
    data=map_data,
    get_position='[lon, lat]',
    get_color=["label == 'Pickup' ? 0 : 255", 0, "label == 'Pickup' ? 255 : 0"],  # Blue for pickup, red for dropoff
    get_radius=100,
)

# Display the map
st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/streets-v11",
    initial_view_state=pdk.ViewState(
        latitude=(pickup_latitude + dropoff_latitude) / 2,
        longitude=(pickup_longitude + dropoff_longitude) / 2,
        zoom=11,
        pitch=0,
    ),
    layers=[layer],
))
# import streamlit as st
# import requests
# from datetime import datetime

# # Title and description
# st.title('NYC Taxi Fare Predictor')

# st.markdown('''
# Enter your trip details below to estimate the fare for a New York City taxi ride.
# ''')

# # === User inputs ===
# st.subheader("Trip Details")

# # Free-form datetime input
# pickup_datetime_input = st.text_input(
#     "Pickup Date & Time (format: YYYY-MM-DD HH:MM:SS)",
#     value=(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
# )

# # Coordinates and passenger count
# pickup_longitude = st.number_input("Pickup Longitude", value=-73.985428)
# pickup_latitude = st.number_input("Pickup Latitude", value=40.748817)
# dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.985428)
# dropoff_latitude = st.number_input("Dropoff Latitude", value=40.748817)
# passenger_count = st.number_input("Passenger Count", min_value=1, max_value=8, value=1)

# # === API call ===
# params = {
#     "pickup_datetime": pickup_datetime_input,
#     "pickup_longitude": pickup_longitude,
#     "pickup_latitude": pickup_latitude,
#     "dropoff_longitude": dropoff_longitude,
#     "dropoff_latitude": dropoff_latitude,
#     "passenger_count": int(passenger_count)
# }

# api_url = 'https://taxifare.lewagon.ai/predict'

# if st.button("Get Fare Estimate"):
#     try:
#         # Basic validation
#         _ = datetime.strptime(pickup_datetime_input, "%Y-%m-%d %H:%M:%S")
#         response = requests.get(api_url, params=params)
#         response.raise_for_status()
#         prediction = response.json().get("fare", "No fare returned")
#         st.success(f"Estimated Fare: ${prediction:.2f}")
#     except ValueError:
#         st.error("Invalid datetime format. Please use YYYY-MM-DD HH:MM:SS.")
#     except Exception as e:
#         st.error(f"Failed to get prediction. Error: {e}")
