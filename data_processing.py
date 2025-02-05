import yfinance as yf
from datetime import datetime
import pandas as pd
from constants import STOCK_DATA_DICT, START_DATE, TODAY
import os

def fetch_data():
    # Check if the 'data' directory exists, raise an error if it doesn't
    if not os.path.exists('data'):
        raise FileNotFoundError("The 'data' directory does not exist. Please create it before running the script.")
    
    for company, stock_symbol in STOCK_DATA_DICT.items():
        stock_data = yf.download(stock_symbol, start=START_DATE, end=TODAY)
        #stock_data.to_csv(f"data/{stock_symbol}.csv")
        stock_data.to_csv(f"data/{stock_symbol.lower()}_stock.csv")

def _count_null(df):
    return df.isnull().sum().sum()

def check_null():
    for company, index in STOCK_DATA_DICT.items():
        index_df = pd.read_csv(f"data/{index}.csv")
        total_nulls = _count_null(index_df)
        if total_nulls > 0:
            print(f"{index} has {total_nulls} null entries")

def main():
    fetch_data()
    check_null()

if __name__ == "__main__":
    main()