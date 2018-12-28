import sys
sys.path.append('D:\\Robin\\UniDAX_MM')

import time
from Core import Hedge2_Utils as hed2
from pprint import *
import datetime

'''
参数
'''
# 对冲合约
# CODE_LIST = ['ethusdt', 'etcusdt', 'btcusdt', 'ltcusdt', 'ethbtc', 'ltcbtc']
CODE_LIST = ['btcusdt']

# userID，需要与使用的账号严格
USER_ID = '10090'

'''
变量
'''
# 记录已完成对冲的订单
hedged_id = {}
for code in CODE_LIST:
    hedged_id[code] = []


while True:
    #print('begin' + str(datetime.datetime.now()))

    # 获取未对冲订单信息
    hedge_info = hed2.get_outerTrade(USER_ID, CODE_LIST, hedged_id)

    # 进行对冲
    for info in hedge_info:
        code = info['code']
        vol = info['vol']
        direc = info['direction']
        id = info['id']


        hed2.do_trade_huobi(code,vol,direc)
        print('执行对冲， ' + code + '   Vol=' + vol + ' Dir=' + direc)

        # 记录id
        hedged_id[code].append(id)

    # print('finish' + str(datetime.datetime.now()))
    # 等10秒后再重复
    # time.sleep(3)
