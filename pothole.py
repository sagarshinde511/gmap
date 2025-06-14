import streamlit as st
import pandas as pd
import mysql.connector
import folium
from streamlit_folium import st_folium

# Database Configuration
DB_CONFIG = {
    "host": "82.180.143.66",
    "user": "u263681140_students1",
    "password": "testStudents@123",
    "database": "u263681140_students1"
}

# Function to fetch data from MySQL
def fetch_pothole_data():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id, lat, lon FROM potholes")
        data = cursor.fetchall()

        df = pd.DataFrame(data)
        df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
        df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
        df.dropna(subset=["lat", "lon"], inplace=True)

        cursor.close()
        conn.close()
        return df
    except mysql.connector.Error as err:
        st.error(f"Database connection error: {err}")
        return pd.DataFrame()

# Title
st.title("Pothole Location Map Viewer")

# Load data only once using session_state
if "pothole_data" not in st.session_state:
    st.session_state["pothole_data"] = fetch_pothole_data()

df = st.session_state["pothole_data"]

# Optional: Refresh button
if st.button("Refresh Data"):
    st.session_state["pothole_data"] = fetch_pothole_data()
    df = st.session_state["pothole_data"]
    st.success("Data refreshed successfully!")

# Check if data exists
if not df.empty:
    # Create the map centered on mean coordinates
    m = folium.Map(location=[df["lat"].mean(), df["lon"].mean()], zoom_start=15, tiles="OpenStreetMap")

    for _, row in df.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=folium.Popup(f"Pothole ID: {row['id']}", max_width=250),
            tooltip=f"Pothole ID: {row['id']}",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)

    # Display the map
    st_folium(m, width=700, height=500)

    # Display table with only latitude and longitude
    st.write("### Pothole Coordinates")
    st.dataframe(df[["id", "lat", "lon"]])
else:
    st.warning("No pothole data found in the database.")
