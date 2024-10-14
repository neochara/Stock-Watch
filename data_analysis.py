import os
import pandas as pd
from openai import OpenAI

STOCK_LIST = ['NVDA', 'TSLA', 'AMZN', 'MSFT', 'COST']
BASE_PATH = os.getcwd() #'/Users/neo_chara/Desktop/Projects/Stock-Watch'

def get_clean_data():
    stocks_dfs_dict = {}
    for symbol in STOCK_LIST:
        file_name = f"{symbol.lower()}_stock.csv"
        path_csv = f"{BASE_PATH}/data/{file_name}"
        stocks_dfs_dict[f"{symbol.lower()}"] = pd.read_csv(path_csv,index_col='Date', parse_dates=True)

    return stocks_dfs_dict


def get_description():
    stocks_dict = get_clean_data()

    description_dict = {}
    for stock_idx, stock_data in stocks_dict.items():
        description_dict[stock_idx] = stock_data.describe()
    
    return description_dict

def _format_description(descr_dict):
    """Filters description dict to keep indices of interest and Close column"""
    indices_to_keep = ["mean", "min", "max", "std"]
    characteristic_to_keep = "Close"

    #restricted_data = {key: df.loc[indices_to_keep] for key, df in descr_dict.items()}
    all_info_dictionaries = {}
    for key, df in descr_dict.items():
        info_df = df[characteristic_to_keep].loc[indices_to_keep]#.to_csv(index=True)
        info_dict = info_df.to_dict()
        info_dict['stock_index'] = key
        all_info_dictionaries[key] = info_dict
    
    return all_info_dictionaries


def _get_llm_response(info_dict):
    client = OpenAI()
    idx_name = info_dict['stock_index'].upper()

    query_str = f"""
    I am providing you with the following summary statistics \n{info_dict}\n of the {idx_name} stock index. 
    Can you give me a description, just like the following:
    Here are the statistics for the {idx_name} index. The average stock value was $XXX. The min and max were respectively
    $XX and $XX, and we observed a standard deviation of $XXX.
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a financial analyst."},
            {
                "role": "user",
                "content": query_str
            }
        ]
    )
    return completion.choices[0].message.content


def get_nl_summary():
    """"Gets a summary of the filtered descriptions, for each stock index"""
    descr_dict = get_description()
    all_info_dictionaries = _format_description(descr_dict)

    response_dict = {}
    for stock_idx, info_dict in all_info_dictionaries.items():
        response_dict[stock_idx] = _get_llm_response(info_dict)
    
    return response_dict

def main():
    get_clean_data()
    get_description()
    random = get_nl_summary()
    print(random)

if __name__ == "__main__":
    main()
