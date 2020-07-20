# http://theautomatic.net/2018/01/25/coding-yahoo_fin-package/

import io
import yahoo_fin
import pandas as pd
import requests_html
from functools import reduce
from yahoo_fin.stock_info import *

# Using pycharm with yahoo_fin required me to add the following to make the tickers_sp500 work for some reason
# I did not need this with the exact same code on jupyter
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# a = get_data("amzn") # gets Amazon's data
# print(a)
# this is what is in the tickers_sp500() function
# the [0] is for the 1st table on the linked page.
# sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
# sp_tickers = sorted(sp500.Symbol.tolist())
# print(sp500)

sp = tickers_sp500()  # this works.
print(sp)
## the wikipedia list returns some tickers with a "." like BRK.B however the yahoo url requires "-"
# yahoo trips on "BF.B" goind down and "BRK.B" going from reverse.
a = get_data("amzn")  # works
# b = get_data("brk.b") # this will crap out.
b = get_data("brk-b")  # this works!
# print(a, b)

# this is my fix. It works to replace the "." with "-" and ignores all other characters. Nice!
# for ticker in sp:
#     ticker_str = ticker.replace(".", '-')
#     print(ticker_str, get_data(ticker_str, start_date="06/01/2020"))

# This is even bettter and works. The replace replaces the "." with "-" that yahoo uses.
price_data = {ticker: get_data(ticker.replace(".", "-"), start_date="06/01/2020") for ticker in sp}
# print(price_data)
combined = reduce(lambda x, y: x.append(y), price_data.values())
print(combined)

# If you run yahoo_fin, the getdata() works except if the ticker has a "." in it such as as BF.B and BRK.B.
# This works --> sp = tickers_sp500() but this craps out after "BEN" --> "BF.B"
# price_data = {ticker : get_data(ticker) for ticker in sp}. and "BRK.B" if you run a slice sp[::-1].
# Can you fix that or let me know if I am doing something wrong?
# https://query1.finance.yahoo.com/v8/finance/chart/ben # this works.
# https://query1.finance.yahoo.com/v8/finance/chart/brk.b # this does not work.

# for ticker in sp[::-1]:
#     # print(ticker)
#     if ticker != ("BRK.B"):
#     # if ticker != ("BF.B" or "BRK.B"):
#         print(ticker, get_data(ticker, start_date="06/01/2020"))
