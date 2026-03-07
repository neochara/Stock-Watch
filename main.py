import streamlit as st
import seaborn as sns

from constants import END_DATE, START_DATE, STOCK_IND_LIST
from data_analysis import get_clean_data
from tabs.stock_data.overview import render_overview_tab
from tabs.stock_data.terminology import render_terminology_tab
from tabs.stock_data.data_ts import render_data_ts_tab
from tabs.stock_data.stats import render_stats_tab
from tabs.stock_data.ewma import render_ewma_tab
from tabs.stock_data.candlesticks import render_candlesticks_tab
from tabs.stock_data.bollinger import render_bollinger_tab
from tabs.stock_data.comparison import render_comparison_tab
from tabs.portfolio_management.portfolio_main import render_portfolio_tab
from tabs.quant_basics.quant_main import render_quant_basics_tab

def main():
    sns.set_style("whitegrid")

    st.title("Stock Watch :sunglasses:")
    st.write(f"The time period we are looking at is {START_DATE} to {END_DATE}")

    # Top-level Tabs
    Top_StockData_Tab, Top_QuantBasics_Tab, Top_Portfolio_Tab = st.tabs(
        ["Stock Data", "Quant Finance 'Basics'", "Portfolio Management"]
    )
    with Top_StockData_Tab:
        # Sidebar or Top-level selection (Moved inside this tab)
        idx_of_interest = st.selectbox("Select a stock index:", STOCK_IND_LIST)
        st.write(f"Let us summarize the {idx_of_interest} stock")
        idx_of_interest = idx_of_interest.lower()

        # Load Data (Moved inside this tab so it runs only when needed or just logically placed)
        # Ideally, we cache this, but for now we follow existing pattern
        stocks_dfs_dict = get_clean_data()

        if idx_of_interest in stocks_dfs_dict:
            idx_df = stocks_dfs_dict[idx_of_interest]
        else:
            st.error(f"Data for {idx_of_interest} not found.")
            idx_df = None

        # Subtabs for Stock Data
        (
            Overview_tab,
            Terminology_tab,
            Data_TS_tab,
            Stats_tab,
            EWMA_tab,
            Candlesticks_tab,
            Bollinger_tab,
            Stocks_comp_tab,
        ) = st.tabs(
            [
                "Overview",
                "Terminology",
                "Data and Timeseries",
                "Statistics",
                "EWMA",
                "Candlesticks",
                "Bollinger Bands",
                "Stock Comparisons",
            ]
        )

        with Overview_tab:
            render_overview_tab()

        with Terminology_tab:
            render_terminology_tab()

        if idx_df is not None:
            with Data_TS_tab:
                render_data_ts_tab(idx_df, idx_of_interest)

            with Stats_tab:
                render_stats_tab(idx_of_interest)

            with EWMA_tab:
                render_ewma_tab(idx_df, idx_of_interest)

            with Candlesticks_tab:
                render_candlesticks_tab(idx_df, idx_of_interest)

            with Bollinger_tab:
                render_bollinger_tab(idx_df, idx_of_interest)

    # Comparison tab generally loads all data, so we pass the dict
    with Stocks_comp_tab:
        render_comparison_tab(stocks_dfs_dict)

    with Top_QuantBasics_Tab:
        render_quant_basics_tab()

    with Top_Portfolio_Tab:
        # Ensure data is loaded if user goes straight to Portfolio Tab (though usually Stock Data loads first)
        if "stocks_dfs_dict" not in locals():
            stocks_dfs_dict = get_clean_data()

        render_portfolio_tab(stocks_dfs_dict)


if __name__ == "__main__":
    main()
