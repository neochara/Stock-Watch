import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def get_combined_data(stocks_dfs_dict):
    if not stocks_dfs_dict:
        return pd.DataFrame()
    combined_df = pd.DataFrame()
    for ticker, df in stocks_dfs_dict.items():
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
        combined_df[ticker.upper()] = df['Close']
    return combined_df.dropna()

def render_backtest_tab(stocks_dfs_dict):
    st.header("Benchmark Comparison (Backtest)")
    st.caption("Compare your portfolio's historical performance against the S&P 500 (SPY).")
    
    if not stocks_dfs_dict:
        st.warning("No data available.")
        return

    combined_close = get_combined_data(stocks_dfs_dict)
    tickers = combined_close.columns.tolist()

    # --- 1. Portfolio Construction ---
    st.subheader("1. Construct Portfolio")
    selected_tickers = st.multiselect("Select Assets", tickers, default=tickers[:3], key="backtest_select")
    
    if not selected_tickers:
        return
        
    # Simple Equal Weights for now (can expand to custom later)
    # The user mainly wants to see the comparison feature
    st.info("Backtesting an **Equal-Weighted** portfolio of selected assets.")
    
    portfolio_close = combined_close[selected_tickers]
    portfolio_chg = portfolio_close.pct_change().dropna()
    
    # Calculate Component Portfolio Return
    weights = [1/len(selected_tickers)] * len(selected_tickers)
    # Returns * Weights -> Sum across columns
    portfolio_daily_ret = portfolio_chg.dot(weights)
    
    # Cumulative Return
    portfolio_cum_ret = (1 + portfolio_daily_ret).cumprod()

    # --- 2. Fetch Benchmark (SPY) ---
    st.subheader("2. Market Comparison")
    
    # Determine date range from existing data
    start_date = portfolio_chg.index.min()
    end_date = portfolio_chg.index.max()
    
    @st.cache_data
    def get_benchmark(start, end):
        spy = yf.download("SPY", start=start, end=end, auto_adjust=True, progress=False)
        return spy['Close']

    with st.spinner("Fetching S&P 500 (SPY) data..."):
        try:
            spy_data = get_benchmark(start_date, end_date)
            
            if spy_data.empty:
                st.warning("Could not fetch SPY data for this period.")
                return

            # Align indices
            spy_ret = spy_data.pct_change().dropna()
            
            # Reindex to match portfolio dates roughly (intersection)
            common_idx = portfolio_daily_ret.index.intersection(spy_ret.index)
            
            if common_idx.empty:
                st.warning("No overlapping dates found between your portfolio and the benchmark (SPY).")
                return
            
            my_port = portfolio_daily_ret.loc[common_idx]
            spy_port = spy_ret.loc[common_idx]
            
            my_cum = (1 + my_port).cumprod()
            spy_cum = (1 + spy_port).cumprod()
            
            if my_cum.empty or spy_cum.empty:
                 st.warning("Insufficient data to calculate cumulative returns.")
                 return

            # --- Metrics ---
            my_total_ret = my_cum.iloc[-1] - 1
            spy_total_ret = spy_cum.iloc[-1] - 1
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Your Portfolio Return", f"{my_total_ret:.2%}")
            with col2:
                st.metric("S&P 500 (SPY) Return", f"{spy_total_ret:.2%}", delta=f"{(my_total_ret - spy_total_ret):.2%}")
            
            # --- Plot ---
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(my_cum.index, my_cum, label='Your Portfolio', color='blue')
            ax.plot(spy_cum.index, spy_cum, label='S&P 500 (SPY)', color='gray', linestyle='--')
            
            ax.set_title("Performance vs Benchmark (Normalized)")
            ax.set_ylabel("Growth of $1")
            ax.legend()
            st.pyplot(fig)
            
            st.markdown("""
            **Analysis**:
            - If your line is **above** the gray line, you beat the market over this period.
            - If your line is **below**, the passive index fund outperformed.
            """)
            
        except Exception as e:
            st.error(f"Could not load benchmark data: {e}")
