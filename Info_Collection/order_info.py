"""
# -*- coding: utf-8 -*-
@author: robin.liu

统计订单相关信息
"""

from UniDax import UniDaxServices as uds, Constant as cons
import json


def do_analyze():
    trades = uds.all_trade('btcusdt')
    a = 1
    return trades

do_analyze()