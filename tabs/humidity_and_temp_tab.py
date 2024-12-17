from pandas import DataFrame
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def build_humidity_and_temp_tab(data: DataFrame, selected_city):
    # Filter and clean temperature data
    temperature_data = data[(data["City"] == selected_city) & (data["Specie"] == "temperature")].copy()
    temperature_data['median'] = pd.to_numeric(temperature_data['median'], errors='coerce')
    temperature_data = temperature_data.dropna(subset=['median']).reset_index(drop=True)

    # Filter and clean humidity data
    humidity_data = data[(data["City"] == selected_city) & (data["Specie"] == "humidity")].copy()
    humidity_data['median'] = pd.to_numeric(humidity_data['median'], errors='coerce')
    humidity_data = humidity_data.dropna(subset=['median']).reset_index(drop=True)

    # Filter and clean PM10 data
    pm10_data = data[(data["City"] == selected_city) & (data["Specie"] == "pm10")].copy()
    pm10_data['median'] = pd.to_numeric(pm10_data['median'], errors='coerce')
    pm10_data = pm10_data.dropna(subset=['median']).reset_index(drop=True)

    # Filter and clean PM25 data
    pm25_data = data[(data["City"] == selected_city) & (data["Specie"] == "pm25")].copy()
    pm25_data['median'] = pd.to_numeric(pm25_data['median'], errors='coerce')
    pm25_data = pm25_data.dropna(subset=['median']).reset_index(drop=True)

    # Create columns
    col1, col2 = st.columns(2)

    # Handle and plot temperature data
    if not temperature_data.empty:
        col2.subheader(f"Monthly Temperature in {selected_city}")

        # Convert 'Date' to datetime and drop invalid rows
        if 'Date' in temperature_data.columns:
            temperature_data['Date'] = pd.to_datetime(temperature_data['Date'], errors='coerce')
            temperature_data = temperature_data.dropna(subset=['Date'])
            temperature_data['Month'] = temperature_data['Date'].dt.month_name()

            # Group by month
            monthly_temp = temperature_data.groupby('Month')['median'].mean()

            # Ensure months appear in correct order
            months_order = ["January", "February", "March", "April", "May", "June",
                            "July", "August", "September", "October", "November", "December"]
            monthly_temp = monthly_temp.reindex(months_order, axis=0).dropna()

            # Create and display the bar plot
            fig_temp = px.bar(
                x=monthly_temp.index,
                y=monthly_temp.values,
                labels={"x": "Month", "y": "Average Temperature (°C)"},
                title="Average Monthly Temperature",
                color_discrete_sequence=["orange"]
            )

            fig_temp.update_layout(xaxis_title="Month", yaxis_title="Average Temperature (°C)")

            col2.plotly_chart(fig_temp)
        else:
            col2.write("No valid 'Date' column available in temperature data.")
    else:
        col2.write("No temperature data available for the selected city.")

    # Handle and plot humidity data
    if not humidity_data.empty:
        col1.subheader(f"Monthly Humidity in {selected_city}")

        # Convert 'Date' to datetime and drop invalid rows
        if 'Date' in humidity_data.columns:
            humidity_data['Date'] = pd.to_datetime(humidity_data['Date'], errors='coerce')
            humidity_data = humidity_data.dropna(subset=['Date'])
            humidity_data['Month'] = humidity_data['Date'].dt.month_name()

            # Group by month
            monthly_humi = humidity_data.groupby('Month')['median'].mean()

            # Ensure months appear in correct order
            monthly_humi = monthly_humi.reindex(months_order, axis=0).dropna()

            # Create and display the bar plot
            fig_humi = px.bar(
                x=monthly_humi.index,
                y=monthly_humi.values,
                labels={"x": "Month", "y": "Average Humidity"},
                title="Average Monthly Humidity",
                color_discrete_sequence=["blue"]
            )

            fig_humi.update_layout(xaxis_title="Month", yaxis_title="Average Humidity")

            col1.plotly_chart(fig_humi)
        else:
            col1.write("No valid 'Date' column available in humidity data.")
    else:
        col1.write("No humidity data available for the selected city.")

    # Handle scatter plot of temperature vs PM10
    if not temperature_data.empty and not pm10_data.empty:
        temperature_data['Date'] = pd.to_datetime(temperature_data['Date'], errors='coerce')
        pm10_data['Date'] = pd.to_datetime(pm10_data['Date'], errors='coerce')

        temperature_data = temperature_data.dropna(subset=['Date', 'median']).rename(columns={'median': 'Temperature'})
        pm10_data = pm10_data.dropna(subset=['Date', 'median']).rename(columns={'median': 'PM10'})

        combined_data = pd.merge(temperature_data, pm10_data, on='Date', how='inner')

        if not combined_data.empty:
            col2.subheader(f"Scatter Plot of Temperature vs PM10 in {selected_city} with Regression Line")

            fig_temp_pm10 = px.scatter(
                combined_data,
                x="Temperature",
                y="PM10",
                trendline="ols",
                labels={"Temperature": "Temperature (°C)", "PM10": "PM10 (µg/m³)"},
                title="Temperature vs PM10 with Regression Line",
                color_discrete_sequence=["red"]
            )

            col2.plotly_chart(fig_temp_pm10)
        else:
            col2.write("No matching data available for scatter plot after merging.")

    # Handle scatter plot of temperature vs PM25
    if not data.empty:
        temp_data_pm25 = data[(data["City"] == selected_city) & (data["Specie"] == "temperature")].copy()
        pm25_data = data[(data["City"] == selected_city) & (data["Specie"] == "pm25")].copy()

        temp_data_pm25['Date'] = pd.to_datetime(temp_data_pm25['Date'], errors='coerce')
        pm25_data['Date'] = pd.to_datetime(pm25_data['Date'], errors='coerce')

        temp_data_pm25 = temp_data_pm25.dropna(subset=['Date', 'median']).rename(columns={'median': 'Temperature'})
        pm25_data = pm25_data.dropna(subset=['Date', 'median']).rename(columns={'median': 'PM25'})

        combined_data = pd.merge(temp_data_pm25, pm25_data, on='Date', how='inner')

        if not combined_data.empty:
            col1.subheader(f"Scatter Plot of Temperature vs PM25 in {selected_city} with Regression Line")

            fig_temp_pm25 = px.scatter(
                combined_data,
                x="Temperature",
                y="PM25",
                trendline="ols",
                labels={"Temperature": "Temperature (°C)", "PM25": "PM25 (µg/m³)"},
                title="Temperature vs PM25 with Regression Line",
                color_discrete_sequence=["green"]
            )

            col1.plotly_chart(fig_temp_pm25)
        else:
            col1.write("No matching data available for the scatter plot after merging.")
    else:
        col1.write("Insufficient data for temperature and PM25 to create scatter plot.")