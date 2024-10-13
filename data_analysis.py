import pandas as pd

STOCK_LIST =  ['NVDA', 'TSLA', 'AMZN', 'MSFT', 'COST']
BASE_PATH = '/Users/neo_chara/Desktop/Projects/Stock-Watch'

def get_clean_data():
    stocks_dfs_dict = {}
    for symbol in STOCK_LIST:
        file_name = f"{symbol.lower()}_stock.csv"
        path_csv = f"{BASE_PATH}/data/{file_name}"
        stocks_dfs_dict[f"{symbol.lower()}"] = pd.read_csv(path_csv,index_col='Date')

    return stocks_dfs_dict


def get_description():
    stocks_dict = get_clean_data()

    description_dict = {}
    for stock_idx, stock_data in stocks_dict.items():
        description_dict[stock_idx] = stock_data.describe()
    
    return description_dict


def _get_llm_response(df):
    return "llm response"

def get_nl_summary():
    description_dict = get_description()

    response_dict = {}
    for stock_idx, stock_description in description_dict.items():
        response_dict[stock_idx] = _get_llm_response(stock_description)
    
    return response_dict

def main():
    get_clean_data()
    get_description()
    random = get_nl_summary()
    print(random)

if __name__ == "__main__":
    main()
