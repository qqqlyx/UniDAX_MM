import sys
sys.path.append('D:\\Robin\\UniDAX_MM')

import time
from Core import MM_Utils as mmu
from Api.UniDax import Constant as cons
from Api.UniDax import UniDaxServices as uds
from Api.Bitkub import BitkubServices as bks
import random
from Core import Tokens

# 完成一轮报单的时间 秒
turn_time = 120
ratio = 0.6
max_vol = 30
#
last_time = time.time()
while True:
    turn_begin = time.time()

    try:
        d = bks.getTrades('THB_INF', 10)
        quota = d['result']
        total_vol = 0
        for q in quota:
            t = q[0]
            vol = q[2]
            if t > last_time:
                total_vol += vol

        last_time = quota[0][0]

        order_vol_total = total_vol * 0.6
        #
        quota_uni = uds.market_dept('infbtc', 'step0')
        # 如果没有盘口 就不做报单
        if len(quota_uni['data']['tick']['asks']) < 3:
            break

        if len(quota_uni['data']['tick']['bids']) < 3:
            break

        # 价格使用UniDAX的价格进行计算
        price1 = float(quota_uni['data']['tick']['asks'][0][0])
        price2 = float(quota_uni['data']['tick']['bids'][0][0])
        order_price = (price1 + price2) / 2

        # 把价格和量格式化
        v = round(order_vol_total, cons.get_precision('infbtc', 'volume'))
        p = round(order_price, cons.get_precision('infbtc', 'price'))

        # 报卖单
        if v > 0:
            t = mmu.do_trading('infbtc', p, v, 'SELL')
            # 稍微等一下 避免报单过快
            time.sleep(0.01)
            if t != '000':
                # 报买单
                mmu.do_trading('infbtc', p, v, 'BUY')

        # 等待
        while True:
            if time.time() > (turn_begin + turn_time):
                break
            time.sleep(1)
    except Exception as e:
        pass

    continue