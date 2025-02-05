import streamlit as st
from data_analysis import get_clean_data, get_description, get_nl_summary
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mplfinance as mpf
from datetime import datetime
from utils import plot_streamlit
from constants import STOCK_DATA_DICT, STOCK_IND_LIST, START_DATE, END_DATE
import random
import yfinance as yf
import datetime as dt
import seaborn as sns
sns.set_style('whitegrid')

st.title('Stock Watch :sunglasses:')

idx_of_interest = st.selectbox("Select a stock index:",
                                STOCK_IND_LIST)
                                # random.choice(list(STOCK_DATA_DICT.values()))

st.write(f"Let us summarize the {idx_of_interest} stock")
idx_of_interest = idx_of_interest.lower()

st.write(f"The time period we are looking at is {START_DATE} to {END_DATE}")

stocks_dfs_dict = get_clean_data()

idx_df = stocks_dfs_dict[idx_of_interest]
#company_of_interest = idx_df['copmany_name']

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Data and Timeseries", "Statistics", "EWMA", "Candlesticks", "Stock Comparisons"])

# - - - Display data to streamlit - - -
with tab1: 
    st.header(f"{idx_of_interest.upper()} Data and Timeseries")
    st.dataframe(idx_df)

    # - - - Plots of opening and closing price - - -
    # Plot of opening price
    plot_streamlit(header = f"Opening Price Time Series of {idx_of_interest.upper()}",
                plot_title = f"{idx_of_interest.upper()} Stock Opening Prices",
                x_label = 'Date', y_label = 'Opening Price (USD)', grid='YES', legend = 'NO',
                dataframe = idx_df.index, data_plot = idx_df['Open'],
                plot_marker='x', plot_linestyle='-', plot_color='b',
                dataframe2=None, data_plot2=None, plot_marker2=None, plot_linestyle2=None, plot_color2=None, label1=None, label2=None)

    # Plot of closing price
    plot_streamlit(header = f"Closing Price Time Series of {idx_of_interest.upper()}",
                plot_title = f"{idx_of_interest.upper()} Stock Closing Prices",
                x_label = 'Date', y_label = 'Closing Price (USD)', grid='YES', legend = 'NO',
                dataframe = idx_df.index, data_plot = idx_df['Close'],
                plot_marker='o', plot_linestyle='-', plot_color='r',
                dataframe2=None, data_plot2=None, plot_marker2=None, plot_linestyle2=None, plot_color2=None, label1=None, label2=None)

    # Plot both opening and closing price
    plot_streamlit(f"Opening and Closing Price Time Series of {idx_of_interest.upper()}",
                plot_title = f'{idx_of_interest.upper()} Stock Prices',
                x_label = 'Date', y_label = 'Closing Price (USD)', grid='YES', legend = 'NO',
                dataframe = idx_df.index, data_plot = idx_df['Open'],
                plot_marker = None, plot_linestyle='-', plot_color='b',
                dataframe2 = idx_df.index, data_plot2 = idx_df['Close'],
                plot_marker2 = None, plot_linestyle2 = '-', plot_color2='r', label1=None, label2=None)

    # Plot difference between opening and closing price
    plot_streamlit(header = f"Difference between Closing and Opening Price Time Series of {idx_of_interest.upper()}",
                plot_title = f"{idx_of_interest.upper()} Stock Closing Prices",
                x_label = 'Date', y_label = 'Closing Price (USD)', grid='YES', legend = 'NO',
                dataframe = idx_df.index, data_plot = idx_df['Close']-idx_df['Open'],
                plot_marker = None, plot_linestyle='-', plot_color='m',
                dataframe2=None, data_plot2=None, plot_marker2=None, plot_linestyle2=None, plot_color2=None, label1=None, label2=None)

# - - - Plot timeseries description table - - -
with tab2:
    description_dict = get_description()
    description_idx_df = description_dict[idx_of_interest]

    st.header(f"{idx_of_interest.upper()} Stock Data Statistics")
    st.dataframe(description_idx_df)

# - - - Display Text Summary - - -
# response_dict = get_nl_summary()
# response_idx = response_dict[idx_of_interest]

# st.header(f"{idx_of_interest.upper()} Stock Summary")
# st.text(response_idx)

