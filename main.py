import streamlit as st
import pandas as pd

from tabs.air_quality_tab import build_air_quality_tab
from tabs.forecasting_tab import build_forecasting_tab
from tabs.general_tab import build_general_tab
from tabs.humidity_and_temp_tab import build_humidity_and_temp_tab
from tabs.insights_tab_v2 import build_insights_tab

st.set_page_config(layout="wide")

# Read CSV file (update the file path as needed)
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

data = load_data("data/romania_data_full.csv")

st.title("Romania air quality")
st.sidebar.header("Filters")
selected_city = st.sidebar.selectbox("Select a City:", data["City"].unique())
selected_cities = st.sidebar.multiselect(
    "Select Cities:",
    options=data['City'].unique(),
    default=data['City'].unique()
)

st.sidebar.header("Forecast settings")
forecast_horizon = st.sidebar.slider("Forecast Horizon (days)", min_value=7, max_value=90, value=30)
required_pollutants = ['pm10', 'pm25', 'no2', 'o3', 'so2', 'co']
unique_values_excluding_pollutants = [specie for specie in data["Specie"].unique() if specie not in required_pollutants]
selected_regressor = st.sidebar.selectbox("Select a regressor:", unique_values_excluding_pollutants)

general_tab, humidity_and_temp_tab, insights_tab, forecasting_tab = st.tabs(["General", "City", "Insights", "Forecasting"])

with humidity_and_temp_tab:
    build_humidity_and_temp_tab(data, selected_city)

with general_tab:
    build_general_tab(data, selected_cities)

with insights_tab:
    build_insights_tab(data, selected_cities, selected_city)

with forecasting_tab:
    build_forecasting_tab(data, selected_city, forecast_horizon, selected_regressor)