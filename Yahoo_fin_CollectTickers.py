# http://theautomatic.net/2018/07/31/how-to-get-live-stock-prices-with-python/
# http://jonathansoma.com/lede/foundations/classes/pandas%20columns%20and%20functions/apply-a-function-to-every-row-in-a-pandas-dataframe/
from yahoo_fin.stock_info import *
import datetime as dt
from yahoo_fin.options import *
import requests
import lxml.html as lh
import pandas as pd
from functools import reduce
import pickle
# this ssl stuff is needed for pycharm to execute. Was not needed in jupyter
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


#--------------------------------
# the option call function returns the option name but includes the expiration. How to strip??? so,
#splits a string before the 1st number as a list. [0] prints the 1st item in the list-- the ticker
#https://www.w3schools.com/python/python_regex.asp
# the \d splits it after where the string contains digits (not intuitive).
import re
option = 'ADBE200731C00490000'

x = re.split('\d', option)
print(type(x))
print(x[0])
#-------------------------------



# This is an easier way to get the data, oops.
print('apple current price is ',get_live_price("aapl"))
current = get_quote_table("aapl", dict_result = True)
print(type(current))
print(current)
print(current['Avg. Volume'])
print(current['Earnings Date'])
print(current['Quote Price'])


# sp_greater_than_threshold = ['ABT', 'ACN', 'ADBE']
# sp_greater_than_threshold = ['ABT', 'ACN', 'ADBE', 'ADI', 'ADSK', 'AEE', 'AZO', 'BAC', 'BBY', 'BDX', 'BK', 'C', 'CAG', 'CDNS', 'CDW', 'CFG']
sp_greater_than_threshold = ['ABT', 'ACN', 'ADBE', 'ADSK', 'ALGN', 'APH', 'AZO', 'BAC', 'BBY', 'BIIB', 'BK', 'BLK', 'C', 'CAG', 'CDNS', 'CFG', 'CMA', 'CMG', 'COF', 'COO', 'COST', 'COTY', 'CPB', 'CPRT', 'CRM', 'CSX', 'DAL', 'DE', 'DFS', 'DG', 'DLTR', 'DOV', 'DPZ', 'DRI', 'EFX', 'EL', 'FAST', 'FDX', 'FE', 'FRC', 'GIS', 'GL', 'GS', 'HAL', 'HPE', 'HPQ', 'HRB', 'HRL', 'IBM', 'INFO', 'INTU', 'JBHT', 'JNJ', 'JPM', 'KEY', 'KEYS', 'KMI', 'KMX', 'KO', 'KR', 'KSU', 'LEN', 'LMT', 'LVS', 'MDT', 'MKC', 'MS', 'MSFT', 'MU', 'NDAQ', 'NKE', 'NTAP', 'ORCL', 'PAYX', 'PCAR', 'PEP', 'PLD', 'PM', 'PNC', 'PVH', 'RF', 'ROST', 'RSG', 'RTX', 'SBAC', 'SCHW', 'SJM', 'SLG', 'STT', 'STZ', 'TFC', 'TIF', 'TMO', 'TXN', 'TXT', 'UAL', 'UDR', 'ULTA', 'UNH', 'USB', 'WFC', 'WHR', 'WLTW', 'WM', 'WMB', 'ZION']
# price_data = {ticker: get_data(ticker.replace(".", "-"), start_date="06/01/2020") for ticker in sp_greater_than_threshold}
# print(price_data)
# combined = reduce(lambda x, y: x.append(y), price_data.values())
# print(combined)
# print(combined.to_string())
# print('price_data is ',type(price_data),'combined is   ', type(combined),'combined.to_string() is   ',type(combined.to_string()), sep='type')

print("oooooooooooooooooooooooooooooooooooo")
options_data = {ticker: get_calls(ticker) for ticker in sp_greater_than_threshold}
# print(price_data)
combined_options = reduce(lambda x, y: x.append(y), options_data.values())
print(type(combined_options))
# print(combined_options)
# print(combined_options.to_string())

combined_options['ticker'] = combined_options['Contract Name'] # this works
combined_options['ticker'] = combined_options['ticker'].str.split('\d',expand = True)
print(combined_options.dtypes)
# print(combined_options['ticker'])
print(combined_options.ticker)
print(combined_options.to_string())
# combined_options['Live Price'] = get_live_price('ABT')
print(combined_options.to_string)
# combined_options['Live Price'] = combined_options['Live Price'].apply(get_live_price(combined_options['ticker']))
# This is so unintuitive
combined_options['Live Price']= combined_options['ticker'].apply(get_live_price)
print(combined_options.to_string)
print(get_live_price('ADBE'))
# print(combined_options['ticker'].str[:4])

with open("sp500tickers_greater_threshold.pickle", "wb") as f:
    pickle.dump(combined_options, f)