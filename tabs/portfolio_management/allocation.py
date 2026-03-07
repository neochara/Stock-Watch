import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_combined_data(stocks_dfs_dict):
    """
    Reuse helper to get combined close prices. A bit repetitive, 
    in a real app we might move this to a utils file.
    """
    if not stocks_dfs_dict:
        return pd.DataFrame()
    
    combined_df = pd.DataFrame()
    for ticker, df in stocks_dfs_dict.items():
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
        combined_df[ticker.upper()] = df['Close']
        
    return combined_df.dropna()

def render_allocation_tab(stocks_dfs_dict):
    st.header("Manual Asset Allocation")
    st.caption("Experiment with different portfolio weights to see how they impact Risk and Return.")

    if not stocks_dfs_dict:
        st.warning("No data available.")
        return
        
    combined_close = get_combined_data(stocks_dfs_dict)
    all_tickers = combined_close.columns.tolist()
    
    # --- 1. Asset Selection ---
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("1. Select Assets")
        selected_tickers = st.multiselect("Assets", all_tickers, default=all_tickers[:3], key="alloc_assets")
        
        if not selected_tickers:
            st.info("Select assets to begin.")
            return
            
        st.subheader("2. Assign Weights")
        st.caption("Weights will be normalized to sum to 100%.")
        
        raw_weights = {}
        for ticker in selected_tickers:
            raw_weights[ticker] = st.slider(f"{ticker} Weight", 0, 100, 100 // len(selected_tickers), key=f"alloc_weight_{ticker}")
            
        # Normalize
        total_raw = sum(raw_weights.values())
        if total_raw == 0:
            st.warning("Total weight cannot be zero.")
            return
            
        final_weights = {k: v/total_raw for k, v in raw_weights.items()}
        
        st.markdown("---")
        st.markdown("**Normalized Weights:**")
        weights_df = pd.DataFrame.from_dict(final_weights, orient='index', columns=['Weight'])
        st.dataframe(weights_df.style.format("{:.2%}"))
        
    with col2:
        st.subheader("3. Portfolio Analytics")
        
        # Calculate Metrics
        price_data = combined_close[selected_tickers]
        returns_pct = price_data.pct_change().dropna()
        
        weights_vec = np.array([final_weights[t] for t in selected_tickers])
        
        # Portfolio Expected Return (Annualized)
        port_ret = np.dot(weights_vec, returns_pct.mean() * 252)
        
        # Portfolio Volatility (Annualized)
        cov_matrix = returns_pct.cov() * 252
        port_vol = np.sqrt(np.dot(weights_vec.T, np.dot(cov_matrix, weights_vec)))
        
        # Sharpe (Arbitrary risk free for view)
        rf = 0.02
        sharpe = (port_ret - rf) / port_vol if port_vol > 0 else 0
        
        # Metrics Display
        m1, m2, m3 = st.columns(3)
        m1.metric("Exp. Return", f"{port_ret:.2%}")
        m2.metric("Volatility", f"{port_vol:.2%}")
        m3.metric("Sharpe Ratio", f"{sharpe:.2f}")
        
        # Visuals
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(weights_vec, labels=selected_tickers, autopct='%1.1f%%', startangle=90, normalize=True)
        ax.set_title("Current Allocation")
        st.pyplot(fig)
        
        # Contextual Plot (Risk-Return Landscape)
        st.markdown("#### Risk-Return Context")
        # Generate some random portfolios for context
        n_sim = 500
        sim_vol = []
        sim_ret = []
        
        mu = returns_pct.mean() * 252
        cov = returns_pct.cov() * 252
        
        for _ in range(n_sim):
            w = np.random.random(len(selected_tickers))
            w /= w.sum()
            sim_ret.append(np.dot(w, mu))
            sim_vol.append(np.sqrt(np.dot(w.T, np.dot(cov, w))))
            
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.scatter(sim_vol, sim_ret, color='gray', alpha=0.3, s=10, label='Possible Allocations')
        ax2.scatter(port_vol, port_ret, color='blue', s=200, marker='*', label='Your Portfolio')
        ax2.set_xlabel("Volatility (Risk)")
        ax2.set_ylabel("Return")
        ax2.set_title("Your Portfolio vs Possibilities")
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        st.pyplot(fig2)
