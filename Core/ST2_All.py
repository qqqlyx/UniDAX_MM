import sys
sys.path.append('D:\\Robin\\UniDAX_MM')
#sys.path.append('D:\\Github\\UniDAX_MM')

import time
import pandas as pd
from Core import MM_Utils as mmu
from Api.UniDax import Constant as cons
from Api.UniDax import UniDaxServices as uds
from Api.Huobi import HuobiServices as hbs
import random
import datetime
import os
from Core import Tokens
from pprint import *

# ST2自成交策略，需要prepare配合运行
# 成交时间、金额由setting文件确认好


# 配置文件地址
_path = Tokens._path + '\\ST_setting'

# 参数：正在运行的日期
_runDay = ''

# 记录火币行情
HuobiQuota = {}

print('begin: all')

# 循环运行
while True:

    '''
    先判断是否有换日,并进行处理
    '''
    now = datetime.datetime.now()
    date = str(now.year) + str(now.month) + str(now.day)
    _last_quotaTime = now

    if _runDay != date:
        _runDay = date  # 赋值，同一天不会2次进入这一部分
        _trading_time = []  # _trading_time中包含所有触发交易的时间戳
        _trading_amount = []  # 保存所有成交金额
        _trading_code = [] # 保存交易的合约


        # 读取成交配置文件
        readpath = _path + '\\' + date + '\\all.csv'
        _trading_plan = pd.read_csv(readpath)

        # 保存时间数据
        t = _trading_plan.loc[:, 'Time'].tolist()
        for i in range(len(t)):
            tarry = time.strptime(t[i], "%Y-%m-%d %H:%M:%S")
            _trading_time.append(int(time.mktime(tarry)))  # 时间戳格式
            continue

        # 保存金额数据
        v = _trading_plan.loc[:, 'Amount'].tolist()
        for i in range(len(v)):
            amount = round(float(v[i]), 2)  # 只保留两位小数
            _trading_amount.append(amount)
            continue

        # 保存金额数据
        c = _trading_plan.loc[:, 'Code'].tolist()
        for i in range(len(c)):
            code = c[i]  # 代码
            _trading_code.append(code)
            continue

        # 保存一份不重复的代码，并且要有btc和eth
        _code_set = set(_trading_code)
        _code_set.add('btcusdt')
        _code_set.add('ethusdt')


    '''
    处理自交易,当现在时间>触发时间戳时，触发对应交易
    '''
    now = int(time.time()) # 当前时间戳
    if now - _trading_time[0] > 30: # 当时间超过计划30秒，则不要该计划了

        # 删除陈旧的计划，向前推进一步，此时不进行等待，直接循环，一直到找到最新的计划
        del _trading_amount[0]
        del _trading_time[0]
        del _trading_code[0]
        print('忽略陈旧计划：' + str(_trading_amount[0]))
        continue

    # 每分钟更新一次行情
    ts = datetime.datetime.now() - _last_quotaTime
    if ts.seconds >= 60 or len(HuobiQuota) == 0:
        _last_quotaTime = datetime.datetime.now()
        for coin in _code_set:
            HuobiQuota[coin] = hbs.get_depth(coin, 'step0')

    # 以下是正常触发交易情况
    if now >= _trading_time[0]: # 触发交易
        _code = _trading_code[0]
        quota = HuobiQuota[code]
        # if quota['msg'] != 'suc':
        #     print('获取行情失败，重新开始运行')
        #     continue

        # 自成交相关数据
        ask_p = float(quota['tick']['asks'][0][0])
        bid_p = float(quota['tick']['bids'][0][0])
        base_p = (ask_p + bid_p)/2  # 基准价格

        # 计算一跳的价格
        precis = cons.get_precision(_code, 'price')
        one_step = 1 / (pow(10, precis))  # 一跳

        # 在基准价格上下2跳内，随机取价格
        r = random.randint(-4, 4)
        p = base_p + r * one_step
        _price = round(p, precis) # 最终下单价格

        # 这一单内要交易的金额, usdt
        _amount = _trading_amount[0]

        # 数量计算
        _volume = 0

        # 解析code，分为 usdt/btc/eth
        if _code[-3:] == 'btc':
            try:
                btcq = HuobiQuota['btcusdt']
                p = float(btcq['tick']['asks'][0][0]) + float(btcq['tick']['bids'][0][0])
                p = p/2
                v = _amount / (_price * p)
            except Exception as e:
                print('----><计算报单数量>: ', e)
        elif _code[-3:] == 'eth':
            try:
                btcq = HuobiQuota['ethusdt']
                p = float(btcq['tick']['asks'][0][0]) + float(btcq['tick']['bids'][0][0])
                p = p / 2
                v = _amount / (_price * p)
            except Exception as e:
                print('----><计算报单数量>: ', e)
        else:
            v = _amount / _price

        # 数量标准化
        _volume = round(v, cons.get_precision(_code, 'volume'))


        # 删除交易完成的内容
        del _trading_amount[0]
        del _trading_time[0]
        del _trading_code[0]

        s = str(datetime.datetime.now()) + ', code=' + str(_code)+ ', amount=' + str(_amount)+ ', price=' + str(_price)+ ', volume=' + str(_volume)
        if _code[-3:] == 'btc':
            s += ', btc_price=' + str(p)
        elif _code[-3:] == 'eth':
            s += ', eth_price=' + str(p)


        print(s)

        '''
        执行交易
        '''
        if _volume > 0:
            # 报买单
            mmu.do_trading(_code, _price, _volume, 'BUY')

            # 稍微等一下 避免报单过快
            time.sleep(0.01)

            # 报卖单
            mmu.do_trading(_code, _price, _volume, 'SELL')

        # # 暂停1秒
        # time.sleep(1)

    continue