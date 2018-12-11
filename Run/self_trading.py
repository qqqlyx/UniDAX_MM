"""
# -*- coding: utf-8 -*-
@author: robin.liu
@github: qqqlyx
"""

# 用来自成交，刷成交单状况
import mmAction as mma
from UniDax import UniDaxServices as uds, Constant as cons
import threading
import logging
import json
from pprint import pprint
import datetime

# 参与自成交币种
#stock_list = ['ethusdt', 'btcusdt', 'ltcusdt', 'etcusdt', 'ethbtc', 'ltcbtc']
stock_list = ['ethusdt']
run_count = 1
last_quota = {}

# 定期调用做市程序
def core_timer():
    # log
    global run_count
    log.warning('Start Self-Trading, ' + str(run_count))
    # 读取市场行情
    get_quota()
    # 报单
    do_self_trading()
    # 定时循环
    global timer
    timer = threading.Timer(60, core_timer)
    timer.start()
    # log
    log.warning('End Self-Trading, ' + str(run_count))
    run_count += 1


def set_log():
    # 创建一个logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # 创建一个handler，用于写入日志文件
    date = datetime.datetime.now().strftime('%Y%m%d')
    logname = 'selfTrading_' + date
    fh = logging.FileHandler('log//' + logname)
    #fh = logging.FileHandler('D://test.log')
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

def get_quota():
    global last_quota
    for code in stock_list:
        quota = uds.market_dept(code, 'step0')
        last_quota[code] = quota
    return


# 按照买二卖二报价
def do_self_trading():
    for code in stock_list:
        quota = last_quota[code]

        # 主动卖
        price = quota['data']['tick']['asks'][2][0]
        vol = quota['data']['tick']['asks'][1][1]
        # 下单数量为1/5
        v = round(vol / 5, cons.get_precision(code, 'volume'))
        mma.do_trading(code, price, v, 'BUY', log)

        # 主动买
        price = quota['data']['tick']['bids'][2][0]
        vol = quota['data']['tick']['bids'][1][1]
        # 下单数量为1/5
        v = round(vol / 5, cons.get_precision(code, 'volume'))
        mma.do_trading(code, price, v, 'SELL', log)
    return


# log等级 info < warning < error
log = set_log()
timer = threading.Timer(1, core_timer)
timer.start()
