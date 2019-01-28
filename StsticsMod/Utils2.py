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

Stock = 'btcusdt'
myID = '10090'

end_date = '2019-01-28 00:00:00'
endStamp = time.mktime(time.strptime(end_date, "%Y-%m-%d %H:%M:%S"))  # 获取时间戳
'''
逐日统计成交单
'''
_page = 0
_tradeTable = pd.DataFrame(columns=['coin','price','volume','amount','mySide','oppositeID'])
DoLoop = True

while (DoLoop):
    _page += 1
    _trades = []

    quota = uds.all_trade(Stock, pageSize=5000, page=_page)
    datas = quota['data']['resultList']

    if len(datas) == 0:
        DoLoop = False
        break

    for _data in datas:
        ctime = int(_data['ctime'] / 1000)
        if ctime >= endStamp:
            DoLoop = False
            break

        mySide = 'None'
        oppoID = ''
        if _data['ask_user_id'] != myID:
            mySide = 'Buy'
            oppoID = _data['ask_user_id']

        if _data['bid_user_id'] != myID:
            mySide = 'Sell'
            oppoID = _data['ask_user_id']

        if mySide != 'None':
            newRow = [Stock, _data['price'], _data['volume'], _data['deal_price'], mySide, oppoID]
            timeArray = time.localtime(ctime)
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            _tradeTable.loc[otherStyleTime] = newRow


    time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(datas[0]['ctime']))
    time2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(datas[-1]['ctime']))
    print('[%s] - [%s] finished!')
    
    continue

_tradeTable.to_csv('d:\\%s.csv' %(Stock), index=False)

