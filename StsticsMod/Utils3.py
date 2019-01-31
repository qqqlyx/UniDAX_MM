from Api.UniDax import Constant as cons
from Api.UniDax import UniDaxServices as uds
from Api.Huobi import HuobiServices as hbs
import random
import datetime
import os
from Core import Tokens
from pprint import *
import pandas as pd
import time

stock_list = ['btcusdt', 'ltcusdt', 'etcusdt', 'ethbtc', 'ltcbtc',
              'wtceth', 'zrxusdt', 'omgusdt', 'mcoeth', 'gntusdt', 'aeeth']

#stock_list = ['btcusdt', 'ltcusdt', 'etcusdt', 'ethbtc', 'ltcbtc']

stock_list = ['wtceth', 'zrxusdt', 'omgusdt', 'mcoeth', 'gntusdt', 'aeeth']

begin = '2019-01-01'
end = '2019-01-28'

myID = [10090, 10091]


'''
折半查询
'''
def half_find(_y ,_stock, _cons):

    left = 1
    right = _y

    while True:
        mid = (left + right) // 2
        quota = uds.all_trade(_stock, pageSize=5000, page=mid)

        if len(quota['data']['resultList']) == 0:
            break

        ctime = quota['data']['resultList'][0]['ctime']
        ctime = int(ctime) // 1000

        if ctime < _cons:
            left = mid
            print('修改左边为%s' %(left))
        else:
            right = mid
            print('修改右边为%s' % (right))

        # 退出条件
        if right - left <= 1:
            break
    print('返回结果%s' % (left))
    return left

'''
找到指定日期内, 日期前后包括 
所有成交单
'''
def get_SomeTrades(_stock, _begin, _end):

    #
    all_trades = []

    beginStamp = time.mktime(time.strptime(_begin, '%Y-%m-%d'))
    endStamp = time.mktime(time.strptime(_end, '%Y-%m-%d'))

    # 找到开始页
    quota = uds.all_trade(_stock, pageSize=1, page=1)
    count = int(quota['data']['count']) // 5000 + 1
    page = half_find(count ,_stock, beginStamp)


    # while True:
    #     quota = uds.all_trade(_stock, pageSize=5000, page=page)
    #     ctime = quota['data']['resultList'][-1]['ctime']
    #     ctime = int(ctime) // 1000
    #     if ctime > beginStamp:
    #         break
    #
    #     page += 1
    #     continue


    # 获取成交单
    while True:
        quota = uds.all_trade(_stock, pageSize=5000, page=page)
        all_trades.extend(quota['data']['resultList'])

        ctime = quota['data']['resultList'][-1]['ctime']
        ctime = int(ctime) // 1000
        if ctime > endStamp:
            break

        page += 1
        continue

    # 处理成交单
    trade_dict = {}
    for trade in all_trades:
        ctime = int(trade['ctime']) // 1000
        if ctime >= beginStamp and ctime <= endStamp:
            trade_dict[ctime] = trade
        continue

    return trade_dict

'''
根据获取的成交单，处理成Table
'''
trade_table = pd.DataFrame(columns=['date', 'coin', 'price', 'volume', 'amount', 'mySide', 'oppositeID'])

for stock in stock_list:
    print('%s 开始查找成交单' %(stock))
    data = get_SomeTrades(stock, _begin=begin, _end=end)
    print('%s 开始制作Table' % (stock))
    for _data in data.values():
        mySide = 'None'
        oppoID = ''
        ctime = int(_data['ctime']) // 1000

        if int(_data['ask_user_id']) not in myID:
            mySide = 'Buy'
            oppoID = _data['ask_user_id']

        if int(_data['bid_user_id']) not in myID:
            mySide = 'Sell'
            oppoID = _data['bid_user_id']

        if mySide != 'None':
            timeArray = time.localtime(ctime)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            newRow = [otherStyleTime, stock, _data['price'], _data['volume'], _data['deal_price'], mySide, oppoID]

            trade_table.loc['%s%s' %(otherStyleTime,stock)] = newRow
        continue
    continue

trade_table.to_csv('d:\\trade_%s_%s.csv' %(begin,end), index=False)



# t = get_SomeTrades('btcusdt', _begin='2018-09-01', _end='2018-10-01')
# pprint(t)

# t = uds.all_trade('btcusdt')
# time.localtime(1536718712)
# pprint(time.localtime(1536718712))