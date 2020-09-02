# http://theautomatic.net/2018/07/31/how-to-get-live-stock-prices-with-python/
# http://jonathansoma.com/lede/foundations/classes/pandas%20columns%20and%20functions/apply-a-function-to-every-row-in-a-pandas-dataframe/

from yahoo_fin.stock_info import *
from yahoo_fin.options import *
import numpy as np
import requests
import lxml.html as lh
import pandas as pd
from functools import reduce
import pickle
# this ssl stuff is needed for pycharm to execute. Was not needed in jupyter
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import datetime

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
combined_options.drop(labels=['Last Trade Date','Open Interest','Implied Volatility'], axis = 1, inplace= True)
# print('xxxxxxxxxx')
print(combined_options.to_string)

pd.set_option("display.precision", 2) # this sets the max precisin to two decimal places
print(type(combined_options))

combined_options['ticker'] = combined_options['Contract Name'] # this works
# Careful- lower case 'd' is needed for striping the Ticker
combined_options['ticker'] = combined_options['ticker'].str.split('\d',expand = True)

##################################################################
# combined_options['Test'] = combined_options['Contract Name']
combined_options['Test'] = combined_options['Contract Name'].str.split('\D',expand = False)
print(combined_options)
combined_options['Test'] = combined_options['Test'].str[-2]

combined_options['Expiry'] = combined_options["Contract Name"].str.extract("(\d+)") #This works!
combined_options['Expiry'] = pd.to_datetime(combined_options['Expiry'], format='%y%m%d')
# print(combined_options['Expiry'])

############################################################
print(combined_options.dtypes)
# print(combined_options['ticker'])
print(combined_options.ticker)
print(combined_options.to_string())
# combined_options['Live Price'] = get_live_price('ABT')
print(combined_options.to_string)
# combined_options['Live Price'] = combined_options['Live Price'].apply(get_live_price(combined_options['ticker']))
# This is so unintuitive
combined_options['Live Price']= combined_options['ticker'].apply(get_live_price)

#sometimes yahoo would insert a "-" which then python wouuld interpret the entire series as a string.
combined_options['Bid'] = combined_options['Bid'].replace('-',0.0).astype(float)
print(combined_options.to_string)
print(get_live_price('ADBE'))
# print(combined_options['ticker'].str[:4])

print(combined_options.dtypes)
print(combined_options[['Live Price','Strike']])

# "Where" is the vectorized way to do this. You need numpy. Pandas does not have a ternary way
combined_options['100Shares'] = combined_options['Live Price'] * 100

combined_options['1Contract'] = combined_options['Last Price'] * 100

combined_options['TheMoney'] = np.where(combined_options['Live Price'] >= combined_options['Strike'],
                                         "In", "Out")

combined_options['Intrinsic'] = np.where(combined_options['Live Price'] >= combined_options['Strike'],
                                         combined_options['Live Price']-combined_options['Strike'], 0)

combined_options['Upside'] = np.where(combined_options['Strike'] >= combined_options['Live Price'],
                                         combined_options['Strike']-combined_options['Live Price'], 0)

combined_options['Breakeven'] = combined_options['Live Price'] - combined_options['Last Price'].astype(float)

combined_options['BuyDown'] = np.where(combined_options['Live Price'] >= combined_options['Strike'],
                                         combined_options['Intrinsic'] * 100, 0.0)


combined_options['OptionsProfit'] = combined_options['1Contract'] - combined_options['BuyDown']

combined_options['UpsideProfit'] = combined_options['Upside']*100

combined_options['TotalOptionProfit']=combined_options['OptionsProfit']+combined_options['UpsideProfit']

# Both work. I like the above-- a little more straightforward.
# combined_options['TotalOptionProfit'] = combined_options['OptionsProfit'] + combined_options['Upside'] * 100

combined_options['ROO'] = np.where(combined_options['Strike'] >= combined_options['Live Price'],
                                   100*(combined_options['Last Price']/combined_options['Live Price']),
                                   100*((combined_options['Last Price']-(combined_options['Live Price']-combined_options['Strike']))/combined_options['Strike']))

combined_options

# DON'T Do it this way
# for i in combined_options:
#     if [combined_options['Live Price'].values >= combined_options['Strike'].values]:
#         combined_options['Intrinsic'] = combined_options['Live Price'].values.astype(float)-combined_options['Strike'].values.astype(float)
#         print(combined_options[['Live Price', 'Strike', 'Intrinsic']].to_string)
#     else:
#         combined_options['Intrinsic'] = 0

print(combined_options.to_string)
print(combined_options[['Expiry','Live Price','Strike','100Shares','1Contract','TheMoney','Intrinsic','Upside','Breakeven','BuyDown','OptionsProfit','TotalOptionProfit','ROO']].to_string)
result = combined_options[combined_options['ROO'] > 2]
print(result.to_string)
print("The End")
# with open("sp500tickers_greater_threshold.pickle", "wb") as f:
#     pickle.dump(combined_options, f)