import streamlit as st
from data_analysis import get_description

def render_stats_tab(idx_of_interest: str):
    description_dict = get_description()
    description_idx_df = description_dict[idx_of_interest]

    st.header(f"{idx_of_interest.upper()} Stock Data Statistics")
    st.dataframe(description_idx_df)

    # Optional text summary (kept commented to match main.py)
    # response_dict = get_nl_summary()
    # response_idx = response_dict[idx_of_interest]
    # st.header(f"{idx_of_interest.upper()} Stock Summary")
    # st.text(response_idx)
