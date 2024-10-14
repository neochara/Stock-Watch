import yfinance as yf
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

# Set the title for the Streamlit app
st.title('Trend for This Month')

# Define the stock symbol
stock_symbol = 'NVDA'

# Get the current date and the first day of the current month
today = datetime.today()
#start_of_month = today.replace(day=1)
start_of_month = today.replace(month=1, day=1)  # start of year

# Download stock data for this month
nvidia_stock = yf.download(stock_symbol, start=start_of_month, end=today.strftime('%Y-%m-%d'))

# Display the raw data in Streamlit
st.write("NVIDIA Stock Data for This Month")
st.dataframe(nvidia_stock)

# Plot the closing prices using Matplotlib
st.write("Closing Price Trend")

plt.figure(figsize=(10, 6))
plt.plot(nvidia_stock.index, nvidia_stock['Close'], marker='o', linestyle='-', color='b')
plt.title(f'NVIDIA Stock Closing Prices - {today.strftime("%B %Y")}', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Closing Price (USD)', fontsize=12)
plt.grid(True)
st.pyplot(plt)
