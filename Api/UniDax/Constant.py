"""
# -*- coding: utf-8 -*-
@author: robin.liu
"""

# 记录各类常数
stock_list = []
f = open('D:\\Robin\\UniDAX_MM\\Run\\PARAM.txt')
data = f.read()
d = data.split('\n')

envo = d[0].split('=')[1].replace(' ', '')

S = d[1].split('=')[1]
S2 = S.split(',')
for s in S2:
    stock_list.append(s.replace(' ', ''))


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
        if code == 'iostusdt':
            return 6
        if code == 'linketh':
            return 8
        if code == 'zilbtc':
            return 10
        if code == 'btmusdt':
            return 4
        if code == 'abteth':
            return 8
        if code == 'elfeth':
            return 8
        if code == 'polyeth':
            return 6
        if code == 'thetausdt':
            return 4
        if code == 'dgdeth':
            return 6
        if code == 'paybtc':
            return 8
        if code == 'infbtc':
            return 8
        if code == 'ontusdt':
             return 4
        if code == 'paxusdt':
            return 4

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
        if code == 'iostusdt':
            return 4
        if code == 'linketh':
            return 2
        if code == 'zilbtc':
            return 2
        if code == 'btmusdt':
            return 2
        if code == 'abteth':
            return 2
        if code == 'elfeth':
            return 0
        if code == 'polyeth':
            return 4
        if code == 'thetausdt':
            return 4
        if code == 'dgdeth':
            return 4
        if code == 'paybtc':
            return 2
        if code == 'infbtc':
            return 2
        if code == 'paxusdt':
            return 4
        if code == 'ontusdt':
            return 4