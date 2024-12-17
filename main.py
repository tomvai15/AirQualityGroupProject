import streamlit as st
import pandas as pd

from tabs.air_quality_tab import build_air_quality_tab
from tabs.general_tab import build_general_tab
from tabs.humidity_and_temp_tab import build_humidity_and_temp_tab

st.set_page_config(layout="wide")

# Read CSV file (update the file path as needed)
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

data = load_data("data/romania_data.csv")
st.write("Columns in dataset:", data.columns)

general_tab, humidity_and_temp_tab, air_quality_tab = st.tabs(["General", "Humidity & Temperature", "Air quality"])

with humidity_and_temp_tab:
    build_humidity_and_temp_tab(data)

with air_quality_tab:
    build_air_quality_tab(data)

with general_tab:
    build_general_tab(data)