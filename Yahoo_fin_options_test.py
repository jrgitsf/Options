from yahoo_fin.stock_info import *
from yahoo_fin.options import *
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# c= get_calls('cvx', date='2020-8-7')
c = get_calls('cvx', date='July 31, 2020')
# c = get_calls('cvx', date='August 7, 2020')

e = get_expiration_dates('cvx')

print(list(c.head()))

print(type(c))

print(c.to_string())

print(build_options_url('cvx'))
print(type(e))
print(e)

chain = get_options_chain('CVX')  # Option chain does call and puts. Don't really need puts
print(type(chain))
print(list(chain))
print(chain['calls'][0:3][:].to_string())  # the extra [:] does not do anything
print(chain['calls'][0:3]['Bid'].to_string())  # this prints out one column
print(chain['calls'][0:3][['Ask', 'Bid']].to_string())  # this prints out mult columns

print(build_url('cvx'))
print(build_options_url('cvx'))