from pandas import DataFrame
import streamlit as st
import pandas as pd
import plotly.express as px

def build_air_quality_tab(data: DataFrame):
    # Filter temperature data
    temperature_data = data[data['Specie'] == "temperature"]

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