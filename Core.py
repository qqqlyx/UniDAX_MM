"""
# -*- coding: utf-8 -*-
@author: robin.liu
@github: qqqlyx
"""

import mmAction as mma
import threading
import logging
import json
from pprint import pprint

# 参与报价币种
# stock_list = ['ethusdt', 'btcusdt', 'ltcusdt', 'etcusdt', 'ethbtc', 'ltcbtc']
stock_list = ['etcusdt', 'ethusdt']
# stock_list = ['bchusdt']


# 定期调用做市程序
def core_timer():
    # log
    global run_count
    log.warning('Start MM Action, ' + str(run_count))
    # 全撤单
    mma.mm_cancel_all(stock_list, log)
    # 获取火币深度行情
    huobi_quota = mma.get_huobi_depth(stock_list, log)
    # 进行报单
    mma.mm_trading(huobi_quota, log)
    # 定时循环
    global timer
    timer = threading.Timer(15, core_timer)
    timer.start()
    # log
    log.warning('End MM Action, ' + str(run_count))
    run_count += 1


def set_log():
    # 创建一个logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler('D://test.log')
    fh.setLevel(logging.DEBUG)
    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)
    # 记录一条日志
    logger.info('robin mm begin')
    return logger


# log等级 info < warning < error
run_count = 1
log = set_log()
timer = threading.Timer(1, core_timer)
timer.start()

# 深度数据格式
# 例，huobi_quota['btcusdt']['tick']['asks'][0][0] = 卖一价
# 例，huobi_quota['btcusdt']['tick']['asks'][1][0] = 卖二价
# 例，huobi_quota['btcusdt']['tick']['asks'][1][1] = 卖二量
# for k in huobi_quota:
# pprint(k)





# etcusdt

#print (u' 获取行情深度数据 ')
#pprint (type(hbs.get_symbols()['data'][1]['base-currency']))
#pprint (hbs.get_symbols()['data'])

#pprint(hbs.get_depth('etcusdt','step0'))
# def fun_timer():
#     print('Hello Timer!')
#     global timer
#     timer = threading.Timer(5.5, fun_timer)
#     timer.start()
#
# timer = threading.Timer(1, fun_timer)
# timer.start()

#pprint(uds.account())

#pprint(uds.symbols())
#uds.get_ticker('ethusdt')
#uds.create_order('etcusdt','BUY','3.98','1.1')

# url = "http://api.unidax.com/exchange-open-api/open/api/create_order"
# headers = {
#         "Accept": "application/json",
#         'Content-Type': 'application/x-www-form-urlencoded'
#     }
# data={'side':'BUY',
#       'type':'1',
#       'volume':'1',
#       'price':'4.34',
#       'symbol':'etcusdt',
#       'fee_is_user_exchange_coin':'0',
#       'api_key':'c59256c6ae13e3d45b4c9386111a6ee4',
#       'time':'145705845710',
#       'sign':'a7c043600590280f38184fc50f6533dc'}
#
# r = requests.post(url=url, data=data,headers=headers)
# print(r.text)

#data1 = json.dumps(data)
#requests.post(url=url, data=data,headers={'Content-Type': 'application/x-www-form-urlencoded'})

#uds.new_order('btcusdt')