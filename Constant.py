"""
# -*- coding: utf-8 -*-
@author: robin.liu
"""

# 记录各类常数


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
