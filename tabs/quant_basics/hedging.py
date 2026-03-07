import streamlit as st
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def calculate_greeks(S, K, T, r, sigma):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    
    # Call Greeks
    delta = norm.cdf(d1)
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    theta = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r*T) * norm.cdf(d2)
    rho = K * T * np.exp(-r*T) * norm.cdf(d2)
    vega = S * norm.pdf(d1) * np.sqrt(T)
    
    # Annualize theta usually shown as 1 day decay
    # But keeping raw for now or scaling? Usually Theta is shown per day
    theta_daily = theta / 365.0
    
    return delta, gamma, theta_daily, vega, rho

def render_hedging_tab():
    st.header("Hedging & The Greeks")
    st.caption("Managing risk using derivatives sensitivities.")
    
    st.markdown(r"""
    **The Greeks** measure how an option's price changes relative to market variables:
    
    - **Delta ($\Delta$)**: Sensitivity to Stock Price. $\frac{\partial C}{\partial S}$.
    - **Gamma ($\Gamma$)**: Sensitivity of Delta to Stock Price. $\frac{\partial^2 C}{\partial S^2}$.
    - **Theta ($\Theta$)**: Time decay. $\frac{\partial C}{\partial t}$.
    - **Vega ($\nu$)**: Sensitivity to Volatility. $\frac{\partial C}{\partial \sigma}$.
    """)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Parameters")
        S = st.number_input("Spot Price", 50, 200, 100, key="hedge_S")
        K = st.number_input("Strike Price", 50, 200, 100, key="hedge_K")
        T_days = st.slider("Time (Days)", 1, 180, 30, key="hedge_T")
        T = T_days / 365.0
        sigma = st.slider("Vol (%)", 5, 100, 20, key="hedge_sigma") / 100.0
        r = 0.05
        
        delta, gamma, theta, vega, _ = calculate_greeks(S, K, T, r, sigma)
        
        st.divider()
        st.metric("Delta", f"{delta:.4f}")
        st.metric("Gamma", f"{gamma:.4f}")
        st.metric("Theta (Daily)", f"{theta:.4f}")
        st.metric("Vega", f"{vega:.4f}")

    with col2:
        st.subheader("Delta vs Spot Price")
        st.markdown("*Why Delta Hedge?* To make a portfolio 'Delta Neutral', immune to small price moves.")
        
        spots = np.linspace(K*0.7, K*1.3, 100)
        deltas = []
        
        for s in spots:
            d, _, _, _, _ = calculate_greeks(s, K, T, r, sigma)
            deltas.append(d)
            
        fig, ax = plt.subplots()
        ax.plot(spots, deltas, color='purple', label='Call Delta')
        ax.axvline(S, color='red', linestyle='--', label='Current Spot')
        ax.axhline(delta, color='green', linestyle=':', label='Current Delta')
        ax.set_xlabel("Spot Price")
        ax.set_ylabel("Delta")
        ax.set_title("Delta Sensitivity")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
