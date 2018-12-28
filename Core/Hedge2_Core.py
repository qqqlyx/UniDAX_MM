import sys
sys.path.append('D:\\Robin\\UniDAX_MM')

import time
from Core import Hedge2_Utils as hed2
from pprint import *

'''
参数
'''
# 对冲合约
CODE_LIST = ['ethusdt', 'etcusdt', 'btcusdt', 'ltcusdt', 'ethbtc', 'ltcbtc']

# 基准仓位
UNI_BASE = {'eth': 10000000,
            'etc': 9000000,
            'btc': 10000000,
            'ltc': 10000000}

HUOBI_BASE = {'eth': 0,
              'etc': 0,
              'btc': 0,
              'ltc': 0}

# userID，需要与使用的账号严格
USER_ID = ''

'''
变量
'''
# 记录已完成对冲的订单
hedged_id = {}
for code in CODE_LIST:
    hedged_id[code] = []


while True:

    # 获取未对冲订单信息
    hedge_info = hed2.get_outerTrade(USER_ID, CODE_LIST, hedged_id)

    # 进行对冲
    pprint(hedge_info)

    # 记录id
    for info in hedge_info:
        code = hedge_info['code']
        id = hedge_info['id']
        hedged_id[code].append(id)

    # 等10秒后再重复
    time.sleep(10)
