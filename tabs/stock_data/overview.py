import streamlit as st
from constants import START_DATE, END_DATE, STOCK_DATA_DICT

def render_overview_tab():
    st.header("Overview")

    st.markdown(
        f"""
- This app loads **locally stored CSV price data** (no live downloading in tabs).
- You choose a ticker from the dropdown at the top; all tabs update for that selection.
- Date range configured in `constants.py`: **{START_DATE}** to **{END_DATE}**.

**What each tab contains**
- **Data and Timeseries**: raw data table + Open/Close time series plots, plus a year-over-year Close overlay (raw + normalized to start at 100).
- **Statistics**: descriptive statistics summary table for the selected instrument.
- **EWMA**: exponentially weighted moving average plots (half-life and alpha controls) + crossing visualization.
- **Candlesticks**: candlestick chart (with volume).
- **Bollinger Bands**: Bollinger bands with adjustable window and $k$ (std dev multiplier).
- **Stock Comparisons**: multi-ticker comparison over the last $X$ completed years (growth % + covariance heatmap) using local CSVs.
"""
    )

    st.subheader("Available tickers (from constants.py)")

    # Build ticker->name list dynamically from STOCK_DATA_DICT (name -> ticker)
    pairs = sorted(((ticker, name) for name, ticker in STOCK_DATA_DICT.items()), key=lambda x: x[0])

    bullets = "\n".join([f"- **{ticker}** — {name}" for ticker, name in pairs])
    st.markdown(bullets)
