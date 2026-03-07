import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

def get_combined_data(stocks_dfs_dict):
    if not stocks_dfs_dict:
        return pd.DataFrame()
    combined_df = pd.DataFrame()
    for ticker, df in stocks_dfs_dict.items():
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
        combined_df[ticker.upper()] = df['Close']
    return combined_df.dropna()

def render_risk_tab(stocks_dfs_dict):
    st.header("Risk & Correlation Analysis")
    st.caption("Deep dive into downside risk and asset relationships.")

    if not stocks_dfs_dict:
        st.warning("No data available.")
        return

    combined_close = get_combined_data(stocks_dfs_dict)
    returns = combined_close.pct_change().dropna()
    
    # --- 1. Value at Risk (VaR) & CVaR ---
    st.subheader("1. Value at Risk (VaR) & Conditional VaR (CVaR)")
    
    with st.expander("Definitions", expanded=True):
        st.markdown(r"""
        *   **Value at Risk (VaR, 95%)**: The maximum loss expected over a day with 95% confidence. 
            If VaR is -2.5%, it means there is a 5% chance your portfolio drops *more* than 2.5% in a day.
        *   **Conditional VaR (CVaR / Expected Shortfall)**: The average loss *given* that the loss has exceeded the VaR threshold. 
            It answers: "If things get really bad (worst 5%), how bad is the average?"
        """)

    # Weights Selection (Simplified: Equal Weighted for this view to show intrinsic asset risk)
    st.info("Metrics below allow you to view risk for individual assets or an Equal-Weighted Portfolio.")
    
    tickers = returns.columns.tolist()
    
    # Calculate VaR/CVaR for each stock
    confidence_level = 0.95
    var_95 = returns.quantile(1 - confidence_level)
    cvar_95 = returns[returns <= var_95].mean()
    
    risk_df = pd.DataFrame({
        "VaR (95%)": var_95,
        "CVaR (95%)": cvar_95
    })
    
    # Display Risk Metrics
    st.dataframe(risk_df.style.format("{:.2%}"), use_container_width=True)
    
    # Visualization of Return Distribution for a selected asset
    selected_asset = st.selectbox("View Return Distribution for:", tickers)
    asset_rets = returns[selected_asset]
    asset_var = var_95[selected_asset]
    asset_cvar = cvar_95[selected_asset]
    
    fig_hist, ax_hist = plt.subplots(figsize=(10, 5))
    sns.histplot(asset_rets, bins=50, kde=True, ax=ax_hist, color='skyblue')
    ax_hist.axvline(asset_var, color='red', linestyle='--', label=f'VaR (95%): {asset_var:.2%}')
    ax_hist.axvline(asset_cvar, color='darkred', linestyle='-', label=f'CVaR (95%): {asset_cvar:.2%}')
    ax_hist.legend()
    ax_hist.set_title(f"Daily Return Distribution: {selected_asset}")
    st.pyplot(fig_hist)

    st.divider()

    # --- 2. Correlation Dendrogram ---
    st.subheader("2. Correlation Dendrogram")
    
    with st.expander("Why use a Dendrogram?"):
        st.markdown("""
        **Hierarchical Clustering** groups stocks that behave similarly. 
        - Stocks connected by short branches are highly correlated (move together).
        - To diversify effectively, you want to pick stocks from *different* main branches.
        """)

    corr_matrix = returns.corr()
    
    # Linkage Matrix
    # We use 'ward' linkage which minimizes variance within clusters
    # Distance metric = 1 - correlation (since high corr = low distance)
    dist = linkage(1 - corr_matrix, method='ward')
    
    fig_dendro, ax_dendro = plt.subplots(figsize=(10, 6))
    dendrogram(dist, labels=tickers, leaf_rotation=90, ax=ax_dendro)
    ax_dendro.set_title("Hierarchical Clustering of Assets")
    ax_dendro.set_ylabel("Distance (Dissimilarity)")
    st.pyplot(fig_dendro)
    
    # Heatmap for reference
    if st.checkbox("Show Correlation Heatmap"):
        fig_corr, ax_corr = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', ax=ax_corr)
        st.pyplot(fig_corr)
