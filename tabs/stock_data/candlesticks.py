import streamlit as st
import mplfinance as mpf
import pandas as pd

def render_candlesticks_tab(idx_df: pd.DataFrame, idx_of_interest: str):
    st.header(f"Candlestick Chart Analysis on Closing Prices of {idx_of_interest.upper()}")
    
    # mpf.plot needs DateTimeIndex. Ensure it's correct.
    # idx_df was already cleaned in main, but let's be safe if it's passed around.
    
    fig, _ax = mpf.plot(
        idx_df,
        type="candle",
        style="charles",
        title=f"Candlestick Chart for {idx_of_interest.upper()}",
        ylabel="Price",
        volume=True,
        returnfig=True,
    )
    st.pyplot(fig)

    st.write(
        "**Naked Price Action** -- green candlesticks are **bullish** (increase in price), "
        "red candlesticks are **bearish** (decrease in price)."
    )
