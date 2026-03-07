import streamlit as st
import numpy as np
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt

def black_scholes_price(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    
    if option_type == 'call':
        price = S*norm.cdf(d1) - K*np.exp(-r*T)*norm.cdf(d2)
    else:
        price = K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)
    
    return price

def render_options_tab():
    st.header("Options Pricing Models")
    st.caption("Binomial Trees and Black-Scholes-Merton.")
    
    tab1, tab2 = st.tabs(["Black-Scholes Calculator", "Payoff Diagrams"])
    
    with tab1:
        st.subheader("Black-Scholes-Merton (BSM) Formula")
        st.markdown(r"""
        The **BSM Model** provides a closed-form solution for pricing European options:
        
        $$ C(S,t) = N(d_1)S_t - N(d_2)Ke^{-r(T-t)} $$
        
        Where:
        - $S_t$: Spot price
        - $K$: Strike price
        - $r$: Risk-free rate
        - $\sigma$: Volatility
        - $T-t$: Time to maturity
        """)
        
        c1, c2, c3 = st.columns(3)
        S = c1.number_input("Spot Price", 50.0, 500.0, 100.0, 5.0, key="opt_S")
        K = c2.number_input("Strike Price", 50.0, 500.0, 100.0, 5.0, key="opt_K")
        T_days = c3.slider("Days to Expiration", 1, 365, 30, key="opt_T")
        T = T_days / 365.0
        
        c4, c5 = st.columns(2)
        r = c4.slider("Risk-Free Rate (%)", 0.0, 10.0, 5.0, 0.5, key="opt_r") / 100.0
        sigma = c5.slider("Volatility (%)", 5.0, 100.0, 20.0, 5.0, key="opt_sigma") / 100.0
        
        # Calculate
        call_price = black_scholes_price(S, K, T, r, sigma, 'call')
        put_price = black_scholes_price(S, K, T, r, sigma, 'put')
        
        st.success(f"**Call Price**: ${call_price:.2f}")
        st.info(f"**Put Price**: ${put_price:.2f}")
        
    with tab2:
        st.subheader("Option Payoff at Expiration")
        st.markdown("Visualizing the profit/loss profile of holding an option.")
        
        spot_range = np.linspace(K * 0.5, K * 1.5, 100)
        
        # Intrinsic Values at Expiration
        call_payoff = np.maximum(spot_range - K, 0) - call_price #Net Profit
        put_payoff = np.maximum(K - spot_range, 0) - put_price
        
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(spot_range, call_payoff, label='Long Call Profit', color='green')
        ax.plot(spot_range, put_payoff, label='Long Put Profit', color='red', linestyle='--')
        ax.axhline(0, color='black', linewidth=1)
        ax.axvline(K, color='gray', linestyle=':', label='Strike')
        
        ax.set_xlabel("Stock Price at Expiration")
        ax.set_ylabel("Profit / Loss")
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
