import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Create sample data with latitude, longitude, and labels
data = pd.DataFrame({
    'name': ['Pothole 1', 'Pothole 2'],
    'lat': [17.2987556, 17.29085],
    'lon': [74.1900642, 74.1842447]
})

# Initialize a Folium map
m = folium.Map(location=[17.2948, 74.1872], zoom_start=15, tiles="OpenStreetMap")

# Add markers with popups and tooltips
for index, row in data.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=folium.Popup(row['name'], max_width=250),  # Popup text
        tooltip=row['name'],  # Tooltip text
        icon=folium.Icon(color="red", icon="info-sign")  # Explicit marker icon
    ).add_to(m)

# Display map in Streamlit
st_folium(m, width=700, height=500)
