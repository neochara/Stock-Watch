import streamlit as st
from tabs.quant_basics.probability import render_probability_tab
from tabs.quant_basics.stochastic import render_stochastic_tab
from tabs.quant_basics.options import render_options_tab
from tabs.quant_basics.hedging import render_hedging_tab
from tabs.quant_basics.advanced import render_advanced_tab

def render_quant_basics_tab():
    st.header("Quant Finance 'Basics' (Educational)")
    
    tabs = st.tabs([
        "Probability & Stats", 
        "Stochastic Processes", 
        "Options Pricing", 
        "Hedging & Greeks", 
        "Advanced Volatility"
    ])
    
    with tabs[0]:
        render_probability_tab()
    with tabs[1]:
        render_stochastic_tab()
    with tabs[2]:
        render_options_tab()
    with tabs[3]:
        render_hedging_tab()
    with tabs[4]:
        render_advanced_tab()
