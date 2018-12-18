"""
# -*- coding: utf-8 -*-
@author: robin.liu
@github: qqqlyx
"""

# 用来自成交，刷成交单状况
import mmAction as mma
from UniDax import UniDaxServices as uds, Constant as cons
from Huobi import HuobiServices as hbs
import threading
import logging
import json
from pprint import pprint
import datetime
import random
import time

# 参与自成交币种
stock_list = ['ethusdt', 'btcusdt', 'ltcusdt', 'etcusdt', 'ethbtc', 'ltcbtc']
#stock_list = ['ethusdt']
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

    # log
    log.warning('End Self-Trading, ' + str(run_count))
    run_count += 1

    # 定时循环
    global timer
    timer = threading.Timer(60, core_timer)
    timer.start()


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

        # 使用火币报价
        quota_hb = hbs.get_depth(code, 'step0')
        a = 1
        if quota_hb['status'] != 'ok':
            return

        # 价格使用火币的价格进行计算
        price1 = float(quota_hb['tick']['asks'][0][0])
        price2 = float(quota_hb['tick']['bids'][0][0])
        price = (price1 + price2) / 2

        # 量使用UniDAX的量
        quota_uni = last_quota[code]
        # 如果没有盘口 就不做报单
        if len(quota_uni['data']['tick']['asks']) < 5:
            return

        if len(quota_uni['data']['tick']['bids']) < 5:
            return

        vol1 = quota_uni['data']['tick']['asks'][0][1]
        vol2 = quota_uni['data']['tick']['bids'][0][1]
        r = random.uniform(0, 1)
        vol = (vol1 + vol2) * r

        # 把价格和量格式化
        v = round(vol, cons.get_precision(code, 'volume'))
        p = round(price, cons.get_precision(code, 'price'))

        # 报买单
        mma.do_trading(code, p, v, 'BUY', log)

        # 稍微等一下 避免报单过快
        time.sleep(0.1)

        # 报卖单
        mma.do_trading(code, p, v, 'SELL', log)


        # quota = last_quota[code]
        # # 如果没有盘口 就不做报单
        # if len(quota['data']['tick']['asks']) < 10:
        #     return
        #
        # if len(quota['data']['tick']['bids']) < 10:
        #     return

        # # 在买、卖中随机
        # r = random.randint(0, 3)
        # if r == 1:
        #     # 主动卖
        #     price = quota['data']['tick']['asks'][1][0]
        #     vol = quota['data']['tick']['asks'][0][1]
        #     # 下单数量为卖一1/5
        #     v = round(vol / 5, cons.get_precision(code, 'volume'))
        #     mma.do_trading(code, price, v, 'BUY', log)
        # else:
        #     # 主动买
        #     price = quota['data']['tick']['bids'][1][0]
        #     vol = quota['data']['tick']['bids'][0][1]
        #     # 下单数量为1/5
        #     v = round(vol / 5, cons.get_precision(code, 'volume'))
        #     mma.do_trading(code, price, v, 'SELL', log)

        # UniDAX盘口报价
        # price1 = float(quota['data']['tick']['asks'][1][0])
        # price2 = float(quota['data']['tick']['bids'][1][0])
        # price = (price1 + price2) / 2
        # vol1 = quota['data']['tick']['asks'][0][1]
        # vol2 = quota['data']['tick']['bids'][0][1]
        # vol = (vol1 + vol2) * 0.4
        # v = round(vol, cons.get_precision(code, 'volume'))
        # p = round(price, cons.get_precision(code, 'price'))
        # mma.do_trading(code, p, v, 'BUY', log)
        # mma.do_trading(code, p, v, 'SELL', log)



    return


# log等级 info < warning < error
log = set_log()
timer = threading.Timer(1, core_timer)
timer.start()
