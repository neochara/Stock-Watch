import streamlit as st
import pandas as pd
import numpy as np
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

def render_forecasting_tab(stocks_dfs_dict):
    st.header("Monte Carlo Forecasting")
    st.caption("Project future portfolio performance using stochastic simulations.")
    
    if not stocks_dfs_dict:
        st.warning("No data available.")
        return

    combined_close = get_combined_data(stocks_dfs_dict)
    returns = combined_close.pct_change().dropna()
    tickers = combined_close.columns.tolist()

    with st.expander("Methodology: Geometric Brownian Motion", expanded=True):
        st.markdown(r"""
        **Monte Carlo Simulation** generates thousands of possible price paths based on historical characteristics.
        
        We use **Geometric Brownian Motion (GBM)**, a standard model for stock price dynamics:
        $$ \Delta S = S \cdot (\mu \Delta t + \sigma \epsilon \sqrt{\Delta t}) $$
        
        Where:
        - $\mu$: Expected daily return (Drift)
        - $\sigma$: Daily volatility (Shock)
        - $\epsilon$: Random Normal Variable (Z-score)
        """)

    # --- Settings ---
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Simulation Settings")
        selected_tickers = st.multiselect("Assets", tickers, default=tickers[:3], key="forecast_assets")
        
        n_days = st.slider("Forecast Horizon (Days)", 30, 365, 252, key="forecast_days")
        n_sims = st.slider("Number of Simulations", 100, 2000, 500, key="forecast_sims")
        start_val = st.number_input("Initial Investment ($)", 1000, 1000000, 10000, 1000, key="forecast_start")
        
        st.subheader("Weights")
        # Simplified Equal Weight for simulation or custom? 
        # Let's do equal weight for simplicity of UI, or basic sliders
        # To keep it seamless, let's just assume Equal Weights for the selected assets for now to avoid re-implementing the full allocation UI here.
        st.info("Simulating an **Equal-Weighted** portfolio of selected assets.")
        weights = np.array([1/len(selected_tickers)] * len(selected_tickers))

    if not selected_tickers:
        return

    # --- Simulation ---
    with col2:
        # Prepare Stats
        sel_returns = returns[selected_tickers]
        mean_returns = sel_returns.mean().values
        cov_matrix = sel_returns.cov().values
        
        # Portfolio Drift and Volatility (Daily)
        port_mu = np.dot(weights, mean_returns)
        port_sigma = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        
        # Run Simulation
        # shape: (n_days, n_sims)
        # Random shocks
        daily_shocks = np.random.normal(0, 1, (n_days, n_sims))
        
        # Calculate daily percentage changes for each path
        # drift term - 0.5 * sigma^2 is the geometric correction term
        daily_drift = port_mu - 0.5 * port_sigma**2
        daily_change = np.exp(daily_drift + port_sigma * daily_shocks)
        
        # Accumulate path
        price_paths = np.zeros((n_days + 1, n_sims))
        price_paths[0] = start_val
        for t in range(1, n_days + 1):
            price_paths[t] = price_paths[t-1] * daily_change[t-1]
            
        # Analysis
        final_values = price_paths[-1]
        mean_final = np.mean(final_values)
        median_final = np.median(final_values)
        p10 = np.percentile(final_values, 10)
        p90 = np.percentile(final_values, 90)
        
        # Plotting
        st.subheader("Projected Portfolio Value")
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot first 50 paths
        ax.plot(price_paths[:, :50], color='gray', alpha=0.1)
        
        # Plot Mean path
        ax.plot(np.mean(price_paths, axis=1), color='blue', linewidth=2, label='Mean Path')
        
        # Fan Chart areas
        days = np.arange(n_days + 1)
        pct_10 = np.percentile(price_paths, 10, axis=1)
        pct_50 = np.percentile(price_paths, 50, axis=1)
        pct_90 = np.percentile(price_paths, 90, axis=1)
        
        ax.fill_between(days, pct_10, pct_90, color='blue', alpha=0.1, label='10th-90th Percentile')
        
        ax.set_title(f"Monte Carlo Simulation ({n_days} Days)")
        ax.set_ylabel("Portfolio Value ($)")
        ax.set_xlabel("Trading Days")
        ax.legend()
        st.pyplot(fig)
        
        # Stats
        m1, m2, m3 = st.columns(3)
        m1.metric("Exp. Final Value", f"${mean_final:,.0f}")
        m2.metric("Median Final", f"${median_final:,.0f}")
        m3.metric("90% Conf. Range", f"${p10:,.0f} - ${p90:,.0f}")
