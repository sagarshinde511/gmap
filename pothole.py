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
        # Connect to MySQL database
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        
        # Fetch pothole data
        cursor.execute("SELECT id, lat, lon FROM potholes")
        data = cursor.fetchall()
        
        # Convert data to DataFrame
        df = pd.DataFrame(data)
        
        # Ensure lat and lon are numeric
        df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
        df["lon"] = pd.to_numeric(df["lon"], errors="coerce")

        # Drop rows where lat/lon conversion failed
        df.dropna(subset=["lat", "lon"], inplace=True)

        # Close connection
        cursor.close()
        conn.close()
        
        return df
    except mysql.connector.Error as err:
        st.error(f"Database connection error: {err}")
        return pd.DataFrame()  # Return an empty DataFrame on error

# Fetch data
df = fetch_pothole_data()

# Check if data is available
if not df.empty:
    # Initialize a Folium map, centering it on the data
    m = folium.Map(location=[df["lat"].mean(), df["lon"].mean()], zoom_start=15, tiles="OpenStreetMap")

    # Add markers for each pothole
    for index, row in df.iterrows():
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=folium.Popup(f"Pothole ID: {row['id']}", max_width=250),
            tooltip=f"Pothole ID: {row['id']}",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)

    # Display the map in Streamlit
    st_folium(m, width=700, height=500)

    # Display data table for reference
    st.write("### Pothole Data")
    st.dataframe(df)
else:
    st.warning("No pothole data found in the database.")
