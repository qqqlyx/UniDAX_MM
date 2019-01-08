import datetime
from Api.UniDax import Constant as cons
from Api.UniDax import UniDaxServices as uds
from Api.Huobi import HuobiServices as hbs
from pprint import *
import threading
import time
import random
import pandas as pd

stock_list = ['ethusdt', 'btcusdt', 'ltcusdt', 'etcusdt', 'ethbtc', 'ltcbtc',
              'wtceth', 'zrxusdt', 'omgusdt', 'mcoeth', 'gntusdt','aeeth']

_date = datetime.datetime(year=2019,month=1,day=3,hour=17,minute=28,second=0)



for code in stock_list:
    _code_info = {'amount': [],
                  'close': [],
                  'count': [],
                  'high': [],
                  'low': [],
                  'open': [],
                  'vol': []}
    _pd = pd.DataFrame(columns=list(_code_info.keys()))

    datas = hbs.get_kline(code, '60min', 2000)
    for _quota in datas['data']:

        temp = [_quota['amount'],_quota['close'],_quota['count'],_quota['high'],_quota['low'],_quota['open'],_quota['vol']]
        timeArray = time.localtime(_quota['id'])
        _time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        _pd.loc[str(_time)] = temp

    path = 'D:\\GitHub\\UniDAX_MM\\Huobi_History\\' + code + '_hours.csv'
    _pd.to_csv(path)

    ###
    datas = hbs.get_kline(code, '1day', 2000)
    for _quota in datas['data']:
        temp = [_quota['amount'], _quota['close'], _quota['count'], _quota['high'], _quota['low'], _quota['open'],
                _quota['vol']]
        timeArray = time.localtime(_quota['id'])
        _time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        _pd.loc[str(_time)] = temp

    path = 'D:\\GitHub\\UniDAX_MM\\Huobi_History\\' + code + '_day.csv'
    _pd.to_csv(path)


    #
    # _pd = pd.DataFrame()
    # _pd['amount'] = _code_info['amount']
    # _pd['amount'] = _code_info['amount']
