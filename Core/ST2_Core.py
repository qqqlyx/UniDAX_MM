import sys
sys.path.append('D:\\Robin\\UniDAX_MM')

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

# ST2自成交策略，需要prepare配合运行
# 成交时间、金额由setting文件确认好

# 系统参数
#_coin =sys.argv[1]
_coin = 'btcusdt'

# 配置文件地址
_path = Tokens._path + '\\ST_setting'

# 参数：正在运行的日期
_runDay = ''

# 循环运行
while True:

    '''
    先判断是否有换日,并进行处理
    '''
    now = datetime.datetime.now()
    date = str(now.year) + str(now.month) + str(now.day)
    if _runDay != date:

        _runDay = date  # 赋值，同一天不会2次进入这一部分
        _trading_time = []  # _trading_time中包含所有触发交易的时间戳
        _trading_amount = []  # 保存所有成交金额

        # 读取成交配置文件
        path = _path + '\\' + date
        path += '\\' + _coin + '.csv'
        datas = pd.read_csv(path)

        # 保存时间数据
        t = datas.iloc[:, 0].tolist()
        for i in range(len(t)):
            tarry = time.strptime(t[i], "%Y-%m-%d %H:%M:%S")
            _trading_time.append(int(time.mktime(tarry)))  # 时间戳格式

        # 保存金额数据
        v = datas.iloc[:, 1].tolist()
        for i in range(len(v)):
            amount = round(float(v[i]) * 10000, 2)  # 由万元转换成元，只保留两位小数
            _trading_amount.append(amount)

    '''
    处理自交易,当现在时间>触发时间戳时，触发对应交易
    '''
    now = int(time.time()) # 当前时间戳
    if now - _trading_time[0] > 30: # 当时间超过计划30秒，则不要该计划了

        # 删除陈旧的计划，向前推进一步，此时不进行等待，直接循环，一直到找到最新的计划
        del _trading_amount[0]
        del _trading_time[0]
        print('忽略陈旧计划：' + str(_trading_amount[0]))
        continue

    # 以下是正常触发交易情况
    if now >= _trading_time[0]: # 触发交易

        quota = uds.market_dept(_coin, 'step0')
        if quota['msg'] != 'suc':
            print('获取行情失败，重新开始运行')
            continue

        # 自成交相关数据
        ask_p = float(quota['data']['tick']['asks'][0][0])
        bid_p = float(quota['data']['tick']['bids'][0][0])
        base_p = (ask_p + bid_p)/2  # 基准价格

        # 计算一跳的价格
        precis = cons.get_precision(_coin, 'price')
        one_step = 1 / (pow(10, precis))  # 一跳

        # 在基准价格上下2跳内，随机取价格
        r = random.randint(-2, 2)
        p = base_p + r * one_step
        _price = round(p, precis) # 最终下单价格

        # 这一单内要交易的金额
        _amount = _trading_amount[0]
        v = _amount / _price
        _vol = round(v, cons.get_precision(_coin, 'volume'))


        # 删除交易完成的内容
        del _trading_amount[0]
        del _trading_time[0]

        print(str(datetime.datetime.now()) + ',' + str(_amount) + ',' + str(_price) + ',' + str(_vol))

        '''
        执行交易
        '''
        # 报买单
        # mmu.do_trading(_coin, p, v, 'BUY')
        #
        # # 稍微等一下 避免报单过快
        # time.sleep(0.01)
        #
        # # 报卖单
        # mmu.do_trading(_coin, p, v, 'SELL')

        # 暂停1秒
        time.sleep(1)

    continue