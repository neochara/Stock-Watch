import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def render_probability_tab():
    st.header("Probability & Statistics")
    st.caption("Foundational concepts: Random Variables, Correlation, and Diversification.")

    tab1, tab2 = st.tabs(["Distributions", "Diversification Demo"])

    with tab1:
        st.subheader("Random Variables & Normal Distribution")
        st.markdown(r"""
        Financial returns are often modeled as **Random Variables**. A common assumption is that log-returns follow a **Normal (Gaussian) Distribution**:
        
        $$ f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{ -\frac{1}{2} (\frac{x-\mu}{\sigma})^2 } $$
        
        Where:
        - $\mu$ (Mu): Expected Return (Mean)
        - $\sigma$ (Sigma): Volatility (Standard Deviation)
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            mu = st.slider(r"Mean Return ($\mu$)", -0.05, 0.05, 0.00, 0.01)
            sigma = st.slider(r"Volatility ($\sigma$)", 0.01, 0.10, 0.02, 0.01)
            n_samples = st.slider("Sample Size", 100, 5000, 1000)
            
        with col2:
            # Generate dummy data
            data = np.random.normal(mu, sigma, n_samples)
            
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.histplot(data, bins=30, kde=True, ax=ax, color='skyblue')
            ax.axvline(mu, color='red', linestyle='--', label=f'Mean: {mu:.2f}')
            ax.set_title("Return Distribution")
            ax.legend()
            st.pyplot(fig)

    with tab2:
        st.subheader("The Power of Diversification")
        st.markdown(r"""
        **Diversification** reduces portfolio risk by combining assets that are not perfectly correlated.
        
        Portfolio Variance for 2 assets:
        $$ \sigma_p^2 = w_1^2 \sigma_1^2 + w_2^2 \sigma_2^2 + 2 w_1 w_2 \rho \sigma_1 \sigma_2 $$
        
        - $\rho$ (Rho): Correlation coefficient ($-1$ to $+1$).
        - If $\rho < 1$, the combined risk is **lower** than the weighted average risk.
        """)
        
        c1, c2 = st.columns(2)
        with c1:
            rho = st.slider(r"Correlation ($\rho$)", -1.0, 1.0, 0.0, 0.1)
            w1 = st.slider("Weight Asset 1", 0.0, 1.0, 0.5)
            sigma1 = 0.20 # Fixed for demo
            sigma2 = 0.20 # Fixed for demo
            
        with c2:
            w2 = 1.0 - w1
            
            # Calculate Risk
            port_var = (w1**2 * sigma1**2) + (w2**2 * sigma2**2) + (2 * w1 * w2 * rho * sigma1 * sigma2)
            port_vol = np.sqrt(port_var)
            
            st.metric("Portfolio Volatility", f"{port_vol:.2%}", help="Note how this changes as you lower Correlation!")
            
            # Visualizing Volatility Reduction
            # Plot Volatility vs Weight 1 for the selected Rho
            w_space = np.linspace(0, 1, 100)
            vol_space = np.sqrt((w_space**2 * sigma1**2) + ((1-w_space)**2 * sigma2**2) + (2 * w_space * (1-w_space) * rho * sigma1 * sigma2))
            
            fig2, ax2 = plt.subplots(figsize=(6, 3))
            ax2.plot(w_space, vol_space, label=f'Correlation = {rho}')
            ax2.scatter(w1, port_vol, color='red', s=100, zorder=5, label='Current Alloc')
            ax2.set_xlabel("Weight in Asset 1")
            ax2.set_ylabel("Portfolio Volatility")
            ax2.set_title("Risk vs Allocation")
            ax2.legend()
            st.pyplot(fig2)
