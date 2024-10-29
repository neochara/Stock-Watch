import streamlit as st
from data_analysis import get_clean_data, get_description, get_nl_summary
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mplfinance as mpf
from datetime import datetime

st.title('Stock Watch :sunglasses:')

# idx_of_interest = 'cost'
idx_of_interest = st.selectbox("Select a stock index:",
                                ('NVDA', 'TSLA', 'AMZN', 'MSFT', 'COST', 'GME', 'PFE', 'LLY'))

st.write(f"Let us summarize the {idx_of_interest} stock")
idx_of_interest = idx_of_interest.lower()

# - - - Plot timeseries - - -
stocks_dfs_dict = get_clean_data()

idx_df = stocks_dfs_dict[idx_of_interest]
#company_of_interest = idx_df['copmany_name']

# Display data to streamlit
st.header(f"{idx_of_interest.upper()} Stock Data")
st.dataframe(idx_df)

# - - - Plots of opening and closing price - - -
# Plot of opening price
st.header(f"Opening Price Time Series of {idx_of_interest.upper()}")

plt.figure(figsize=(10, 6))
plt.plot(idx_df.index, idx_df['Open'], marker='x', linestyle='-', color='b')
plt.title(f'{idx_of_interest.upper()} Stock Opening Prices', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Opening Price (USD)', fontsize=12)
plt.grid(True)
st.pyplot(plt)

# Plot of closing price
st.header(f"Closing Price Time Series of {idx_of_interest.upper()}")

plt.figure(figsize=(10, 6))
plt.plot(idx_df.index, idx_df['Close'], marker='o', linestyle='-', color='r')
plt.title(f'{idx_of_interest.upper()} Stock Closing Prices', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Closing Price (USD)', fontsize=12)
plt.grid(True)
st.pyplot(plt)

# Plot both opening and closing price
st.header(f"Opening and Closing Price Time Series of {idx_of_interest.upper()}")
plt.figure(figsize=(10, 6))
plt.plot(idx_df.index, idx_df['Open'], linestyle='-', color='b', label='Opening Price')
plt.plot(idx_df.index, idx_df['Close'], linestyle='-', color='r', label='Closing Price')
plt.title(f'{idx_of_interest.upper()} Stock Prices', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Price (USD)', fontsize=12)
plt.grid(True)
st.pyplot(plt)

# Plot difference between opening and closing price
st.header(f"Difference between Closing and Opening Price Time Series of {idx_of_interest.upper()}")
plt.figure(figsize=(10, 6))
plt.plot(idx_df.index, idx_df['Close']-idx_df['Open'], linestyle='-', color='m')
plt.title(f'{idx_of_interest.upper()} Stock Prices', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Price (USD)', fontsize=12)
plt.grid(True)
st.pyplot(plt)

# - - - Plot timeseries description table - - -
description_dict = get_description()
description_idx_df = description_dict[idx_of_interest]

st.header(f"{idx_of_interest.upper()} Stock Data Statistics")
st.dataframe(description_idx_df)

# - - - Display Text Summary - - -
# response_dict = get_nl_summary()
# response_idx = response_dict[idx_of_interest]

# st.header(f"{idx_of_interest.upper()} Stock Summary")
# st.text(response_idx)

# - - - Plot EWMA on Closing Prices - - -

alpha = st.number_input("Enter a smoothing parameter $\\alpha$ between 0 and 1:",
                        min_value=0.01, max_value=1.0, value=0.3, step=0.01)
#st.write(f"You entered alpha = {alpha}")

ewma_nvda_closing = pd.Series(idx_df['Close']).ewm(alpha=alpha, adjust=False).mean()

st.header(f"EWMA of Closing Price Time Series of {idx_of_interest.upper()}")
plt.figure(figsize=(12, 6))
plt.plot(idx_df['Close'], label='Original Data', color='skyblue')
plt.plot(ewma_nvda_closing, label=f'EWMA (alpha={alpha})', color='orange')
plt.title('Exponentially Weighted Moving Average (EWMA)', fontsize=16)
plt.xlabel('Time', fontsize=12)
plt.ylabel('Value', fontsize=12)
plt.legend()
plt.grid()
plt.show()
st.pyplot(plt)

# - - - Plot EWMA on Closing Prices with varying half-life - - -

half_life_short = st.number_input("Enter a half-life of your EWMA in days, up to 3 years",
                        min_value=1, max_value=1095, value=30, step=1)
alpha_hl_short = 1 - np.exp(-np.log(2)/half_life_short)
st.write(f"For half-life = {half_life_short}, we get $\\alpha$ = {alpha_hl_short}")

half_life_long = st.number_input("Enter a longer half-life of your EWMA in days, up to 3 years",
                        min_value=half_life_short, max_value=1095, value=100, step=1)
alpha_hl_long = 1 - np.exp(-np.log(2)/half_life_long)
st.write(f"For the longer half-life = {half_life_long}, we get $\\alpha$ = {alpha_hl_long}")

ewma_nvda_closing_hl_short = pd.Series(idx_df['Close']).ewm(alpha=alpha_hl_short, adjust=False).mean()
ewma_nvda_closing_hl_long = pd.Series(idx_df['Close']).ewm(alpha=alpha_hl_long, adjust=False).mean()

st.header(f"EWMA of Closing Price Time Series of {idx_of_interest.upper()} -- varying half-life")
plt.figure(figsize=(12, 6))
plt.plot(idx_df['Close'], label='Original Data', color='skyblue')
plt.plot(ewma_nvda_closing_hl_short, label=f'short half-life={half_life_short}', color='orange')
plt.plot(ewma_nvda_closing_hl_long, label=f'long half-life={half_life_long}', color='green')
plt.title('Exponentially Weighted Moving Average (EWMA) -- varying half-life', fontsize=16)
plt.xlabel('Time', fontsize=12)
plt.ylabel('Value', fontsize=12)
plt.legend()
plt.grid()
plt.show()
st.pyplot(plt)

# - - - Plot Candlestick Chart on Closing Prices - - -

st.header(f"Candlestick Chart Analysis on Closing Prices of {idx_of_interest.upper()}")
fig, ax = mpf.plot(idx_df, type='candle', style='charles', 
                    title=f"Candlestick Chart for {idx_of_interest.upper()}",
                    ylabel='Price', volume=True, returnfig=True)
st.pyplot(fig)

st.write("**Naked Price Action** -- green candlesticks are **bullish** (increase in price), red candlesticks are **bearish** (increase in price).")
