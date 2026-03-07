import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def render_stochastic_tab():
    st.header("Stochastic Processes")
    st.caption("Modeling stock price movements over time.")

    tab1, tab2 = st.tabs(["Random Walk", "Geometric Brownian Motion (GBM)"])

    with tab1:
        st.subheader("Simple Random Walk")
        st.markdown(r"""
        A **Symbolic Random Walk** describes a path that consists of a succession of random steps.
        $$ S_t = S_{t-1} + \epsilon_t $$
        where $\epsilon_t$ is a random shock (e.g., coin toss +1 or -1).
        """)
        
        n_steps = st.slider("Steps", 100, 1000, 500, key="rw_steps")
        
        if st.button("Simulate Walk", key="rw_sim"):
            steps = np.random.choice([-1, 1], size=n_steps)
            path = np.cumsum(steps)
            
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.plot(path)
            ax.set_title("Symmetric Random Walk 1D")
            st.pyplot(fig)

    with tab2:
        st.subheader("Geometric Brownian Motion (GBM)")
        st.markdown(r"""
        Stock prices are typically modeled using **GBM**, which prevents negative prices and accounts for compounding returns.
        
        **SDE**: $dS_t = \mu S_t dt + \sigma S_t dW_t$
        
        **Solution**: 
        $$ S_t = S_0 \exp\left( (\mu - \frac{\sigma^2}{2})t + \sigma W_t \right) $$
        
        This is the foundation for the **Black-Scholes** model.
        """)
        
        c1, c2 = st.columns(2)
        with c1:
            mu = st.number_input(r"Drift ($\mu$)", 0.0, 0.5, 0.05, 0.01, key="gbm_mu")
            sigma = st.number_input(r"Volatility ($\sigma$)", 0.01, 1.0, 0.2, 0.01, key="gbm_sigma")
            S0 = st.number_input(r"Start Price ($S_0$)", 10, 1000, 100, key="gbm_s0")
            T = 1.0 # 1 year
            dt = 1/252 # Daily steps
            N = int(T/dt)
            
        with c2:
            n_paths = st.slider("Number of Paths", 1, 50, 10, key="gbm_paths")
            
            # Simulation
            t = np.linspace(0, T, N)
            
            fig, ax = plt.subplots(figsize=(10, 5))
            
            for _ in range(n_paths):
                W = np.random.standard_normal(size=N) 
                W = np.cumsum(W)*np.sqrt(dt) ### Standard Brownian Motion 
                X = (mu - 0.5*sigma**2)*t + sigma*W 
                S = S0*np.exp(X) ## GBM 
                ax.plot(t, S, alpha=0.6)
                
            ax.set_title("GBM Price Paths (1 Year)")
            ax.set_xlabel("Time (Years)")
            ax.set_ylabel("Price")
            st.pyplot(fig)
