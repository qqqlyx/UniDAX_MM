import sys
sys.path.append('D:\\Robin\\UniDAX_MM')

import time
from Core import MM_Utils as mmu
from Api.UniDax import Constant as cons
from Api.UniDax import UniDaxServices as uds
from Api.Huobi import HuobiServices as hbs
import random

stock_list = ['ethusdt', 'btcusdt', 'ltcusdt', 'etcusdt', 'ethbtc', 'ltcbtc']

# stock_list = ['ethusdt', 'btcusdt', 'ltcusdt', 'etcusdt', 'ethbtc', 'ltcbtc',
#               'zrxusdt','omgusdt','mcousdt','manausdt','sntusdt',
#               'wtcusdt','gntusdt','cmtusdt','aeusdt','elfusdt']

# 完成一轮报单的时间 秒
turn_total_time = 60

# 为了增加真实性，此处报单顺序会随机打乱
while True:
    # 把stock顺序打乱
    random.shuffle(stock_list)

    # 再进行报单
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
        quota_uni = uds.market_dept(code, 'step0')

        # 如果没有盘口 就不做报单
        if len(quota_uni['data']['tick']['asks']) < 6:
            break

        if len(quota_uni['data']['tick']['bids']) < 6:
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
        time.sleep(0.01)

        # 报卖单
        mmu.do_trading(code, p, v, 'SELL')

        # 报单后等随机时间，以使得各合约成交时间不同
        # 等待时间根据‘一轮报单时间’参数确定
        count = len(stock_list)
        each_time = int(turn_total_time / count)
        r = random.randint(0, 2 * each_time)
        time.sleep(r)

    continue


    def get_quota():
        global last_quota
        for code in stock_list:
            quota = uds.market_dept(code, 'step0')
            last_quota[code] = quota
        return

