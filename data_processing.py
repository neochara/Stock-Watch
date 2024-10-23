import yfinance as yf
from datetime import datetime
import pandas as pd

START_DATE = "2018-01-01"
STOCK_LIST =  ['NVDA', 'TSLA', 'AMZN', 'MSFT', 'COST', 'GME', 'PFE', 'LLY']

def fetch_data():
    today = datetime.today()

    for stock_symbol in STOCK_LIST:
        stock_data = yf.download(stock_symbol, start=START_DATE, end=today)    
        stock_data.to_csv(f"data/{stock_symbol.lower()}_stock.csv")

def _count_null(df):
    return df.isnull().sum().sum()

def check_null():
    for index in STOCK_LIST:
        index_df = pd.read_csv(f"data/{index.lower()}_stock.csv")
        total_nulls = _count_null(index_df)
        if total_nulls > 0:
            print(f"{index} has {total_nulls} null entries")

def main():
    fetch_data()
    check_null()

if __name__ == "__main__":
    main()