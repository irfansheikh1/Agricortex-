# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import joblib
from statsmodels.tsa.arima.model import ARIMAResults

# Load the dataset
url = "Tomato.csv"  # Replace with the actual URL or file path
df = pd.read_csv(url)
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# Sidebar for user input
st.sidebar.header('User Input')
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2013-06-16"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2021-01-01"))

# Load the trained ARIMA model
# arima_model = joblib.load('model (1).joblib')
arima_model = joblib.load('PricePrediction/model (1).joblib')

# Create a date range for forecasting
forecast_dates = pd.date_range(start=end_date + pd.DateOffset(days=1), periods=300)

# Forecast using the ARIMA model
forecast = arima_model.forecast(steps=len(forecast_dates))

# Display the forecast in the Streamlit app using Plotly
st.header('🍅ARIMA Time Series Forecasting Tomato🍅')

# Plotting with Plotly
fig = go.Figure()

# Historical Prices
fig.add_trace(go.Scatter(x=df.index, y=df['Average'], mode='lines', name='Historical Prices'))

# Forecasted Prices
fig.add_trace(go.Scatter(x=forecast_dates, y=forecast, mode='lines', name='Forecasted Prices'))

# Highlight forecasted period
fig.add_shape(
    type='rect',
    x0=forecast_dates[0],
    x1=forecast_dates[-1],
    y0=min(df['Average']),
    y1=max(df['Average']),
    fillcolor='rgba(255, 0, 0, 0.1)',  # Light red background
    line=dict(color='rgba(255, 0, 0, 0.5)', width=2),
    layer='below'
)

# Update layout for better visualization
fig.update_layout(
    title='ARIMA Time Series Forecasting',
    xaxis_title='Date',
    yaxis_title='Average Price',
    showlegend=True,
    template='plotly_dark',  # You can choose other templates like 'plotly' or 'seaborn' as well
    xaxis_range=[start_date, forecast_dates[-1]]  # Adjust the x-axis range
)

# Show the plot in the Streamlit app
st.plotly_chart(fig)
