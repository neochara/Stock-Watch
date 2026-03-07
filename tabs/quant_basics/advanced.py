import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def render_advanced_tab():
    st.header("Advanced Volatility: Heston Model")
    st.caption("Stochastic Volatility modeling for real-world markets.")
    
    with st.expander("Why Stochastic Volatility?", expanded=True):
        st.markdown(r"""
        Black-Scholes assumes volatility ($\sigma$) is constant. In reality, volatility changes over time and clusters.
        
        The **Heston Model** assumes volatility itself follows a random process (CIR process):
        
        1.  **Price Process**: $dS_t = \mu S_t dt + \sqrt{v_t} S_t dW_t^S$
        2.  **Variance Process**: $dv_t = \kappa (\theta - v_t) dt + \xi \sqrt{v_t} dW_t^v$
        
        Where:
        - $\theta$: Long term variance mean.
        - $\kappa$: Mean reversion speed.
        - $\xi$: Volatility of volatility (Vol of Vol).
        - $\rho$: Correlation between price $S$ and volatility $v$.
        """)
    
    st.info("Demonstration of Heston Volatility Paths")
    
    col1, col2 = st.columns(2)
    with col1:
        kappa = st.slider(r"Mean Reversion ($\kappa$)", 0.1, 5.0, 2.0)
        theta = st.slider(r"Long Term Vol ($\sqrt{\theta}$)", 0.05, 0.50, 0.20)**2 # convert to variance
        xi = st.slider(r"Vol of Vol ($\xi$)", 0.1, 1.0, 0.3)
        v0 = theta # Start at mean
    
    with col2:
        # Simple Euler simulation of Variance
        T = 1.0
        dt = 1/252
        N = 252
        n_sims = 10
        
        t_space = np.linspace(0, T, N)
        fig, ax = plt.subplots(figsize=(8, 5))
        
        for _ in range(n_sims):
            v = np.zeros(N)
            v[0] = v0
            for t in range(1, N):
                dW = np.random.normal(0, np.sqrt(dt))
                # Heston variance step (simplified)
                # Ensure non-negative with abs() or reflection
                drift = kappa * (theta - v[t-1]) * dt
                shock = xi * np.sqrt(max(v[t-1], 0)) * dW
                v[t] = v[t-1] + drift + shock
            
            # Convert variance back to Volatility (sqrt) for plotting
            ax.plot(t_space, np.sqrt(np.maximum(v, 0)), alpha=0.6)
            
        ax.set_title("Stochastic Volatility Paths (Heston)")
        ax.set_xlabel("Time (Years)")
        ax.set_ylabel("Volatility ($\sqrt{v_t}$)")
        ax.axhline(np.sqrt(theta), color='black', linestyle='--', label='Long-Term Mean')
        ax.legend()
        st.pyplot(fig)
