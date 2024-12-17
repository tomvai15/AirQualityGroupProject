from pandas import DataFrame
import streamlit as st
import pandas as pd
import plotly.express as px

def build_insights_tab(data: DataFrame, selected_cities):
    # Streamlit App
    st.title("Romania Air Quality and Weather Insights")

    # Preprocessing
    romania_data = data.copy()
    romania_data['Date'] = pd.to_datetime(romania_data['Date'], errors='coerce')
    romania_data = romania_data.dropna(subset=['Date', 'median'])  # Ensure valid rows
    romania_data['Month'] = romania_data['Date'].dt.month_name()  # Month names

    romania_data = romania_data[romania_data['City'].isin(selected_cities)]

    # Question 1: How does air pollution vary across cities throughout the year?
    st.subheader("1. How does air pollution vary across cities throughout the year?")
    pollutants = ["pm10", "pm25", "no2", "o3", "so2", "co"]
    pollutant_choice = st.selectbox("Select a pollutant:", pollutants, key="q1_pollutant")

    pollution_data = romania_data[romania_data["Specie"].str.lower() == pollutant_choice].copy()
    monthly_pollution = pollution_data.groupby(['City', 'Month'])['median'].mean().reset_index()

    fig_q1 = px.line(
        monthly_pollution,
        x="Month",
        y="median",
        color="City",
        title=f"Monthly Average {pollutant_choice.upper()} Levels Across Cities",
        labels={"median": f"{pollutant_choice.upper()} (µg/m³)", "Month": "Month"}
    )
    st.plotly_chart(fig_q1)

    # Question 2: Which months are the coldest and hottest in Romania?
    st.subheader("2. Which months are the coldest and hottest in Romania?")
    temperature_data = romania_data[romania_data["Specie"].str.lower() == "temperature"].copy()
    avg_temp = temperature_data.groupby(['City', 'Month'])['median'].mean().reset_index()

    fig_q2 = px.bar(
        avg_temp,
        x="Month",
        y="median",
        color="City",
        title="Average Monthly Temperature Across Cities",
        labels={"median": "Temperature (°C)", "Month": "Month"}
    )
    fig_q2.update_xaxes(categoryorder="array", categoryarray=["January", "February", "March", "April", "May", "June",
                                                             "July", "August", "September", "October", "November", "December"])
    st.plotly_chart(fig_q2)

    # Question 3: How does temperature relate to air pollution levels?
    st.subheader("3. How does temperature relate to air pollution levels?")
    scatter_pollutant = st.selectbox("Select a pollutant for comparison:", pollutants, key="q3_pollutant")
    temp_data = romania_data[romania_data["Specie"].str.lower() == "temperature"].copy()
    pollutant_data = romania_data[romania_data["Specie"].str.lower() == scatter_pollutant].copy()

    # Merge temperature and pollutant data on Date and City
    combined_data = pd.merge(
        temp_data[['Date', 'City', 'median']].rename(columns={'median': 'Temperature'}),
        pollutant_data[['Date', 'City', 'median']].rename(columns={'median': scatter_pollutant.upper()}),
        on=['Date', 'City'],
        how='inner'
    )

    fig_q3 = px.scatter(
        combined_data,
        x="Temperature",
        y=scatter_pollutant.upper(),
        color="City",
        trendline="ols",
        title=f"Relationship Between Temperature and {scatter_pollutant.upper()} Levels",
        labels={"Temperature": "Temperature (°C)", scatter_pollutant.upper(): f"{scatter_pollutant.upper()} (µg/m³)"}
    )
    st.plotly_chart(fig_q3)

    # Question 4: Which cities have the cleanest and most polluted air (API)?
    st.subheader("4. Which cities have the cleanest and most polluted air (API)?")
    api_pollutants = ["pm10", "pm25", "no2", "o3", "so2", "co"]
    pivot_data = romania_data[romania_data["Specie"].str.lower().isin(api_pollutants)].pivot_table(
        index=["City", "Date"],
        columns="Specie",
        values="median",
        aggfunc="max"
    ).reset_index()

    # Dynamically check for available pollutants
    pivot_data.columns = pivot_data.columns.str.lower()  # Standardize column names
    available_api_pollutants = [col for col in api_pollutants if col in pivot_data.columns]

    if available_api_pollutants and 'city' in pivot_data.columns:
        # Calculate API as the maximum of the available pollutants
        pivot_data['api'] = pivot_data[available_api_pollutants].max(axis=1, skipna=True)
        avg_api = pivot_data.groupby("city")['api'].mean().reset_index().sort_values(by="api", ascending=False)

        # Plot the API values
        fig_q4 = px.bar(
            avg_api,
            x="city",
            y="api",
            title="Average Air Pollution Index (API) by City",
            labels={"api": "Average API", "city": "City"}
        )
        st.plotly_chart(fig_q4)
    else:
        st.write("No pollutants available or 'City' column missing to calculate API. Please check the dataset.")

    # Question 5: How do pollution levels change in winter versus summer?
    st.subheader("5. How do pollution levels change in winter versus summer?")
    romania_data['Season'] = romania_data['Date'].dt.month.map({
        12: 'Winter', 1: 'Winter', 2: 'Winter',
        3: 'Spring', 4: 'Spring', 5: 'Spring',
        6: 'Summer', 7: 'Summer', 8: 'Summer',
        9: 'Autumn', 10: 'Autumn', 11: 'Autumn'
    })
    season_pollutant = st.selectbox("Select a pollutant:", pollutants, key="q5_pollutant")
    season_data = romania_data[romania_data["Specie"].str.lower() == season_pollutant]

    avg_season_pollution = season_data.groupby(['City', 'Season'])['median'].mean().reset_index()

    fig_q5 = px.bar(
        avg_season_pollution,
        x="City",
        y="median",
        color="Season",
        title=f"Average {season_pollutant.upper()} Levels in Winter vs Summer",
        labels={"median": f"{season_pollutant.upper()} (µg/m³)", "City": "City", "Season": "Season"}
    )
    st.plotly_chart(fig_q5)