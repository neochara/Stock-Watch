# Global constants are defined in this file
from datetime import datetime

#STOCK_NAME_DATA_DICT = {'NVDA':'Nvidia', 'TSLA':'Tesla', 'AMZN':'Amazon', 'MSFT':'Microsoft', 'COST':'Costco', 'GME':'GameStop', 'PFE':'Pfizer Inc', 'LLY':'Eli Lilly And Co'}
#STOCK_LIST =  ['NVDA', 'TSLA', 'AMZN', 'MSFT', 'COST', 'GME', 'PFE', 'LLY']

STOCK_DATA_DICT = {'Nvidia':'NVDA', 'Tesla':'TSLA', 'Amazon':'AMZN', 'Microsoft':'MSFT', 'Costco':'COST',
                    'GameStop':'GME', 'Pfizer Inc':'PFE', 'Eli Lilly And Co':'LLY',
                    'Netflix Inc':'NFLX', 'Palantir Technologies Inc':'PLTR', 'Volcon Inc':'VLCN', 'Visa':'V'}

START_DATE = "2018-01-01"
TODAY = datetime.today()
END_DATE = datetime.today().date()

#BASE_PATH = os.getcwd() #'/Users/neo_chara/Desktop/Projects/Stock-Watch'
BASE_PATH = '/Users/neo_chara/Desktop/Projects/Stock-Watch'