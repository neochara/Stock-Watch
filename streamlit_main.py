import streamlit as st
from data_analysis import get_clean_data, get_description, get_nl_summary
import matplotlib.pyplot as plt
from datetime import datetime

st.title('Stock Watch :sunglasses:')

# idx_of_interest = 'cost'
idx_of_interest = st.selectbox("Select a stock index:",
                                ('NVDA', 'TSLA', 'AMZN', 'MSFT', 'COST'))

st.write(f"Let us summarize the {idx_of_interest} stock")
idx_of_interest = idx_of_interest.lower()

# - - - Plot timeseries - - -
stocks_dfs_dict = get_clean_data()

idx_df = stocks_dfs_dict[idx_of_interest]

# Display data to streamlit
st.header(f"{idx_of_interest.upper()} Stock Data")
st.dataframe(idx_df)

# Plot closing price
st.header(f"Closing Price Time Series of {idx_of_interest.upper()}")

plt.figure(figsize=(10, 6))
plt.plot(idx_df.index, idx_df['Close'], marker='o', linestyle='-', color='b')
plt.title(f'{idx_of_interest.upper()} Stock Closing Prices', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Closing Price (USD)', fontsize=12)
plt.grid(True)
st.pyplot(plt)

# - - - Plot timeseries description table - - -
description_dict = get_description()
description_idx_df = description_dict[idx_of_interest]

st.header(f"{idx_of_interest.upper()} Stock Data Statistics")
st.dataframe(description_idx_df)

# - - - Display Text Summary - - -
# response_dict = get_nl_summary()
# response_idx = response_dict[idx_of_interest]

# st.header(f"{idx_of_interest.upper()} Stock Summary")
# st.text(response_idx)
