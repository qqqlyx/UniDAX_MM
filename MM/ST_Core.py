import time
from MM import MM_Utils as mmu
import sys
from UniDax import UniDaxServices as uds, Constant as cons
from Huobi import HuobiServices as hbs
import random

stock_list = ['ethusdt', 'btcusdt', 'ltcusdt', 'etcusdt', 'ethbtc', 'ltcbtc']

while True:
    for code in stock_list:
        # 使用火币报价
        quota_hb = hbs.get_depth(code, 'step0')
        a = 1
        if quota_hb['status'] != 'ok':
            break

        # 价格使用火币的价格进行计算
        price1 = float(quota_hb['tick']['asks'][0][0])
        price2 = float(quota_hb['tick']['bids'][0][0])
        price = (price1 + price2) / 2

        # 量使用UniDAX的量
        quota_uni = last_quota[code]
        # 如果没有盘口 就不做报单
        if len(quota_uni['data']['tick']['asks']) < 4:
            break

        if len(quota_uni['data']['tick']['bids']) < 4:
            break

        vol1 = quota_uni['data']['tick']['asks'][0][1]
        vol2 = quota_uni['data']['tick']['bids'][0][1]
        r = random.uniform(0, 1)
        vol = (vol1 + vol2) * r

        # 把价格和量格式化
        v = round(vol, cons.get_precision(code, 'volume'))
        p = round(price, cons.get_precision(code, 'price'))

        # 报买单
        mmu.do_trading(code, p, v, 'BUY')

        # 稍微等一下 避免报单过快
        time.sleep(0.1)

        # 报卖单
        mmu.do_trading(code, p, v, 'SELL')

    # 等55秒后再重复
    time.sleep(55)

    continue


    def get_quota():
        global last_quota
        for code in stock_list:
            quota = uds.market_dept(code, 'step0')
            last_quota[code] = quota
        return

