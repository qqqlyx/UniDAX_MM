"""
# -*- coding: utf-8 -*-
@author: robin.liu
"""

# 删除所有已挂单
from Api.UniDax import UniDaxServices as uds
import json

codes = ['ethusdt', 'btcusdt', 'ltcusdt', 'etcusdt', 'ethbtc', 'ltcbtc']
#codes = ['ltcbtc','ltcusdt']



for code in codes:
    all_order = uds.new_order(code)
# t = uds.account()
    #pprint(all_order)
    if all_order['data']['count'] > 0:
        for order in all_order['data']['resultList']:
        # if order['status'] == 1:
            id = str(order['id'])
            r = uds.cancel_order(code, id)
            re = json.loads(r)
            # 打印log
            if re['msg'] != 'suc':
                print(re)
