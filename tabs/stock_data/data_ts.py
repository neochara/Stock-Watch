import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from utils import plot_streamlit

def render_data_ts_tab(idx_df: pd.DataFrame, idx_of_interest: str):
    st.header(f"{idx_of_interest.upper()} Stock Data")
    st.dataframe(idx_df)

    # Opening
    plot_streamlit(
        header=f"Opening Price Time Series of {idx_of_interest.upper()}",
        plot_title=f"{idx_of_interest.upper()} Stock Opening Prices",
        x_label="Date",
        y_label="Opening Price (USD)",
        grid="YES",
        legend="NO",
        dataframe=idx_df.index,
        data_plot=idx_df["Open"],
        label1=None,
        plot_marker="x",
        plot_linestyle="-",
        plot_color="b",
        dataframe2=None,
        data_plot2=None,
        label2=None,
        plot_marker2=None,
        plot_linestyle2=None,
        plot_color2=None,
    )

    # Closing
    plot_streamlit(
        header=f"Closing Price Time Series of {idx_of_interest.upper()}",
        plot_title=f"{idx_of_interest.upper()} Stock Closing Prices",
        x_label="Date",
        y_label="Closing Price (USD)",
        grid="YES",
        legend="NO",
        dataframe=idx_df.index,
        data_plot=idx_df["Close"],
        label1=None,
        plot_marker="o",
        plot_linestyle="-",
        plot_color="r",
        dataframe2=None,
        data_plot2=None,
        label2=None,
        plot_marker2=None,
        plot_linestyle2=None,
        plot_color2=None,
    )

    # Both Opening & Closing
    plot_streamlit(
        header=f"Opening and Closing Price Time Series of {idx_of_interest.upper()}",
        plot_title=f"{idx_of_interest.upper()} Stock Prices",
        x_label="Date",
        y_label="Closing Price (USD)",
        grid="YES",
        legend="NO",
        dataframe=idx_df.index,
        data_plot=idx_df["Open"],
        label1=None,
        plot_marker=None,
        plot_linestyle="-",
        plot_color="b",
        dataframe2=idx_df.index,
        data_plot2=idx_df["Close"],
        label2=None,
        plot_marker2=None,
        plot_linestyle2="-",
        plot_color2="r",
    )

    # Difference (Close - Open)
    plot_streamlit(
        header=f"Difference between Closing and Opening Price Time Series of {idx_of_interest.upper()}",
        plot_title=f"{idx_of_interest.upper()} Stock Close-Open Difference",
        x_label="Date",
        y_label="Price Difference (USD)",
        grid="YES",
        legend="NO",
        dataframe=idx_df.index,
        data_plot=idx_df["Close"] - idx_df["Open"],
        label1=None,
        plot_marker=None,
        plot_linestyle="-",
        plot_color="m",
        dataframe2=None,
        data_plot2=None,
        label2=None,
        plot_marker2=None,
        plot_linestyle2=None,
        plot_color2=None,
    )

    # ----------------------------
    # Year-over-year overlay (raw + normalized) for the SELECTED instrument
    # ----------------------------
    st.divider()
    st.subheader("Year-over-year Close comparison (selected instrument)")

    # Per your current setup (Jan 2026), 2025 is the most recent completed year.
    most_recent_completed_year = 2025

    X = st.selectbox(
        "Select number of years (always includes 2025):",
        [1, 2, 3, 4, 5],
        index=2,
        key="yoy_years_in_first_tab",
    )

    years_to_plot = list(range(most_recent_completed_year - int(X) + 1, most_recent_completed_year + 1))
    st.caption(f"Years shown: {years_to_plot}")

    idx_df_local = idx_df.copy()
    idx_df_local.index = pd.to_datetime(idx_df_local.index)

    if "Close" not in idx_df_local.columns:
        st.error("This dataset does not contain a 'Close' column.")
    else:
        close_all = idx_df_local["Close"].dropna()

        per_year_close: dict[int, pd.Series] = {}
        skipped_years: list[int] = []
        for y in years_to_plot:
            s = close_all[close_all.index.year == y]
            if s.empty:
                skipped_years.append(y)
            else:
                per_year_close[y] = s

        if skipped_years:
            st.warning(f"No Close data found for year(s): {skipped_years}. They will be skipped.")

        if not per_year_close:
            st.error("No year data available to plot for your selection.")
        else:
            # Align by trading-day number so years overlay cleanly
            max_len = max(len(s) for s in per_year_close.values())
            day_idx = np.arange(1, max_len + 1)

            comp_raw = pd.DataFrame(index=day_idx)
            comp_norm = pd.DataFrame(index=day_idx)

            for y, s in per_year_close.items():
                vals = s.values
                # Handle cases where some years have fewer days than max_len gracefully or just plot up to len
                # Here we reindex to 1..len(vals)
                comp_raw[y] = pd.Series(vals, index=np.arange(1, len(vals) + 1))

                base = float(s.iloc[0])  # first trading day of that year
                comp_norm[y] = pd.Series((vals / base) * 100.0, index=np.arange(1, len(vals) + 1))

            # Plot 1: Raw Close
            fig1, ax1 = plt.subplots(figsize=(12, 6))
            for y in sorted(comp_raw.columns):
                ax1.plot(comp_raw.index, comp_raw[y], label=str(y))
            ax1.set_title(f"{idx_of_interest.upper()} — Close (raw), overlayed by trading day")
            ax1.set_xlabel("Trading day of year (1 = first trading day)")
            ax1.set_ylabel("Close (USD)")
            ax1.grid(True)
            ax1.legend(title="Year")
            st.pyplot(fig1)

            # Plot 2: Normalized Close (each year starts at 100)
            fig2, ax2 = plt.subplots(figsize=(12, 6))
            for y in sorted(comp_norm.columns):
                ax2.plot(comp_norm.index, comp_norm[y], label=str(y))
            ax2.set_title(f"{idx_of_interest.upper()} — Close (normalized), each year starts at 100")
            ax2.set_xlabel("Trading day of year (1 = first trading day)")
            ax2.set_ylabel("Indexed Close (Year start = 100)")
            ax2.grid(True)
            ax2.legend(title="Year")
            st.pyplot(fig2)
