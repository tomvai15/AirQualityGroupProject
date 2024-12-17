from pandas import DataFrame
import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
from prophet import Prophet

def perform_backtest_with_percentage(data: pd.DataFrame, train_percentage: float, forecast_horizon: int):
    data['ds'] = pd.to_datetime(data['ds'])
    data = data.sort_values(by='ds')

    # Define training and test sizes
    train_size = int(len(data) * train_percentage)
    train_data = data.iloc[:train_size]
    test_data = data.iloc[train_size:train_size + forecast_horizon]

    # Train the Prophet model
    model = Prophet()
    model.fit(train_data)

    # Forecast the test period
    future = model.make_future_dataframe(periods=forecast_horizon, freq='D')
    forecast = model.predict(future)

    # Extract forecasted values
    forecasted_values = forecast[['ds', 'yhat']].set_index('ds').loc[test_data['ds']].reset_index()
    predicted_y = forecasted_values['yhat'].values
    actual_y = test_data['y'].values

    # Calculate errors
    mae = mean_absolute_error(actual_y, predicted_y)
    mape = mean_absolute_percentage_error(actual_y, predicted_y) * 100  # in percentage

    # Store results in a DataFrame
    results_df = pd.DataFrame({
        'Date': test_data['ds'],
        'Actual': actual_y,
        'Predicted': predicted_y
    })

    errors = {'MAE': mae, 'MAPE': mape}
    return errors, results_df

# Streamlit UI for Multiple Backtesting Scenarios
def build_backtesting_ui():
    st.title("Prophet Model Backtesting - Training Data Percentages")

    # Data upload
    uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type=['csv'])

    if uploaded_file:
        # Load and prepare the data
        data = pd.read_csv(uploaded_file)
        data['Date'] = pd.to_datetime(data['Date'])
        data.rename(columns={"Date": "ds", "api": "y"}, inplace=True)  # Prophet requires 'ds' and 'y'

        st.write("Loaded Data Preview:", data.head())

        # Forecast horizon input
        forecast_horizon = st.sidebar.slider("Forecast Horizon (days)", min_value=7, max_value=90, value=30)

        # Scenarios: Define training percentages
        training_percentages = [0.5, 0.7, 0.9]  # 50%, 70%, and 90% of the data

        # Backtesting for each scenario
        st.subheader("Backtesting Results for Different Training Data Percentages")
        for percentage in training_percentages:
            st.write(f"### Scenario: {int(percentage * 100)}% Training Data")

            errors, results_df = perform_backtest_with_percentage(
                data=data, train_percentage=percentage, forecast_horizon=forecast_horizon
            )

            # Display errors
            st.write(f"**MAE**: {errors['MAE']:.2f}")
            st.write(f"**MAPE**: {errors['MAPE']:.2f}%")

            # Plot actual vs predicted
            st.line_chart(results_df.set_index('Date'))

def build_forecasting_tab(data: DataFrame):
    st.title("Romania Air Quality and Weather Insights")

    # Sidebar for user inputs
    st.sidebar.header("Filters")

    # Extract Romania data
    romania_data = data[data["Country"] == "RO"].copy()

    # Convert 'Date' column to datetime format and drop invalid dates
    romania_data['Date'] = pd.to_datetime(romania_data['Date'], errors='coerce')
    romania_data = romania_data.dropna(subset=['Date'])

    # Extract 'Day' for better precision
    romania_data['Date'] = romania_data['Date'].dt.to_period('D').astype(str)

    # Required pollutants for API calculation
    required_pollutants = ['pm10', 'pm25', 'no2', 'o3', 'so2', 'co']

    # Filter data for required pollutants
    api_data = romania_data[romania_data['Specie'].str.lower().isin(required_pollutants)].copy()

    # Pivot pollutants into columns
    pivot_data = api_data.pivot_table(
        index=['City', 'Date'],
        columns='Specie',
        values='median',
        aggfunc='max'
    ).reset_index()

    # Clean up column names
    pivot_data.columns.name = None
    pivot_data.columns = [col.lower() if isinstance(col, str) else col for col in pivot_data.columns]

    # Dynamically calculate API
    available_pollutants = [col for col in required_pollutants if col in pivot_data.columns]
    if available_pollutants:
        pivot_data['api'] = pivot_data[available_pollutants].max(axis=1, skipna=True)
    else:
        st.write("No pollutants available for API calculation.")
        pivot_data['api'] = None

    # Sidebar: City filter
    st.sidebar.subheader("City Filter")
    selected_cities = st.sidebar.multiselect(
        "Select Cities:",
        options=pivot_data['city'].unique(),
        default=pivot_data['city'].unique(), key="uniqueid"
    )

    # Filter the data based on cities
    filtered_data = pivot_data[pivot_data['city'].isin(selected_cities)]

    # Display current API data
    st.subheader("Air Pollution Index (API) Results")
    if 'api' in filtered_data.columns:
        display_data = filtered_data[['city', 'date', 'api']].sort_values(by=['city', 'date'])
        st.write(display_data)

    ### Forecasting Section ###
    st.subheader("Air Pollution Index Forecasting with Prophet")

    # Select City for Forecasting
    forecast_city = st.selectbox("Select a City for Forecasting:", options=selected_cities)

    # Filter data for the selected city
    city_data = filtered_data[filtered_data['city'] == forecast_city]

    # Check if sufficient data exists
    if city_data.empty or city_data['api'].isna().all():
        st.warning(f"No sufficient API data available for forecasting in {forecast_city}.")
        return

    # Prepare data for Prophet
    city_data = city_data[['date', 'api']].dropna()
    city_data['date'] = pd.to_datetime(city_data['date'])
    city_data = city_data.rename(columns={"date": "ds", "api": "y"})

    # Train the Prophet model
    model = Prophet()
    model.fit(city_data)

    # Generate future dates for prediction (e.g., next 30 days)
    future = model.make_future_dataframe(periods=30, freq='D')
    forecast = model.predict(future)

    # Plot forecast results
    fig = px.line(
        forecast,
        x='ds',
        y='yhat',
        title=f"Air Pollution Index Forecast for {forecast_city}",
        labels={"yhat": "Forecasted API", "ds": "Date"}
    )

    # Overlay historical data
    fig.add_scatter(x=city_data['ds'], y=city_data['y'], mode='markers', name='Historical API')

    # Display Plot
    st.plotly_chart(fig)

    # Show forecasted data
    st.subheader("Forecasted Data")
    st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(30))

    # Forecast horizon input
    forecast_horizon = st.sidebar.slider("Forecast Horizon (days)", min_value=7, max_value=90, value=30)
    # Scenarios: Define training percentages
    training_percentages = [0.5, 0.7, 0.9]  # 50%, 70%, and 90% of the data
    # Backtesting for each scenario
    st.subheader("Backtesting Results for Different Training Data Percentages")
    for percentage in training_percentages:
        st.write(f"### Scenario: {int(percentage * 100)}% Training Data")
        errors, results_df = perform_backtest_with_percentage(
            data=city_data, train_percentage=percentage, forecast_horizon=forecast_horizon
        )
        # Display errors
        st.write(f"**MAE**: {errors['MAE']:.2f}")
        st.write(f"**MAPE**: {errors['MAPE']:.2f}%")
        # Plot actual vs predicted
        st.line_chart(results_df.set_index('Date'))