"""
# -*- coding: utf-8 -*-
@author: robin.liu
"""

# 记录各类常数
# 'zrxusdt','omgusdt','mcoeth','manaeth','sntusdt',
#               'wtceth','gntusdt','cmtusdt','aeeth']

# 获取交易精度 type：price、volume
def get_precision(code, type):
    if type == 'price':
        if code == 'etcusdt':
            return 2
        if code == 'ltcusdt':
            return 2
        if code == 'btcusdt':
            return 2
        if code == 'ethusdt':
            return 2
        if code == 'ltcbtc':
            return 6
        if code == 'ethbtc':
            return 8
        if code == 'bchusdt':
            return 2

        if code == 'zrxusdt':
            return 4
        if code == 'omgusdt':
            return 4
        if code == 'mcoeth':
            return 6
        if code == 'manaeth':
            return 8
        if code == 'sntusdt':
            return 6
        if code == 'wtceth':
            return 6
        if code == 'gntusdt':
            return 4
        if code == 'cmtusdt':
            return 4
        if code == 'aeeth':
            return 6

    if type == 'volume':
        if code == 'etcusdt':
            return 2
        if code == 'ltcusdt':
            return 3
        if code == 'btcusdt':
            return 4
        if code == 'ethusdt':
            return 3
        if code == 'ltcbtc':
            return 2
        if code == 'ethbtc':
            return 3
        if code == 'bchusdt':
            return 2

        if code == 'zrxusdt':
            return 2
        if code == 'omgusdt':
            return 4
        if code == 'mcoeth':
            return 4
        if code == 'manaeth':
            return 1
        if code == 'sntusdt':
            return 4
        if code == 'wtceth':
            return 4
        if code == 'gntusdt':
            return 4
        if code == 'cmtusdt':
            return 4
        if code == 'aeeth':
            return 4
