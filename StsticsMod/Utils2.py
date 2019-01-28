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


'''
参数
'''
stock_list = ['ethusdt', 'btcusdt', 'ltcusdt', 'etcusdt', 'ethbtc', 'ltcbtc',
              'wtceth', 'zrxusdt', 'omgusdt', 'mcoeth', 'gntusdt', 'aeeth', 'manaeth']

end_date = '2019-01-28 00:00:00'
'''
逐日统计成交单
'''


def get_otherTrader(Stock, endStamp, myID):
    _page = 0
    _tradeTable = pd.DataFrame(columns=['coin', 'price', 'volume', 'amount', 'mySide', 'oppositeID'])
    DoLoop = True
    count = 0

    while (DoLoop):
        _page += 1
        _trades = []

        quota = uds.all_trade(Stock, pageSize=5000, page=_page)
        datas = quota['data']['resultList']

        if len(datas) == 0:
            DoLoop = False
            break

        for _data in datas:
            count += 1
            mySide = 'None'
            oppoID = ''

            ctime = int(_data['ctime'] / 1000)
            if ctime >= endStamp:
                DoLoop = False
                break

            if int(_data['ask_user_id']) not in myID:
                mySide = 'Buy'
                oppoID = _data['ask_user_id']

            if int(_data['bid_user_id']) not in myID:
                mySide = 'Sell'
                oppoID = _data['bid_user_id']

            if mySide != 'None':
                newRow = [Stock, _data['price'], _data['volume'], _data['deal_price'], mySide, oppoID]
                timeArray = time.localtime(ctime)
                otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                _tradeTable.loc[otherStyleTime] = newRow

        time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(datas[0]['ctime'] / 1000)))
        time2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(datas[-1]['ctime'] / 1000)))
        print('%s [%s] - [%s] finished!' % (Stock, time1, time2))

        continue

    _tradeTable.to_csv('d:\\%s.csv' % (Stock), index=False)
    f = open('d:\\lastCtime.txt', 'w')
    f.write('%s,%s,%s' %(end_date, Stock, count))
    f.close()

for s in stock_list:
    my = [10090,10091]
    es = time.mktime(time.strptime(end_date, "%Y-%m-%d %H:%M:%S"))  # 获取时间戳
    get_otherTrader(s, es, my)
