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
    for info in hedge_info:
        code = info['code']
        vol = info['vol']
        dir = info['direction']
        hed2.do_trade_huobi(code,vol,dir)

        # 记录id
        code = hedge_info['code']
        id = hedge_info['id']
        hedged_id[code].append(id)

        # print
        pprint('已进行对冲：' + code + '  Vol=' + vol + ' DIR=' + dir)

    # 等50秒后再重复
    time.sleep(50)
