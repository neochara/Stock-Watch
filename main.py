import streamlit as st
from data_analysis import get_clean_data, get_description, get_nl_summary
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mplfinance as mpf
from datetime import datetime

# Set up the main tab
st.title('Stock Watch :sunglasses:')
tab = st.tabs(["Main Analysis"])[0]

with tab:
    st.header("This is Tab 1")

    # Select stock index
    idx_of_interest = st.selectbox("Select a stock index:", ('NVDA', 'TSLA', 'AMZN', 'MSFT', 'COST', 'GME', 'PFE', 'LLY'))
    st.write(f"Let us summarize the {idx_of_interest} stock")
    idx_of_interest = idx_of_interest.lower()

    # Get stock data
    stocks_dfs_dict = get_clean_data()
    idx_df = stocks_dfs_dict[idx_of_interest]

    # Display stock data
    st.header(f"{idx_of_interest.upper()} Stock Data")
    st.dataframe(idx_df)

    # Plot opening and closing prices
    for col, color, marker, label in zip(['Open', 'Close'], ['b', 'r'], ['x', 'o'], ["Opening", "Closing"]):
        st.header(f"{label} Price Time Series of {idx_of_interest.upper()}")
        plt.figure(figsize=(10, 6))
        plt.plot(idx_df.index, idx_df[col], marker=marker, linestyle='-', color=color)
        plt.title(f'{idx_of_interest.upper()} Stock {label} Prices', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel(f'{label} Price (USD)', fontsize=12)
        plt.grid(True)
        st.pyplot(plt)

    # Plot opening and closing prices together
    st.header(f"Opening and Closing Price Time Series of {idx_of_interest.upper()}")
    plt.figure(figsize=(10, 6))
    plt.plot(idx_df.index, idx_df['Open'], linestyle='-', color='b', label='Opening Price')
    plt.plot(idx_df.index, idx_df['Close'], linestyle='-', color='r', label='Closing Price')
    plt.title(f'{idx_of_interest.upper()} Stock Prices', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price (USD)', fontsize=12)
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

    # Plot price difference
    st.header(f"Difference between Closing and Opening Price Time Series of {idx_of_interest.upper()}")
    plt.figure(figsize=(10, 6))
    plt.plot(idx_df.index, idx_df['Close'] - idx_df['Open'], linestyle='-', color='m')
    plt.title(f'{idx_of_interest.upper()} Price Difference', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price (USD)', fontsize=12)
    plt.grid(True)
    st.pyplot(plt)

    # Show statistics table
    description_dict = get_description()
    description_idx_df = description_dict[idx_of_interest]
    st.header(f"{idx_of_interest.upper()} Stock Data Statistics")
    st.dataframe(description_idx_df)

    # Set up EWMA with alpha
    alpha = st.number_input("Enter a smoothing parameter $\\alpha$ between 0 and 1:", min_value=0.01, max_value=1.0, value=0.3, step=0.01)
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
    st.pyplot(plt)

    # Set up EWMA with varying half-life
    half_life_short = st.number_input("Enter a short half-life in days", min_value=1, max_value=1095, value=30, step=1)
    alpha_hl_short = 1 - np.exp(-np.log(2) / half_life_short)
    half_life_long = st.number_input("Enter a longer half-life in days", min_value=half_life_short, max_value=1095, value=100, step=1)
    alpha_hl_long = 1 - np.exp(-np.log(2) / half_life_long)

    ewma_short = pd.Series(idx_df['Close']).ewm(alpha=alpha_hl_short, adjust=False).mean()
    ewma_long = pd.Series(idx_df['Close']).ewm(alpha=alpha_hl_long, adjust=False).mean()
    st.header(f"EWMA of Closing Price Time Series of {idx_of_interest.upper()} -- varying half-life")
    plt.figure(figsize=(12, 6))
    plt.plot(idx_df['Close'], label='Original Data', color='skyblue')
    plt.plot(ewma_short, label=f'Short half-life={half_life_short}', color='orange')
    plt.plot(ewma_long, label=f'Long half-life={half_life_long}', color='green')
    plt.title('EWMA with Varying Half-life', fontsize=16)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.legend()
    plt.grid()
    st.pyplot(plt)

    # Display candlestick chart
    st.header(f"Candlestick Chart Analysis for {idx_of_interest.upper()}")
    fig, ax = mpf.plot(idx_df, type='candle', style='charles', title=f"Candlestick Chart for {idx_of_interest.upper()}", ylabel='Price', volume=True, returnfig=True)
    st.pyplot(fig)

    st.write("**Naked Price Action** -- green candlesticks are **bullish** (increase in price), red candlesticks are **bearish** (decrease in price).")