# - - - Plot EWMA on Closing Prices with varying half-life - - -
with tab3:
    half_life_short = st.number_input("Enter a half-life of your EWMA in days, up to 3 years",
                            min_value=1, max_value=1095, value=30, step=1)
    alpha_hl_short = 1 - np.exp(-np.log(2)/half_life_short)
    st.write(f"For half-life = {half_life_short}, we get $\\alpha$ = {alpha_hl_short}")

    half_life_long = st.number_input("Enter a longer half-life of your EWMA in days, up to 3 years",
                            min_value=half_life_short, max_value=1095, value=100, step=1)
    alpha_hl_long = 1 - np.exp(-np.log(2)/half_life_long)
    st.write(f"For the longer half-life = {half_life_long}, we get $\\alpha$ = {alpha_hl_long}")

    ewma_closing_hl_short = idx_df['Close'].ewm(halflife=half_life_short, adjust=False).mean()
    ewma_closing_hl_long = idx_df['Close'].ewm(halflife=half_life_long, adjust=False).mean()

    st.header(f"EWMA of Closing Price Time Series of {idx_of_interest.upper()} -- varying half-life")
    plt.figure(figsize=(12, 6))
    plt.plot(idx_df['Close'], label='Original Data', color='skyblue')
    plt.plot(ewma_closing_hl_short, label=f'short half-life={half_life_short}', color='orange')
    plt.plot(ewma_closing_hl_long, label=f'long half-life={half_life_long}', color='green')
    plt.title('Exponentially Weighted Moving Average (EWMA) -- varying half-life', fontsize=16)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.legend()
    plt.grid()
    plt.show()
    st.pyplot(plt)

    # - - - Plot EWMA on Closing Prices - - -
    alpha = st.number_input("Enter a smoothing parameter $\\alpha$ between 0 and 1:",
                            min_value=0.01, max_value=1.0, value=0.05, step=0.01)

    ewma_instrument_closing = pd.Series(idx_df['Close']).ewm(alpha=alpha, adjust=False).mean()

    plot_streamlit(header = f"EWMA of Closing Price Time Series of {idx_of_interest.upper()}",
                plot_title = 'Exponentially Weighted Moving Average (EWMA), w/ choice of $\\alpha$',
                x_label = 'Time', y_label = 'Value', grid='NO', legend = 'YES',
                dataframe = idx_df.index, data_plot = idx_df['Close'], plot_color='skyblue',
                label1='Original Data', plot_marker = None, plot_linestyle='-',
                dataframe2 = idx_df.index, data_plot2=ewma_instrument_closing,
                label2=f'EWMA (alpha={alpha})', plot_marker2=None, plot_linestyle2=None, plot_color2='orange')

    # st.header(f"EWMA of Closing Price Time Series of {idx_of_interest.upper()}")
    # plt.figure(figsize=(12, 6))
    # plt.plot(idx_df['Close'], label='Original Data', color='skyblue')
    # plt.plot(ewma_instrument_closing, label=f'EWMA (alpha={alpha})', color='orange')
    # plt.title('Exponentially Weighted Moving Average (EWMA)', fontsize=16)
    # plt.xlabel('Time', fontsize=12)
    # plt.ylabel('Value', fontsize=12)
    # plt.legend()
    # plt.grid()
    # plt.show()
    # st.pyplot(plt)

    # - - - - - - - - - - - - - - - - - -
    # Create a figure for plotting
    st.header(f"EWMA of Closing Price Time Series of {idx_of_interest.upper()} -- varying half-life w/ crossings")
    plt.figure(figsize=(12, 6))
    plt.plot(idx_df['Close'], label='Original Data', color='skyblue')
    plt.plot(ewma_closing_hl_short, label=f'short half-life={half_life_short}', color='orange')
    plt.plot(ewma_closing_hl_long, label=f'long half-life={half_life_long}', color='magenta')

    # Create a mask for filling colors based on crossovers
    cross_above = ewma_closing_hl_short > ewma_closing_hl_long
    cross_below = ewma_closing_hl_short < ewma_closing_hl_long

    # Fill between the close price and the EWMA based on crossing conditions
    plt.fill_between(idx_df.index, idx_df['Close'], where=cross_above, color='green', alpha=0.5, label='long 1/2-life > short 1/2-life', interpolate=True)
    plt.fill_between(idx_df.index, idx_df['Close'], where=cross_below, color='red', alpha=0.5, label='short 1/2-life > long 1/2-life', interpolate=True)

    plt.title('Exponentially Weighted Moving Average (EWMA) -- varying half-life w/ crossings', fontsize=16)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.legend()
    plt.grid()
    plt.show()
    st.pyplot(plt)
    # - - - - - - - - - - - - - - - - - -

# - - - Plot Candlestick Chart on Closing Prices - - -
with tab4:
    st.header(f"Candlestick Chart Analysis on Closing Prices of {idx_of_interest.upper()}")
    fig, ax = mpf.plot(idx_df, type='candle', style='charles', 
                        title=f"Candlestick Chart for {idx_of_interest.upper()}",
                        ylabel='Price', volume=True, returnfig=True)
    st.pyplot(fig)

    st.write("**Naked Price Action** -- green candlesticks are **bullish** (increase in price), red candlesticks are **bearish** (increase in price).")

# - - - Comparisons - - -
with tab5:
    st.header(f"Indices Comparisons, over the past years")
    number_of_years = st.selectbox("Select the past how many years you want to compare",
                                list(range(1, 6)))

    start_date_comparison = END_DATE - dt.timedelta(365*number_of_years) 

    # Download stock data for each symbol
    stock_data = yf.download(STOCK_IND_LIST, start=start_date_comparison, end=END_DATE)

    # Calculate log returns for each stock symbol and add them to the DataFrame
    log_returns = pd.DataFrame()
    for symbol in STOCK_IND_LIST:
        log_returns[symbol] = np.log(stock_data['Close'][symbol]/stock_data['Close'][symbol].shift(1))

    log_returns = log_returns.dropna()

    returns = (np.exp(log_returns)-1)

    plt.figure(figsize=(12, 6))

    for symbol in STOCK_IND_LIST:
        plt.plot(stock_data.index, ((stock_data['Close'][symbol]/stock_data['Close'][symbol].iloc[0])-1)*100, label=symbol)
    plt.legend()
    plt.title('Stock Growth', fontsize = 20)
    plt.ylabel('Cumulative Returns in %', fontsize = 15)
    st.pyplot(plt)

    # Calculate the covariance matrix
    covariance_matrix = ((log_returns).cov())

    # Create a heatmap to visualize the covariance matrix
    plt.figure(figsize=(15, 15))
    sns.heatmap(1000*covariance_matrix, annot=True, cmap='cividis', fmt='.4f', linewidths=.5)  # multiply by 1000, to reove decimals
    plt.title('Covariance Matrix of Log Returns (scaled by 10^3)', fontsize=20)
    plt.show()
    st.pyplot(plt)
