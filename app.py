import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.title("🚕 Taxi Fare Predictor")

st.markdown('''
Welcome to the **Taxi Fare Predictor**!
Fill out the ride details below to get a fare estimate.
''')

# 1. User inputs
pickup_date = st.date_input("Pickup Date", datetime(2013, 7, 6).date())
pickup_time = st.time_input("Pickup Time", datetime(2013, 7, 6, 17, 18).time())
pickup_datetime = datetime.combine(pickup_date, pickup_time)
pickup_longitude = st.number_input("Pickup Longitude", value=-73.985428)
pickup_latitude = st.number_input("Pickup Latitude", value=40.748817)
dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.985428)
dropoff_latitude = st.number_input("Dropoff Latitude", value=40.712776)
passenger_count = st.slider("Passenger Count", min_value=1, max_value=8, value=1)

# 2. API URL
url = 'https://taxifare.lewagon.ai/predict'  # Replace with your API if available


# 4. Submit button
if st.button("Predict Fare"):
    params = {
        "pickup_datetime": pickup_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": passenger_count
    }

    # 5. Make the API call
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # raise error for bad status codes
        prediction = response.json().get("fare", None)

        if prediction is not None:
            st.success(f"💰 Estimated fare: **${prediction:.2f}**")
        else:
            st.warning("The API did not return a fare.")

    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")

# 6. Map visualization
st.subheader("Ride Path 🗺")
map_data = pd.DataFrame({
    'lat': [pickup_latitude, dropoff_latitude],
    'lon': [pickup_longitude, dropoff_longitude]
})
st.map(map_data)
