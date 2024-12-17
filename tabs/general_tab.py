from pandas import DataFrame
import streamlit as st
import pandas as pd
import plotly.express as px

def build_general_tab(data: DataFrame):
    # Filter and clean temperature data
    temperature_data = data[data['Specie'] == "temperature"].copy()
    temperature_data['median'] = pd.to_numeric(temperature_data['median'], errors='coerce')
    temperature_data = temperature_data.dropna(subset=['median']).reset_index(drop=True)

    st.write("Cleaned temperature_data:", temperature_data.head())

    if not temperature_data.empty:
        # Multiselect for cities
        selected_cities = st.multiselect(
            "Select Cities",
            temperature_data['City'].unique(),
            default=temperature_data['City'].unique()
        )

        # Filter temperature data based on selected cities
        filtered_temperature_data = temperature_data[temperature_data['City'].isin(selected_cities)]

        if not filtered_temperature_data.empty:
            st.subheader("Boxplot of Temperature for Selected Cities")

            # Create a Plotly boxplot for temperature
            fig_temp = px.box(
                filtered_temperature_data,
                x='City',
                y='median',
                color='City',
                title="Temperature Distribution by City",
                labels={
                    "City": "City",
                    "median": "Temperature (°C)"
                },
                template="plotly",
                boxmode='group'
            )

            fig_temp.update_layout(
                xaxis_title="City",
                yaxis_title="Temperature (°C)",
                xaxis_tickangle=45  # Rotate city labels
            )

            st.plotly_chart(fig_temp)
        else:
            st.write("No temperature data available for the selected cities.")

        # Filter and clean PM10 data based on selected cities
        filtered_pm10_data = data[(data['Specie'] == "pm10") & (data['City'].isin(selected_cities))].copy()
        filtered_pm10_data['median'] = pd.to_numeric(filtered_pm10_data['median'], errors='coerce')
        filtered_pm10_data = filtered_pm10_data.dropna(subset=['median']).reset_index(drop=True)

        st.write("Cleaned filtered_pm10_data:", filtered_pm10_data.head())

        if not filtered_pm10_data.empty:
            st.subheader("Boxplot of PM10 for Selected Cities")

            # Create a Plotly boxplot for PM10
            fig_pm10 = px.box(
                filtered_pm10_data,
                x='City',
                y='median',
                color='City',
                title="PM10 Distribution by City",
                labels={
                    "City": "City",
                    "median": "PM10"
                },
                template="plotly",
                boxmode='group'
            )

            fig_pm10.update_layout(
                xaxis_title="City",
                yaxis_title="PM10",
                xaxis_tickangle=45  # Rotate city labels
            )

            st.plotly_chart(fig_pm10)
        else:
            st.write("No PM10 data available for the selected cities.")
    else:
        st.write("No temperature data available for plotting.")