import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# Read CSV file (update the file path as needed)
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

data = load_data("data/romania_data.csv")


generalTab, humidityAndTempTab, AirQualityTab = st.tabs(["General", "Humidity & Temperature", "Air quality"])

with humidityAndTempTab:
    # Streamlit App
    st.title("Romania air quality")

    # Sidebar for user inputs
    st.sidebar.header("Filters")

    romania_data = data[(data["Country"] == "RO")]
    selected_city = st.sidebar.selectbox("Select a City:", romania_data["City"].unique())

    # Filter data for the selected city and specie
    # city_data = data[(data["City"] == selected_city) & (data["Specie"] == selected_specie)]
    temperature_data = data[(data["City"] == selected_city) & (data["Specie"] == "temperature")]
    humidity_data = data[(data["City"] == selected_city) & (data["Specie"] == "humidity")]
    pm10_data = data[(data["City"] == selected_city) & (data["Specie"] == "pm10")]
    pm25_data = data[(data["City"] == selected_city) & (data["Specie"] == "pm25")]
    
    col1, col2 = st.columns(2)
    # if city_data.empty:
    #     col1.write("No data available for the selected city and specie.")
    # else:
    #     col1.subheader(f"Statistics for {selected_city} ({selected_specie})")
    #     col1.write(f"**Date Range:** {city_data['Date'].min()} to {city_data['Date'].max()}")
    #     col1.write(f"**Count:** {city_data['count'].sum()}")
    #     col1.write(f"**Min:** {city_data['min'].min()}")
    #     col1.write(f"**Max:** {city_data['max'].max()}")
    #     col1.write(f"**Median:** {city_data['median'].median()}")
    #     col1.write(f"**Variance:** {city_data['variance'].mean()}")

    #     # Create and display histogram
    #     col1.subheader(f"Histogram for {selected_specie}")
    #     sns.set(style="whitegrid")
    #     fig, ax = plt.subplots()
    #     sns.histplot(city_data["median"], bins=10, kde=True, color="blue", ax=ax)
    #     ax.set_title(f"{selected_specie} Median Distribution")
    #     col1.pyplot(fig)

    # Create and display bar plot for temperature
    if not temperature_data.empty:
        col2.subheader(f"Monthly Temperature in {selected_city}")
        temperature_data_transformed = pd.to_datetime(temperature_data['Date'])
        temperature_data['Month'] = temperature_data_transformed.dt.month_name() 

        monthly_temp = temperature_data.groupby('Month')['median'].mean()

        months_order = ["January", "February", "March", "April", "May", "June", 
                        "July", "August", "September", "October", "November", "December"]
        monthly_temp = monthly_temp.reindex(months_order, axis=0).dropna()

        fig, ax = plt.subplots()
        monthly_temp.plot(kind='bar', ax=ax, color='orange')
        ax.set_title("Average Monthly Temperature")
        ax.set_xlabel("Month")
        ax.set_ylabel("Average Temperature (°C)")
        col2.pyplot(fig)
    else:
        col2.write("No temperature data available for the selected city.")

    if not humidity_data.empty:
        col1.subheader(f"Monthly Humidity in {selected_city}")

        humidity_data_transformed = pd.to_datetime(humidity_data['Date'])
        humidity_data['Month'] = humidity_data_transformed.dt.month_name() 

        monthly_humi = humidity_data.groupby('Month')['median'].mean()

        months_order = ["January", "February", "March", "April", "May", "June", 
                        "July", "August", "September", "October", "November", "December"]
        monthly_humi = monthly_humi.reindex(months_order, axis=0).dropna()

        fig, ax = plt.subplots()
        monthly_humi.plot(kind='bar', ax=ax, color='blue')
        ax.set_title("Average Monthly Humidity")
        ax.set_xlabel("Month")
        ax.set_ylabel("Average Humidity")
        col1.pyplot(fig)
    else:
        col1.write("No humidity data available for the selected city.")

    # # Merge temperature and PM10 data on Date to prepare for plotting
    # if not temperature_data.empty and not pm10_data.empty:
    #     # Rename median to avoid column name clashes during merge
    #     temperature_data = temperature_data[['Date', 'median']].rename(columns={'median': 'Temperature'})
    #     pm10_data = pm10_data[['Date', 'median']].rename(columns={'median': 'PM10'})
        
    #     combined_data = pd.merge(temperature_data, pm10_data, on='Date', how='inner')

    #     col1.subheader(f"Scatter Plot of Temperature vs PM10 in {selected_city}")

    #     fig, ax = plt.subplots()
    #     ax.scatter(combined_data['Temperature'], combined_data['PM10'], alpha=0.6, c='green')
    #     ax.set_title("Temperature vs PM10")
    #     ax.set_xlabel("Temperature (°C)")
    #     ax.set_ylabel("PM10 (µg/m³)")
    #     col1.pyplot(fig)
    # else:
    #     col1.write("Insufficient data for temperature and PM10 to create scatter plot.")


    # Merge temperature and PM10 data on Date to prepare for plotting
    if not temperature_data.empty and not pm10_data.empty:
        # Rename median to avoid column name clashes during merge
        temperature_data_transformed = temperature_data[['Date', 'median']].rename(columns={'median': 'Temperature'})
        pm10_data = pm10_data[['Date', 'median']].rename(columns={'median': 'PM10'})
        
        combined_data = pd.merge(temperature_data_transformed, pm10_data, on='Date', how='inner')

        col2.subheader(f"Scatter Plot of Temperature vs PM10 in {selected_city} with Regression Line")

        fig, ax = plt.subplots()
        sns.regplot(x='Temperature', y='PM10', data=combined_data, ax=ax, scatter_kws={'alpha':0.6}, line_kws={"color": "red"})
        ax.set_title("Temperature vs PM10 with Regression Line")
        ax.set_xlabel("Temperature (°C)")
        ax.set_ylabel("PM10 (µg/m³)")
        col2.pyplot(fig)
    else:
        col2.write("Insufficient data for temperature and PM10 to create scatter plot.")

    if not temperature_data.empty and not pm25_data.empty:
        # Rename median to avoid column name clashes during merge
        temperature_data = temperature_data[['Date', 'median']].rename(columns={'median': 'Temperature'})
        pm25_data = pm25_data[['Date', 'median']].rename(columns={'median': 'PM25'})
        
        combined_data = pd.merge(temperature_data, pm25_data, on='Date', how='inner')

        col1.subheader(f"Scatter Plot of Temperature vs PM25 in {selected_city} with Regression Line")

        fig, ax = plt.subplots()
        sns.regplot(x='Temperature', y='PM25', data=combined_data, ax=ax, scatter_kws={'alpha':0.6}, line_kws={"color": "red"})
        ax.set_title("Temperature vs PM25 with Regression Line")
        ax.set_xlabel("Temperature (°C)")
        ax.set_ylabel("PM25 (µg/m³)")
        col1.pyplot(fig)
    else:
        col1.write("Insufficient data for temperature and PM25 to create scatter plot.")

