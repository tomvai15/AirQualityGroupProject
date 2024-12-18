from pandas import DataFrame
import streamlit as st
import pandas as pd
import plotly.express as px

def build_question_1(data: DataFrame, selected_cities):
    st.title("Romania Air Quality and Weather Insights")

    # Preprocessing
    romania_data = data.copy()
    romania_data['Date'] = pd.to_datetime(romania_data['Date'], errors='coerce')
    romania_data = romania_data.dropna(subset=['Date', 'median'])  # Ensure valid rows
    romania_data['Month'] = romania_data['Date'].dt.month_name()  # Month names

    romania_data = romania_data[romania_data['City'].isin(selected_cities)]

    # Pivot the data
    pivot_data = romania_data.pivot_table(
        index=['City', 'Date'],
        columns='Specie',
        values='median',
        aggfunc='max'
    ).reset_index()

    # Calculate API (Air Quality Index)
    required_pollutants = ['pm10', 'pm25', 'no2', 'o3', 'so2', 'co']
    available_pollutants = [col for col in required_pollutants if col in pivot_data.columns]

    if available_pollutants:
        pivot_data['api'] = pivot_data[available_pollutants].max(axis=1, skipna=True)
    else:
        st.write("No pollutants available for API calculation.")
        pivot_data['api'] = None

    # Question 1: How does air pollution vary across cities throughout the year?
    st.subheader("1. How does air pollution vary across cities throughout the year?")
    pollutants = ["api", "pm10", "pm25", "no2", "o3", "so2", "co"]  # Add API as an option
    pollutant_choice = st.selectbox("Select a pollutant or API:", pollutants, key="q2_pollutant")

    pollution_data = pivot_data[['City', 'Date', pollutant_choice]].dropna()
    pollution_data['Month'] = pollution_data['Date'].dt.month_name()

    # Define month order
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    # Convert 'Month' to categorical with order
    pollution_data['Month'] = pd.Categorical(pollution_data['Month'], categories=month_order, ordered=True)

    # Group data by city and month
    monthly_pollution = pollution_data.groupby(['City', 'Month'])[pollutant_choice].mean().reset_index()

    # Plot the data
    fig_q1 = px.line(
        monthly_pollution,
        x="Month",
        y=pollutant_choice,
        color="City",
        title=f"Monthly Average {pollutant_choice.upper()} Levels Across Cities",
        labels={pollutant_choice: f"{pollutant_choice.upper()} (µg/m³)", "Month": "Month"}
    )
    st.plotly_chart(fig_q1)

    st.text("Largest pollution levels are observed during the cold season months – November till March. ​\nThe biggest offender is the city of Bucharest, with API ranging from 30.93 to 56.17 for the cold season months, with yearly mean of 42; closest city has API mean of 24")

def build_question_2_1(data: DataFrame, selected_cities):
    # Preprocessing
    romania_data = data.copy()
    romania_data['Date'] = pd.to_datetime(romania_data['Date'], errors='coerce')
    romania_data = romania_data.dropna(subset=['Date', 'median'])  # Ensure valid rows
    romania_data['Month'] = romania_data['Date'].dt.month_name()  # Month names

    romania_data = romania_data[romania_data['City'].isin(selected_cities)]

    # Pivot the data
    pivot_data = romania_data.pivot_table(
        index=['City', 'Date'],
        columns='Specie',
        values='median',
        aggfunc='max'
    ).reset_index()

    # Calculate API (Air Quality Index)
    required_pollutants = ['pm10', 'pm25', 'no2', 'o3', 'so2', 'co']    # Dynamically calculate API
    available_pollutants = [col for col in required_pollutants if col in pivot_data.columns]

    if available_pollutants:
        pivot_data['api'] = pivot_data[available_pollutants].max(axis=1, skipna=True)
    else:
        st.write("No pollutants available for API calculation.")
        pivot_data['api'] = None

    # Question 2: Which months are the coldest and hottest in Romania?
    st.subheader("2. Which months are the coldest and hottest in Romania?")
    temperature_data = pivot_data[['City', 'Date', 'temperature']].dropna()
    temperature_data['Month'] = temperature_data['Date'].dt.month_name()

    # Group by City and Month to get the average temperature
    avg_temp = temperature_data.groupby(['City', 'Month'])['temperature'].mean().reset_index()

    # Create the bar chart
    fig_q2 = px.bar(
        avg_temp,
        x="Month",
        y="temperature",
        color="City",
        title="Average Monthly Temperature Across Cities",
        labels={"temperature": "Temperature (°C)", "Month": "Month"}
    )

    # Update the x-axis to display months in order
    fig_q2.update_xaxes(categoryorder="array", categoryarray=["January", "February", "March", "April", "May", "June",
                                                             "July", "August", "September", "October", "November", "December"])

    temperature_data = pivot_data[['City', 'Date', 'temperature']].dropna()

    # Extract the month from the Date column
    temperature_data['Month'] = temperature_data['Date'].dt.month_name()

    # Group by Month to get the average temperature across all cities
    avg_temp = temperature_data.groupby('Month')['temperature'].mean().reset_index()

    # Create the bar chart
    fig_q2 = px.bar(
        avg_temp,
        x="Month",
        y="temperature",
        title="Average Monthly Temperature Across All Cities",
        labels={"temperature": "Temperature (°C)", "Month": "Month"}
    )

    # Update the x-axis to display months in order
    fig_q2.update_xaxes(categoryorder="array", categoryarray=["January", "February", "March", "April", "May", "June",
                                                             "July", "August", "September", "October", "November", "December"])

    # Show the plot
    st.plotly_chart(fig_q2)

    st.write("Coldest – January, with mean of 2.7C; hottest – July, with mean of 23C.")


