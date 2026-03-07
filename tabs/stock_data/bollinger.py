import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from utils.signals import bollinger_bands


def render_bollinger_tab(idx_df: pd.DataFrame, idx_of_interest: str):
    st.header(f"Bollinger Bands Visualization for {idx_of_interest.upper()}")

    window = st.number_input(
        "Rolling window size (days):", min_value=2, max_value=300, value=20, step=1
    )

    k_choices = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0]
    num_std = st.selectbox(
        "Number of standard deviations ($k$):", k_choices, index=k_choices.index(2.0)
    )

    price_col = st.selectbox("Price to use:", ["Close", "Open"], index=0)

    price_series = idx_df[price_col].dropna()
    if price_series.empty:
        st.error(f"No data available for {price_col} to compute Bollinger Bands.")
    else:
        # Use utils.bollinger_bands which returns [Price, Rolling Mean, Rolling Std, Upper Band, Lower Band]
        bb = bollinger_bands(price_series, window=int(window), num_std=float(num_std))

        fig, ax = plt.subplots(figsize=(10, 6))

        # Keep price as-is (prominent)
        ax.plot(bb.index, bb["Price"], label=f"{price_col} Price", color="blue")

        # Thin straight lines; remove upper/lower from legend
        ax.plot(
            bb.index,
            bb["Upper Band"],
            color="red",
            linestyle="-",
            linewidth=1,
            label="_nolegend_",
        )
        ax.plot(
            bb.index,
            bb["Lower Band"],
            color="green",
            linestyle="-",
            linewidth=1,
            label="_nolegend_",
        )
        ax.plot(
            bb.index,
            bb["Rolling Mean"],
            color="orange",
            linestyle="-",
            linewidth=1,
            label="Rolling Mean",
        )

        # Shade between bands (light blue)
        mask = bb["Upper Band"].notna() & bb["Lower Band"].notna()
        ax.fill_between(
            bb.index,
            bb["Lower Band"],
            bb["Upper Band"],
            where=mask,
            alpha=0.25,
            label="_nolegend_",
        )

        ax.set_title(
            f"{idx_of_interest.upper()} Bollinger Bands (window={int(window)}, k={num_std})",
            fontsize=16,
        )
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (USD)")
        ax.legend(loc="best")
        ax.grid(True)

        st.pyplot(fig)