with AirQualityTab:
    # Streamlit App
    temperature_data = data[data['Specie'] == "temperature"]

    if not temperature_data.empty:
        st.subheader("Boxplot of Temperature for Different Cities")

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(x='City', y='median', data=temperature_data, ax=ax, palette="Set3")
        ax.set_title("Temperature Distribution by City")
        ax.set_xlabel("City")
        ax.set_ylabel("Temperature (°C)")
        plt.xticks(rotation=45)  # Rotate city labels if necessary
        st.pyplot(fig)
    else:
        st.write("No temperature data available for boxplot.")

with generalTab:

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

            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(x='City', y='median', data=filtered_temperature_data, ax=ax, palette="Set3", showfliers=False)
            ax.set_title("Temperature Distribution by City")
            ax.set_xlabel("City")
            ax.set_ylabel("Temperature (°C)")
            plt.xticks(rotation=45)  # Rotate city labels if necessary
            st.pyplot(fig)
        else:
            st.write("No temperature data available for the selected cities and date range.")

         # Filter temperature data based on selected cities
        filtered_pm10_data = data[data['City'].isin(selected_cities)]

        if not filtered_pm10_data.empty:
            st.subheader("Boxplot of PM10 for Selected Cities")

            fig, ax = plt.subplots(figsize=(10, 6))
            sns.boxplot(x='City', y='median', data=filtered_pm10_data, ax=ax, palette="Set3", showfliers=False)
            ax.set_title("PM10 Distribution by City")
            ax.set_xlabel("City")
            ax.set_ylabel("PM10")
            plt.xticks(rotation=45)  # Rotate city labels if necessary
            st.pyplot(fig)
        else:
            st.write("No PM10 data available for the selected cities and date range.")
    else:
        st.write("No temperature data available for plotting.")