def build_question_2_2(data: DataFrame, selected_city):
    # Preprocessing
    romania_data = data.copy()
    romania_data['Date'] = pd.to_datetime(romania_data['Date'], errors='coerce')
    romania_data = romania_data.dropna(subset=['Date', 'median'])  # Ensure valid rows
    romania_data['Month'] = romania_data['Date'].dt.month_name()  # Month names

    romania_data = romania_data[romania_data['City'].isin([selected_city])]

    # Pivot the data
    pivot_data = romania_data.pivot_table(
        index=['City', 'Date'],
        columns='Specie',
        values='median',
        aggfunc='max'
    ).reset_index()

    # Calculate API (Air Quality Index)
    required_pollutants = ['pm10', 'pm25', 'no2', 'o3', 'so2', 'co']    # Dynamically calculate API
    available_pollutants = [col for col in required_pollutants if col in pivot_data.columns]

    if available_pollutants:
        pivot_data['api'] = pivot_data[available_pollutants].max(axis=1, skipna=True)
    else:
        st.write("No pollutants available for API calculation.")
        pivot_data['api'] = None

    # Filter the pivoted data for the selected city and temperature
    city_temperature_data = pivot_data[pivot_data['City'] == selected_city][['City', 'Date', 'temperature']].dropna()

    # Extract the month from the Date column
    city_temperature_data['Month'] = city_temperature_data['Date'].dt.month_name()

    # Group by Month to get the average temperature for the selected city
    avg_city_temp = city_temperature_data.groupby('Month')['temperature'].mean().reset_index()

    # Create the bar chart for the selected city's average monthly temperature
    fig_q2 = px.bar(
        avg_city_temp,
        x="Month",
        y="temperature",
        title=f"Average Monthly Temperature for {selected_city}",
        labels={"temperature": "Temperature (°C)", "Month": "Month"}
    )

    # Update the x-axis to display months in order
    fig_q2.update_xaxes(categoryorder="array", categoryarray=["January", "February", "March", "April", "May", "June",
                                                         "July", "August", "September", "October", "November", "December"])

    # Show the plot
    st.plotly_chart(fig_q2)



def build_question_3(data: DataFrame, selected_city):
    # Preprocessing
    romania_data = data.copy()
    romania_data['Date'] = pd.to_datetime(romania_data['Date'], errors='coerce')
    romania_data = romania_data.dropna(subset=['Date', 'median'])  # Ensure valid rows
    romania_data['Month'] = romania_data['Date'].dt.month_name()  # Month names

    romania_data = romania_data[romania_data['City'].isin([selected_city])]

    # Pivot the data
    pivot_data = romania_data.pivot_table(
        index=['City', 'Date'],
        columns='Specie',
        values='median',
        aggfunc='max'
    ).reset_index()

    pivot_data['Month'] = pivot_data['Date'].dt.month_name()


    # Calculate API (Air Quality Index)
    required_pollutants = ['pm10', 'pm25', 'no2', 'o3', 'so2', 'co']    # Dynamically calculate API
    available_pollutants = [col for col in required_pollutants if col in pivot_data.columns]

    if available_pollutants:
        pivot_data['api'] = pivot_data[available_pollutants].max(axis=1, skipna=True)
    else:
        st.write("No pollutants available for API calculation.")
        pivot_data['api'] = None

    # List of pollutants to choose from
    pollutants = ["api", "pm10", "pm25", "no2", "o3", "so2", "co"]

    # Question: How does air pollution correlate with temperature in the selected city?
    st.subheader("3. How does temperature relate to air pollution levels?")

    # Select pollutant
    pollutant_choice = st.selectbox("Select a pollutant:", pollutants, key="q3_pollutant")

    # Filter the pivoted data for the selected city and pollutant
    city_data = pivot_data[pivot_data['City'] == selected_city].dropna(subset=['temperature', pollutant_choice])

    # Scatter plot of the selected pollutant against temperature
    fig_q3 = px.scatter(
        city_data,
        x=pollutant_choice,
        y="temperature",
        trendline="ols",
        title=f"Correlation Between {pollutant_choice.upper()} and Temperature in {selected_city}",
        labels={pollutant_choice: f"{pollutant_choice.upper()} (µg/m³)", "temperature": "Temperature (°C)"},
    )

    # Show the plot
    st.plotly_chart(fig_q3)

    st.write("No correlation was detected between temperature and selected pollutants.")


