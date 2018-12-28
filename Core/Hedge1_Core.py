import sys
sys.path.append('D:\\Robin\\UniDAX_MM')

import time
from Core import Hedge1_Utils as hed

'''
参数
'''
# 对冲币种
COIN_LIST = ['eth', 'etc', 'btc', 'ltc']

# 基准仓位
UNI_BASE = {'eth': 10000000,
            'etc': 9000000,
            'btc': 10000000,
            'ltc': 10000000}

HUOBI_BASE = {'eth': 0,
              'etc': 0,
              'btc': 0,
              'ltc': 0}

while True:

    # 获取持仓信息
    uni = hed.get_unidax_position()
    huobi = hed.get_huobi_position()

    if len(uni) == 0 or len(huobi) == 0:
        time.sleep(3)
        continue

    # 对比仓位
    hedge_dict = hed.comparePosition(uni, huobi, UNI_BASE, HUOBI_BASE, COIN_LIST)

    # 获取火币行情


    # 等10秒后再重复
    time.sleep(10)
