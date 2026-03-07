import streamlit as st
from tabs.portfolio_management.optimization import render_optimization_tab
from tabs.portfolio_management.allocation import render_allocation_tab
from tabs.portfolio_management.risk import render_risk_tab
from tabs.portfolio_management.forecasting import render_forecasting_tab
from tabs.portfolio_management.backtest import render_backtest_tab

def render_portfolio_tab(stocks_dfs_dict):
    st.header("Portfolio Management")
    
    # Expanded set of tabs
    tabs = st.tabs([
        "Optimization", 
        "Manual Allocation", 
        "Risk & Correlation", 
        "Forecasting", 
        "Backtest"
    ])
    
    with tabs[0]:
        render_optimization_tab(stocks_dfs_dict)
        
    with tabs[1]:
        render_allocation_tab(stocks_dfs_dict)
        
    with tabs[2]:
        render_risk_tab(stocks_dfs_dict)
        
    with tabs[3]:
        render_forecasting_tab(stocks_dfs_dict)
        
    with tabs[4]:
        render_backtest_tab(stocks_dfs_dict)
