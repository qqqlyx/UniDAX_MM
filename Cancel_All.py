"""
# -*- coding: utf-8 -*-
@author: robin.liu
"""

# 删除所有已挂单
from UniDax import UniDaxServices as uds
from pprint import pprint

code = 'etcusdt'
all_order = uds.new_order(code)

pprint(all_order)
# for order in all_order['data']['resultList']:
#     if order['status'] == 1:
#         id = str(order['id'])
#         uds.cancel_order(code,id)