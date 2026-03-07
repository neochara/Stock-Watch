import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from constants import STOCK_IND_LIST

def render_comparison_tab(stocks_dfs_dict: dict):
    st.header("Indices comparisons (local CSV data)")

    most_recent_completed_year = 2025
    number_of_years = st.selectbox(
        "Select the past how many completed years you want to compare:",
        [1, 2, 3, 4, 5],
        index=2,
        key="multi_ticker_years_last_tab",
    )

    start_year = most_recent_completed_year - int(number_of_years) + 1
    start_date = pd.Timestamp(f"{start_year}-01-01")
    end_date = pd.Timestamp(f"{most_recent_completed_year}-12-31")
    st.caption(f"Window: {start_date.date()} to {end_date.date()}")

    available: list[str] = []
    skipped: list[str] = []
    close_series: dict[str, pd.Series] = {}

    for symbol in STOCK_IND_LIST:
        sym_key = symbol.lower()
        if sym_key not in stocks_dfs_dict:
            skipped.append(symbol)
            continue

        df_sym = stocks_dfs_dict[sym_key].copy()
        df_sym.index = pd.to_datetime(df_sym.index)

        if "Close" not in df_sym.columns:
            skipped.append(symbol)
            continue

        s = df_sym["Close"].dropna()
        s = s[(s.index >= start_date) & (s.index <= end_date)].dropna()

        if s.empty:
            skipped.append(symbol)
            continue

        close_series[symbol] = s
        available.append(symbol)

    if skipped:
        st.warning("Skipping tickers with missing data in this window: " + ", ".join(skipped))

    if not available:
        st.error("No tickers had valid Close data for this period from local CSVs.")
    else:
        # ---- Figure 1: cumulative growth (%) since first day in window (per ticker)
        fig_growth, ax_growth = plt.subplots(figsize=(12, 6))
        for symbol in available:
            s = close_series[symbol]
            base = float(s.iloc[0])
            growth_pct = ((s / base) - 1.0) * 100.0
            ax_growth.plot(growth_pct.index, growth_pct.values, label=symbol)

        ax_growth.set_title("Stock Growth (Close) — cumulative return % since first day in window", fontsize=16)
        ax_growth.set_xlabel("Date", fontsize=12)
        ax_growth.set_ylabel("Cumulative Returns (%)", fontsize=12)
        ax_growth.grid(True)
        ax_growth.legend()
        st.pyplot(fig_growth)

        # ---- Figure 2: covariance heatmap of log returns
        log_returns = pd.DataFrame()
        for symbol in available:
            s = close_series[symbol]
            log_returns[symbol] = np.log(s / s.shift(1))

        log_returns = log_returns.dropna(how="all")
        valid_cols = [c for c in available if c in log_returns.columns and not log_returns[c].dropna().empty]

        if len(valid_cols) < 2:
            st.info("Not enough valid tickers to compute a covariance matrix for this period.")
        else:
            cov = log_returns[valid_cols].dropna().cov()

            fig_cov, ax_cov = plt.subplots(figsize=(12, 10))
            sns.heatmap(1000 * cov, annot=True, cmap="cividis", fmt=".4f", linewidths=0.5, ax=ax_cov)
            ax_cov.set_title("Covariance Matrix of Log Returns (scaled by 10^3)", fontsize=16)
            st.pyplot(fig_cov)
