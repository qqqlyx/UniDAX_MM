from Api.Huobi import HuobiServices as hbs
from Api.UniDax import Constant as cons
from Api.UniDax import UniDaxServices as uds
from Api.Bitkub import BitkubServices as bks
from pprint import *
import time
import random
# t= uds.create_order(symbol='elfeth',side = 'BUY',price = 0.00000001,volume=1)
# print(t)
#
# if 1 == 1.0:
#     print(1)
# all_order = uds.new_order('wtceth')
# print(uds.new_order_2('wtceth'))

# t= uds.create_order(symbol='btcusdt',side = 'BUY',price = 7000,volume=0.5)
# print(t)
# t= uds.create_order(symbol='btcusdt',side = 'SELL',price = 7000,volume=0.5)
# print(t)
#
# t = uds.create_order(symbol='btcusdt',side = 'BUY',price = '6300',volume=0.5)
# print(t)
# # #
# all_order = uds.new_order_2('btcusdt', pageSize='1000', page='1')
# pprint(all_order)

# all = bks.getTrades('THB_INF',1000)
# pprint(all)
#
#print(random.)
# a = 'btcusdt'
# print(a[-3:])

#tem = uds.all_trade('infbtc', pageSize=1,page=1)
tem = uds.all_trade('infbtc', pageSize=100,page=1)
temp = tem['data']['resultList']

# kk = []
# for t in temp:
#     if t['ask_user_id'] != t['bid_user_id']:
#         kk.append(t)
#
# pprint('**=' + str(len(kk)))
pprint(temp)