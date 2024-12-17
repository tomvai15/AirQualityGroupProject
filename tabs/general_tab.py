from pandas import DataFrame
import streamlit as st
import pandas as pd
import plotly.express as px

def build_api_boxplot(data: DataFrame, selected_cities):
    romania_data = data.copy()

    # Convert 'Date' column to datetime format and drop invalid dates
    romania_data['Date'] = pd.to_datetime(romania_data['Date'], errors='coerce')
    romania_data = romania_data.dropna(subset=['Date'])

    # Extract 'Month' in "YYYY-MM" format
    romania_data['Month'] = romania_data['Date'].dt.to_period('M').astype(str)

    # List of required pollutants for API calculation
    required_pollutants = ['pm10', 'pm25', 'no2', 'o3', 'so2', 'co']

    # Filter data to include only rows for the required pollutants
    api_data = romania_data[romania_data['Specie'].str.lower().isin(required_pollutants)].copy()

    # Pivot the data so pollutants become columns
    pivot_data = api_data.pivot_table(
        index=['City', 'Month'],
        columns='Specie',
        values='median',
        aggfunc='max'
    ).reset_index()

    # Clean up column names
    pivot_data.columns.name = None
    pivot_data.columns = [col.lower() if isinstance(col, str) else col for col in pivot_data.columns]

    # Dynamically calculate API as the maximum value across the available pollutants
    available_pollutants = [col for col in required_pollutants if col in pivot_data.columns]
    if available_pollutants:
        pivot_data['api'] = pivot_data[available_pollutants].max(axis=1, skipna=True)
    else:
        st.write("No pollutants available for API calculation.")
        pivot_data['api'] = None

    # Filter the data based on selected cities
    filtered_data = pivot_data[pivot_data['city'].isin(selected_cities)]

    # # # Display API results in a table
    # # st.subheader("Air Pollution Index (API) Results")
    # # if 'api' in filtered_data.columns:
    # #     display_data = filtered_data[['city', 'month', 'api']].sort_values(by=['city', 'month'])
    # #     #st.write(display_data)
    # else:
    #     st.write("No valid API data available to display.")

    # Check if there is valid data to plot
    if not filtered_data.empty:
        st.subheader("Boxplot of Air Pollution Index (API) for Different Cities")

        # Create a Plotly boxplot
        fig = px.box(
            filtered_data,
            x='city',
            y='api',
            color='city',
            title="Air Pollution Index (API)",
            labels={
                "city": "City",
                "api": "Air Pollution Index (API)"
            },
            template="plotly"
        )

        fig.update_layout(
            xaxis_title="City",
            yaxis_title="API",
            xaxis_tickangle=45  # Rotate city labels
        )

        # Display the plot in Streamlit
        st.plotly_chart(fig, key="sadsdaasdasdasdz")
    else:
        st.write("No temperature data available for boxplot.")

def build_general_tab(data: DataFrame, selected_cities):
    # Streamlit App
    st.title("Air Pollution Index (API) by City and Month")
    build_api_boxplot(data, selected_cities)

    romania_data = data.copy()

    # Convert 'Date' column to datetime format and drop invalid dates
    romania_data['Date'] = pd.to_datetime(romania_data['Date'], errors='coerce')
    romania_data = romania_data.dropna(subset=['Date'])

    # Extract 'Month' in "YYYY-MM" format
    romania_data['Month'] = romania_data['Date'].dt.to_period('M').astype(str)

    # List of required pollutants for API calculation
    required_pollutants = ['pm10', 'pm25', 'no2', 'o3', 'so2', 'co']

    # Filter data to include only rows for the required pollutants
    api_data = romania_data[romania_data['Specie'].str.lower().isin(required_pollutants)].copy()

    # Pivot the data so pollutants become columns
    pivot_data = api_data.pivot_table(
        index=['City', 'Month'],
        columns='Specie',
        values='median',
        aggfunc='max'
    ).reset_index()

    # Clean up column names
    pivot_data.columns.name = None
    pivot_data.columns = [col.lower() if isinstance(col, str) else col for col in pivot_data.columns]

    # Dynamically calculate API as the maximum value across the available pollutants
    available_pollutants = [col for col in required_pollutants if col in pivot_data.columns]
    if available_pollutants:
        pivot_data['api'] = pivot_data[available_pollutants].max(axis=1, skipna=True)
    else:
        st.write("No pollutants available for API calculation.")
        pivot_data['api'] = None

    # Filter the data based on selected cities
    filtered_data = pivot_data[pivot_data['city'].isin(selected_cities)]

    # # Display API results in a table
    # st.subheader("Air Pollution Index (API) Results")
    # if 'api' in filtered_data.columns:
    #     display_data = filtered_data[['city', 'month', 'api']].sort_values(by=['city', 'month'])
    #     st.write(display_data)
    # else:
    #     st.write("No valid API data available to display.")

    # Visualize API results as a bar chart
    st.subheader("Air Pollution Index (API) Visualization")
    if not filtered_data.empty:
        fig = px.bar(
            filtered_data,
            x='month',
            y='api',
            color='city',
            barmode='group',
            title="Monthly Air Pollution Index (API) by City",
            labels={"month": "Month", "api": "Air Pollution Index (API)", "city": "City"}
        )
        fig.update_layout(xaxis={'categoryorder': 'category ascending'})
        st.plotly_chart(fig)
    else:
        st.write("No data available for the selected cities.")