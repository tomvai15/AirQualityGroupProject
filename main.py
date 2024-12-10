import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read CSV file (update the file path as needed)
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

data = load_data("data/romania_data.csv")  # Replace with your actual file path

# Streamlit App
st.title("Romania air quality")

# Sidebar for user inputs
st.sidebar.header("Filters")

romania_data = data[(data["Country"] == "RO")]
selected_city = st.sidebar.selectbox("Select a City:", romania_data["City"].unique())
selected_specie = st.sidebar.radio(
    "Select Specie for Histogram:", data["Specie"].unique()
)

# Filter data for the selected city and specie
city_data = data[(data["City"] == selected_city) & (data["Specie"] == selected_specie)]

if city_data.empty:
    st.write("No data available for the selected city and specie.")
else:
    st.subheader(f"Statistics for {selected_city} ({selected_specie})")
    st.write(f"**Date Range:** {city_data['Date'].min()} to {city_data['Date'].max()}")
    st.write(f"**Count:** {city_data['count'].sum()}")
    st.write(f"**Min:** {city_data['min'].min()}")
    st.write(f"**Max:** {city_data['max'].max()}")
    st.write(f"**Median:** {city_data['median'].median()}")
    st.write(f"**Variance:** {city_data['variance'].mean()}")

    # Create and display histogram
    st.subheader(f"Histogram for {selected_specie}")
    sns.set(style="whitegrid")
    fig, ax = plt.subplots()
    sns.histplot(city_data["median"], bins=10, kde=True, color="blue", ax=ax)
    ax.set_title(f"{selected_specie} Median Distribution")
    st.pyplot(fig)
