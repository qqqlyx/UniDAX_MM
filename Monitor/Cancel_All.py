"""
# -*- coding: utf-8 -*-
@author: robin.liu
"""

# 删除所有已挂单
from Api.UniDax import UniDaxServices as uds
import json
from pprint import *

#codes = ['zilbtc']
#codes = ['ltcbtc','ltcusdt']
#
#codes = ['btcusdt']
#codes = ['etcusdt', 'ethbtc',]
#codes = ['zrxusdt', 'omgusdt']
#codes = ['mcoeth', 'gntusdt']
#codes = ['thetausdt', 'polyeth']
from Api.UniDax import Constant as cons
#codes = cons.stock_list
codes = ['zilbtc']
#ethusdt,btcusdt,ltcusdt,etcusdt,ethbtc,ltcbtc,wtceth,zrxusdt,omgusdt,mcoeth,gntusdt,aeeth,sntusdt,manaeth,linketh,zilbtc,btmusdt,abteth,elfeth,polyeth,thetausdt,dgdeth,paybtc



for code in codes:
    #pprint(code)
    haveOrder = True
    while haveOrder:
        all_order = uds.new_order_2(code,pageSize='10',page='1')
# t = uds.account()
    # pprint('code=%s, %s' %(code,all_order))
        if all_order['data']['count'] > 0:
            for order in all_order['data']['resultList']:
            # if order['status'] == 1:
                id = str(order['id'])
                r = uds.cancel_order(code, id)
                re = json.loads(r)
                # 打印log
                #if re['msg'] != 'suc':
                    #print(re)
        else:
            haveOrder = False
            print('*', code)

