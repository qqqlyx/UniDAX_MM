import datetime
from Api.UniDax import Constant as cons
from Api.UniDax import UniDaxServices as uds
from Api.Huobi import HuobiServices as hbs
from pprint import *
import threading
import time
import random
import pandas as pd

coin = 'gntusdt'
myID = '10090'

t = uds.all_trade(coin,pageSize='1',page=1)
ps = int(t['data']['count'])

SellList = []
BuyList = []

if ps > 5000:
    times = int(ps / 5000) + 1
    for i in range(times):
        data = uds.all_trade(coin,pageSize=ps,page=i)
        trades = data['data']['resultList']
        for trade in trades:
            if str(trade['bid_user_id']) != myID:
                SellList.append(trade)
            if str(trade['ask_user_id']) != myID:
                BuyList.append(trade)

SellVol = 0
BuyVol = 0
SellAmount = 0
BuyAmount = 0
for sell in SellList:
    SellAmount += float(sell['deal_price'])
    SellVol += float(sell['volume'])

for buy in BuyList:
    BuyAmount += float(buy['deal_price'])
    BuyVol += float(buy['volume'])

print(SellAmount)
print(SellVol)
print(BuyAmount)
print(BuyVol)


#pprint(t)