def build_question_4(data: DataFrame, selected_cities):
    # Preprocessing
    romania_data = data.copy()
    romania_data['Date'] = pd.to_datetime(romania_data['Date'], errors='coerce')
    romania_data = romania_data.dropna(subset=['Date', 'median'])  # Ensure valid rows
    romania_data['Month'] = romania_data['Date'].dt.month_name()  # Month names

    romania_data = romania_data[romania_data['City'].isin(selected_cities)]

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

    st.write("Based on the analysis of the air quality data across selected Romanian cities, Bucharest was found to have the most polluted air, while Iași had the cleanest air in terms of the Air Pollution Index (API).")

def build_question_5(data: DataFrame, selected_cities):
    # Preprocessing
    romania_data = data.copy()
    romania_data['Date'] = pd.to_datetime(romania_data['Date'], errors='coerce')
    romania_data = romania_data.dropna(subset=['Date', 'median'])  # Ensure valid rows
    romania_data['Month'] = romania_data['Date'].dt.month_name()  # Month names

    romania_data = romania_data[romania_data['City'].isin(selected_cities)]

    # Add Season Column
    romania_data['Season'] = romania_data['Date'].dt.month.map({
        12: 'Winter', 1: 'Winter', 2: 'Winter',
        3: 'Spring', 4: 'Spring', 5: 'Spring',
        6: 'Summer', 7: 'Summer', 8: 'Summer',
        9: 'Autumn', 10: 'Autumn', 11: 'Autumn'
    })

    # Pivot the data
    pivot_data = romania_data.pivot_table(
        index=['City', 'Date'],
        columns='Specie',
        values='median',
        aggfunc='max'
    ).reset_index()

        # Question 5: How do pollution levels change in winter versus summer?
    st.subheader("5. How do pollution levels change in winter versus summer?")

    # Add Month and Season Columns to Pivot Data
    pivot_data['Month'] = pivot_data['Date'].dt.month_name()
    pivot_data['Season'] = pivot_data['Date'].dt.month.map({
        12: 'Winter', 1: 'Winter', 2: 'Winter',
        3: 'Spring', 4: 'Spring', 5: 'Spring',
        6: 'Summer', 7: 'Summer', 8: 'Summer',
        9: 'Autumn', 10: 'Autumn', 11: 'Autumn'
    })

    # Calculate API (Air Quality Index)
    required_pollutants = ['pm10', 'pm25', 'no2', 'o3', 'so2', 'co']
    available_pollutants = [col for col in required_pollutants if col in pivot_data.columns]

    if available_pollutants:
        pivot_data['api'] = pivot_data[available_pollutants].max(axis=1, skipna=True)
    else:
        st.write("No pollutants available for API calculation.")
        pivot_data['api'] = None

    # Pollutant selection
    pollutants = ["api", "pm10", "pm25", "no2", "o3", "so2", "co"]
    season_pollutant = st.selectbox("Select a pollutant:", pollutants, key="q5_pollutant")

    # Filter Pivot Data for the Selected Pollutant
    if season_pollutant in pivot_data.columns:
        # Melt data for analysis
        season_data = pivot_data[['City', 'Season', season_pollutant]].dropna()

        # Group by City and Season
        avg_season_pollution = season_data.groupby(['City', 'Season'])[season_pollutant].mean().reset_index()

        # Plot results
        fig_q5 = px.bar(
            avg_season_pollution,
            x="City",
            y=season_pollutant,
            color="Season",
            title=f"Average {season_pollutant.upper()} Levels in Winter vs Summer",
            labels={season_pollutant: f"{season_pollutant.upper()} (µg/m³)", "City": "City", "Season": "Season"}
        )
        st.plotly_chart(fig_q5)
    else:
        st.write(f"{season_pollutant} data is not available.")

    st.write("Winter consistently exhibits the highest pollution levels across all cities. This is likely due to increased heating activities, which generate emissions from residential and industrial sources.")


def build_insights_tab(data: DataFrame, selected_cities, selected_city):
    build_question_1(data, selected_cities)
    build_question_2_1(data, selected_cities)
    build_question_2_2(data, selected_city)
    build_question_3(data, selected_city)
    build_question_4(data, selected_cities)
    build_question_5(data, selected_cities)
   
