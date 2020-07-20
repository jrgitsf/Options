# https://github.com/mcdallas/wallstreet

from wallstreet import Stock, Call, Put
import numpy as mp

s = Stock('AAPL')

print(s.change)

apple = Stock('AAPL', source='yahoo')

print(apple)

call = Call('AAPL', strike=apple.price, source='yahoo')

p = Stock('BTC-USD')
print(p)

r = Call('RACE', d=10, m=7, y=2020)
print(r.strikes)
print(r.underlying.price)