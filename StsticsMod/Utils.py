"""
# -*- coding: utf-8 -*-
@author: robin.liu

统计订单相关信息
"""

from Api.UniDax import Constant as cons
from Api.UniDax import UniDaxServices as uds
from Api.Huobi import HuobiServices as hbs
import random
import datetime
import os
from Core import Tokens
from pprint import *
import time

'''
统计Unidax报单和成交情况
'''

# 根据coin和start_date, end_date 获取所有成交单
# date格式是str '2019-01-01'
# 返回的格式是dict
def get_allTradeOrders(_coin, start_date, end_date):
    beginStamp = time.mktime(time.strptime(start_date, "%Y-%m-%d"))  # 获取时间戳
    endStamp = time.mktime(time.strptime(end_date, "%Y-%m-%d"))  # 获取时间戳
    runDay = int((endStamp - beginStamp) / 86400) + 1  # 开始到结束共有几天，包括前后

    # 获取所有tradeOrders
    t = uds.all_trade(_coin, pageSize='1', page=1)
    ps = str(t['data']['count'])
    data = uds.all_trade(_coin, pageSize=ps, page=1)
    TradeOrders = data['data']['resultList']

    # 按日期
    DayOrders = {}

    for i in range(runDay):
        stampRange = [beginStamp + 86400 * i, beginStamp + 86400 * (i + 1)]
        todayOrder = []

        for n in range(len(TradeOrders)):
            order = TradeOrders[n]
            ctime = order['ctime'] / 1000
            if ctime >= stampRange[0] and ctime <= stampRange[1]:
                todayOrder.append(order)
        lt = time.localtime(beginStamp + 86400 * i)
        dt = time.strftime("%Y-%m-%d",lt)
        DayOrders[dt] = todayOrder

    return DayOrders
    #print(runDay)

# t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# print(str(t))
temp = get_allTradeOrders('btcusdt', '2018-09-15','2018-09-16')
# lt = time.localtime(1537093932)
# dt = time.strftime("%Y-%m-%d",lt)
# print(dt)
sum = 0
for trade in temp['2018-09-15']:
    sum += float(trade['deal_price'])
print(sum)