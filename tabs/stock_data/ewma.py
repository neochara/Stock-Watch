import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from utils import plot_streamlit

def render_ewma_tab(idx_df: pd.DataFrame, idx_of_interest: str):
    half_life_short = st.number_input(
        "Enter a half-life of your EWMA in days, up to 3 years",
        min_value=1,
        max_value=1095,
        value=30,
        step=1,
    )
    alpha_hl_short = 1 - np.exp(-np.log(2) / half_life_short)
    st.write(f"For half-life = {half_life_short}, we get $\\alpha$ = {alpha_hl_short}")

    half_life_long = st.number_input(
        "Enter a longer half-life of your EWMA in days, up to 3 years",
        min_value=int(half_life_short),
        max_value=1095,
        value=100,
        step=1,
    )
    alpha_hl_long = 1 - np.exp(-np.log(2) / half_life_long)
    st.write(f"For the longer half-life = {half_life_long}, we get $\\alpha$ = {alpha_hl_long}")

    ewma_closing_hl_short = idx_df["Close"].ewm(halflife=half_life_short, adjust=False).mean()
    ewma_closing_hl_long = idx_df["Close"].ewm(halflife=half_life_long, adjust=False).mean()

    st.header(f"EWMA of Closing Price Time Series of {idx_of_interest.upper()} -- varying half-life")
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(idx_df.index, idx_df["Close"], label="Original Data", color="skyblue")
    ax.plot(idx_df.index, ewma_closing_hl_short, label=f"short half-life={half_life_short}", color="orange")
    ax.plot(idx_df.index, ewma_closing_hl_long, label=f"long half-life={half_life_long}", color="green")
    ax.set_title("Exponentially Weighted Moving Average (EWMA) -- varying half-life", fontsize=16)
    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel("Value", fontsize=12)
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    alpha = st.number_input(
        "Enter a smoothing parameter $\\alpha$ between 0 and 1:",
        min_value=0.01,
        max_value=1.0,
        value=0.05,
        step=0.01,
    )
    ewma_instrument_closing = pd.Series(idx_df["Close"]).ewm(alpha=alpha, adjust=False).mean()

    plot_streamlit(
        header=f"EWMA of Closing Price Time Series of {idx_of_interest.upper()}",
        plot_title="Exponentially Weighted Moving Average (EWMA), w/ choice of $\\alpha$",
        x_label="Time",
        y_label="Value",
        grid="NO",
        legend="YES",
        dataframe=idx_df.index,
        data_plot=idx_df["Close"],
        label1="Original Data",
        plot_marker=None,
        plot_linestyle="-",
        plot_color="skyblue",
        dataframe2=idx_df.index,
        data_plot2=ewma_instrument_closing,
        label2=f"EWMA (alpha={alpha})",
        plot_marker2=None,
        plot_linestyle2=None,
        plot_color2="orange",
    )

    st.header(f"EWMA of Closing Price Time Series of {idx_of_interest.upper()} -- varying half-life w/ crossings")
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    ax2.plot(idx_df.index, idx_df["Close"], label="Original Data", color="skyblue")
    ax2.plot(idx_df.index, ewma_closing_hl_short, label=f"short half-life={half_life_short}", color="orange")
    ax2.plot(idx_df.index, ewma_closing_hl_long, label=f"long half-life={half_life_long}", color="magenta")

    cross_above = ewma_closing_hl_short > ewma_closing_hl_long
    cross_below = ewma_closing_hl_short < ewma_closing_hl_long

    ax2.fill_between(
        idx_df.index,
        idx_df["Close"],
        where=cross_above,
        color="green",
        alpha=0.5,
        label="long 1/2-life > short 1/2-life",
        interpolate=True,
    )
    ax2.fill_between(
        idx_df.index,
        idx_df["Close"],
        where=cross_below,
        color="red",
        alpha=0.5,
        label="short 1/2-life > long 1/2-life",
        interpolate=True,
    )

    ax2.set_title("Exponentially Weighted Moving Average (EWMA) -- varying half-life w/ crossings", fontsize=16)
    ax2.set_xlabel("Time", fontsize=12)
    ax2.set_ylabel("Value", fontsize=12)
    ax2.legend()
    ax2.grid(True)
    st.pyplot(fig2)
