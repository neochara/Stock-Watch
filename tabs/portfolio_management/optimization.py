import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.optimize import minimize

def get_combined_data(stocks_dfs_dict):
    """
    Combines individual stock DataFrames from the dictionary into a single DataFrame of Close prices.
    stocks_dfs_dict: { 'ticker': df_with_Close_col, ... }
    """
    if not stocks_dfs_dict:
        return pd.DataFrame()
    
    # We want a single DF where columns are Tickers and values are Close prices
    combined_df = pd.DataFrame()
    
    for ticker, df in stocks_dfs_dict.items():
        # Ensure index is datetime
        if not isinstance(df.index, pd.DatetimeIndex):
            df.index = pd.to_datetime(df.index)
            
        combined_df[ticker.upper()] = df['Close']
        
    return combined_df.dropna()

def optimize_sharpe_ratio(returns_df, risk_free_rate=0.02, min_wt=0.0, max_wt=1.0):
    """
    Finds optimal weights to maximize Sharpe Ratio using scipy.optimize.
    """
    n_assets = len(returns_df.columns)
    
    # Expected Annual Return & Covariance
    mu = returns_df.mean() * 252
    cov_matrix = returns_df.cov() * 252
    
    # Objective: Minimize Negative Sharpe Ratio
    def negative_sharpe(weights):
        port_return = np.dot(weights, mu)
        port_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe = (port_return - risk_free_rate) / port_volatility if port_volatility > 0 else 0
        return -sharpe

    # Constraints: Sum of weights = 1
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    
    # Bounds: min_wt <= weight <= max_wt
    bounds = tuple((min_wt, max_wt) for _ in range(n_assets))
    
    # Initial Guess: Equal weights
    init_guess = np.array([1/n_assets] * n_assets)
    
    result = minimize(negative_sharpe, init_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    
    return result

def render_optimization_tab(stocks_dfs_dict):
    st.header("Portfolio Optimization (Sharpe Ratio)")
    st.caption("Maximize risk-adjusted returns using Mean-Variance Optimization.")

    # --- 1. Data Prep ---
    if not stocks_dfs_dict:
        st.warning("No stock data available. Please check the main data source.")
        return

    combined_close = get_combined_data(stocks_dfs_dict)
    all_tickers = combined_close.columns.tolist()
    
    # --- 2. User Controls ---
    col_ctl1, col_ctl2 = st.columns([1, 2])
    
    with col_ctl1:
        st.subheader("Settings")
        selected_tickers = st.multiselect("Select Assets", all_tickers, default=all_tickers[:5], key="opt_assets")
        
        st.markdown("### Constraints per Asset")
        
        # Dynamic Capping to prevent errors
        n_assets = len(selected_tickers)
        # Prevent division by zero if n=1 (though we check n<2 later)
        if n_assets > 1:
            # User requested caps:
            # 1. Max weight default 80%
            # 2. Min weight capped at (100 - Max) / (n-1) to ensure feasibility
            
            default_max = 80.0
            
            # Allow user to adjust max, but keep it logical (must be >= 1/n)
            lower_bound_for_max = (1.0 / n_assets) * 100.0
            max_wt_val = st.number_input("Max Weight (%)", min_value=float(lower_bound_for_max), max_value=100.0, value=max(default_max, lower_bound_for_max), step=5.0)
            
            # Calculate upper bound for Min weight based on the user's selected Max
            # If one asset is Max, the others must share (100 - Max).
            # So (n-1) * Min <= 100 - Max  =>  Min <= (100 - Max) / (n-1)
            upper_bound_for_min = (100.0 - max_wt_val) / (n_assets - 1)
            
            # Ensure safe default (e.g. 0 or lower than bound)
            default_min = 0.0
            
            min_wt_val = st.number_input("Min Weight (%)", min_value=0.0, max_value=max(0.0, upper_bound_for_min), value=min(default_min, upper_bound_for_min), step=1.0)
            
            min_wt = min_wt_val / 100.0
            max_wt = max_wt_val / 100.0
        else:
            min_wt = 0.0
            max_wt = 1.0
        
        risk_free = st.number_input("Risk Free Rate (%)", 0.0, 20.0, 2.0, 0.5, key="opt_risk_free") / 100.0

    if len(selected_tickers) < 2:
        st.info("Select at least 2 stocks to optimize.")
        return

    # Filter data
    price_data = combined_close[selected_tickers]
    returns_pct = price_data.pct_change().dropna()

    # --- 3. Optimization ---
    with st.spinner("Optimizing Portfolio..."):
        opt_result = optimize_sharpe_ratio(returns_pct, risk_free, min_wt, max_wt)
    
    if not opt_result.success:
        st.error(f"Optimization failed: {opt_result.message}")
        return

    optimal_weights = opt_result.x
    
    # --- 4. Results ---
    with col_ctl2:
        st.subheader("Optimal Allocation")
        
        # Calculate optimal metrics
        ann_ret_opt = np.dot(optimal_weights, returns_pct.mean() * 252)
        ann_vol_opt = np.sqrt(np.dot(optimal_weights.T, np.dot(returns_pct.cov() * 252, optimal_weights)))
        sharpe_opt = (ann_ret_opt - risk_free) / ann_vol_opt
        
        # Metrics Row
        m1, m2, m3 = st.columns(3)
        m1.metric("Exp. Annual Return", f"{ann_ret_opt:.2%}")
        m2.metric("Annual Volatility", f"{ann_vol_opt:.2%}")
        m3.metric("Sharpe Ratio", f"{sharpe_opt:.2f}")
        
        # Allocation Chart
        alloc_df = pd.DataFrame({"Asset": selected_tickers, "Weight": optimal_weights})
        alloc_df = alloc_df[alloc_df['Weight'] > 0.001] # Filter tiny weights
        alloc_df = alloc_df.sort_values("Weight", ascending=False)
        
        fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
        ax_pie.pie(alloc_df['Weight'], labels=alloc_df['Asset'], autopct='%1.1f%%', startangle=90)
        ax_pie.set_title("Recommended Portfolio Weights")
        st.pyplot(fig_pie)

    # --- 5. Visualizer & Single Stock View ---
    st.divider()
    
    tab_viz, tab_single = st.tabs(["Efficient Frontier", "Single Stock Analysis"])
    
    with tab_viz:
        st.markdown("#### Efficient Frontier Simulation")
        num_simulations = 2000
        sim_results = np.zeros((3, num_simulations))
        
        mu_vec = returns_pct.mean() * 252
        cov_mat = returns_pct.cov() * 252
        
        for i in range(num_simulations):
            w = np.random.random(len(selected_tickers))
            w /= np.sum(w)
            
            p_ret = np.dot(w, mu_vec)
            p_vol = np.sqrt(np.dot(w.T, np.dot(cov_mat, w)))
            p_sr = (p_ret - risk_free) / p_vol
            
            sim_results[0,i] = p_vol
            sim_results[1,i] = p_ret
            sim_results[2,i] = p_sr
            
        fig_ef, ax_ef = plt.subplots(figsize=(10, 6))
        sc = ax_ef.scatter(sim_results[0,:], sim_results[1,:], c=sim_results[2,:], cmap='viridis', marker='o', alpha=0.5)
        plt.colorbar(sc, label='Sharpe Ratio')
        
        # Plot Optimal Point
        ax_ef.scatter(ann_vol_opt, ann_ret_opt, c='red', s=200, marker='*', label='Optimal Porfolio')
        
        ax_ef.set_xlabel('Volatility (Risk)')
        ax_ef.set_ylabel('Return')
        ax_ef.set_title('Random Portfolios vs Optimal')
        ax_ef.legend()
        st.pyplot(fig_ef)

        st.markdown(r"""
        **1. Modern Portfolio Theory Metrics**
        
        The optimization is based on the **Mean-Variance** framework. We define the following key terms:
        
        *   **Risk-Free Rate ($R_f$)**:
            The theoretical return of an investment with zero risk (e.g., US Treasury Bonds). It serves as the baseline to measure "excess return". If an asset yields less than $R_f$, it is not worth the risk.
        
        *   **Efficient Frontier**:
            The set of optimal portfolios that offer the highest expected return for a defined level of risk. Portfolios below this curve are sub-optimal because they do not provide enough return for the risk taken.
        
        *   **Portfolio Expected Return ($\mathbb{E}[R_p]$)**:
            $$ \mathbb{E}[R_p] = \sum_{i=1}^{N} w_i \mathbb{E}[R_i] = \mathbf{w}^T \mathbf{\mu} $$
            Where $\mathbf{w}$ is the vector of weights and $\mathbf{\mu}$ is the vector of expected returns for each asset.
            
        *   **Portfolio Variance ($\sigma_p^2$)**:
            $$ \sigma_p^2 = \sum_{i=1}^{N} \sum_{j=1}^{N} w_i w_j \sigma_{ij} = \mathbf{w}^T \mathbf{\Sigma} \mathbf{w} $$
            Where $\mathbf{\Sigma}$ is the Covariance Matrix of asset returns.
            
        *   **Sharpe Ratio ($S_p$)**:
            $$ S_p = \frac{\mathbb{E}[R_p] - R_f}{\sigma_p} $$
            The objective function seeks to maximize this ratio, effectively finding the point on the Efficient Frontier that offers the highest excess return per unit of risk.
        """)


    with tab_single:
        st.subheader("Individual Asset Analysis")
        target_stock = st.selectbox("Select Stock to View", selected_tickers, key="opt_single_select")
        
        stock_ret = returns_pct[target_stock]
        stock_ann_vol = stock_ret.std() * np.sqrt(252)
        stock_ann_ret = stock_ret.mean() * 252
        
        col_s1, col_s2 = st.columns(2)
        col_s1.metric("Stock Volatility", f"{stock_ann_vol:.2%}")
        col_s2.metric("Stock Annual Return", f"{stock_ann_ret:.2%}")
        
        # Volatility Plot (Rolling)
        window = st.slider("Rolling Window (Days)", 10, 90, 30, key="opt_roll_window")
        rolling_vol = stock_ret.rolling(window=window).std() * np.sqrt(252)
        
        fig_vol, ax_vol = plt.subplots(figsize=(10, 4))
        ax_vol.plot(rolling_vol.index, rolling_vol, label=f'{window}-Day Rolling Volatility')
        ax_vol.set_title(f"{target_stock} Historical Volatility")
        ax_vol.set_ylabel("Annualized Volatility")
        ax_vol.legend()
        st.pyplot(fig_vol)

        st.markdown(r"""
        #### Formal Definitions
        
        **1. Log Returns ($r_t$)**
        We use log returns for better statistical properties in additive modeling:
        $$ r_t = \ln(\frac{P_t}{P_{t-1}}) $$
        
        **2. Stock Volatility ($\sigma_{daily}$)**
        The standard deviation of daily returns over the sample period:
        $$ \sigma_{daily} = \sqrt{\frac{1}{N-1} \sum_{t=1}^{N} (r_t - \bar{r})^2} $$
        
        **3. Annualized Volatility ($\sigma_{ann}$)**
        Assuming 252 trading days in a year, we scale the daily volatility:
        $$ \sigma_{ann} = \sigma_{daily} \times \sqrt{252} $$
        
        **4. Stock Annual Return ($R_{ann}$)**
        The geometric mean return scaled to a year:
        $$ R_{ann} = (1 + \bar{r})^{252} - 1 $$
        *(Note: Simple mean return $\times$ 252 is often used as an approximation in Optimization contexts)*
        """)
