from pandas import DataFrame
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def build_humidity_and_temp_tab(data: DataFrame):
    # Streamlit App
    st.title("Romania air quality")

    # Sidebar for user inputs
    st.sidebar.header("Filters")

    romania_data = data[(data["Country"] == "RO")]
    selected_city = st.sidebar.selectbox("Select a City:", romania_data["City"].unique())
    temperature_data = data[(data["City"] == selected_city) & (data["Specie"] == "temperature")]
    humidity_data = data[(data["City"] == selected_city) & (data["Specie"] == "humidity")]
    pm10_data = data[(data["City"] == selected_city) & (data["Specie"] == "pm10")]
    pm25_data = data[(data["City"] == selected_city) & (data["Specie"] == "pm25")]

    col1, col2 = st.columns(2)

    # Create and display bar plot for temperature
    if not temperature_data.empty:
        col2.subheader(f"Monthly Temperature in {selected_city}")
        temperature_data['Date'] = pd.to_datetime(temperature_data['Date'])
        temperature_data['Month'] = temperature_data['Date'].dt.month_name()

        monthly_temp = temperature_data.groupby('Month')['median'].mean()

        months_order = ["January", "February", "March", "April", "May", "June", 
                        "July", "August", "September", "October", "November", "December"]
        monthly_temp = monthly_temp.reindex(months_order, axis=0).dropna()

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
        col2.write("No temperature data available for the selected city.")

    if not humidity_data.empty:
        col1.subheader(f"Monthly Humidity in {selected_city}")

        humidity_data['Date'] = pd.to_datetime(humidity_data['Date'])
        humidity_data['Month'] = humidity_data['Date'].dt.month_name()

        monthly_humi = humidity_data.groupby('Month')['median'].mean()

        monthly_humi = monthly_humi.reindex(months_order, axis=0).dropna()

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
        col1.write("No humidity data available for the selected city.")

    # Merge temperature and PM10 data on Date to prepare for plotting
    if not temperature_data.empty and not pm10_data.empty:
        temperature_data['Date'] = pd.to_datetime(temperature_data['Date'])
        pm10_data['Date'] = pd.to_datetime(pm10_data['Date'])

        temperature_data = temperature_data[['Date', 'median']].rename(columns={'median': 'Temperature'})
        pm10_data = pm10_data[['Date', 'median']].rename(columns={'median': 'PM10'})

        combined_data = pd.merge(temperature_data, pm10_data, on='Date', how='inner')

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
        col2.write("Insufficient data for temperature and PM10 to create scatter plot.")

    if not temperature_data.empty and not pm25_data.empty:
        temperature_data['Date'] = pd.to_datetime(temperature_data['Date'])
        pm25_data['Date'] = pd.to_datetime(pm25_data['Date'])

        temperature_data = temperature_data[['Date', 'median']].rename(columns={'median': 'Temperature'})
        pm25_data = pm25_data[['Date', 'median']].rename(columns={'median': 'PM25'})

        combined_data = pd.merge(temperature_data, pm25_data, on='Date', how='inner')

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
        col1.write("Insufficient data for temperature and PM25 to create scatter plot.")