from pandas import DataFrame
import streamlit as st
import pandas as pd
import plotly.express as px

def build_air_quality_tab(data: DataFrame):
    # Filter and clean temperature data
    temperature_data = data[data['Specie'] == "temperature"].copy()

    # Ensure 'median' is numeric and drop rows with NaN
    temperature_data['median'] = pd.to_numeric(temperature_data['median'], errors='coerce')
    temperature_data = temperature_data.dropna(subset=['median'])

    # Convert 'Date' column to datetime format if it exists
    if 'Date' in temperature_data.columns:
        temperature_data['Date'] = pd.to_datetime(temperature_data['Date'], errors='coerce')
        temperature_data = temperature_data.dropna(subset=['Date'])

    st.write("Cleaned temperature_data:", temperature_data.head())

    # Check if there is valid data to plot
    if not temperature_data.empty:
        st.subheader("Boxplot of Temperature for Different Cities")

        # Create a Plotly boxplot
        fig = px.box(
            temperature_data,
            x='City',
            y='median',
            color='City',
            title="Temperature Distribution by City",
            labels={
                "City": "City",
                "median": "Temperature (°C)"
            },
            template="plotly"
        )

        fig.update_layout(
            xaxis_title="City",
            yaxis_title="Temperature (°C)",
            xaxis_tickangle=45  # Rotate city labels
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig)
    else:
        st.write("No temperature data available for boxplot.")