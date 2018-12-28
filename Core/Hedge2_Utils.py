"""
# -*- coding: utf-8 -*-
@author: robin.liu
"""

from Api.Huobi import HuobiServices as hbs
from Api.UniDax import UniDaxServices as uds, Constant as cons
import json
from pprint import *
import random
import time

'''
根据成交记录，进行对冲
'''

# 采用盯住成交单的方式，进行对冲
def get_outerTrade(user_id, c_l, hedged_id):
    '''
    :param user_id: 机器人user_id 用来方便成交记录
    :param c_l: 合约列表
    :param hedged_id: 已完成对冲的id号
    :return:
    '''

    result_hedgelist = [] # 返回结果

    for code in c_l:
        trade = uds.all_trade(symbol = code, pageSize=1000, page=0)

        if trade['msg'] != 'suc':
            print('获取成交记录 出错')
            return


        for tr in trade['data']['resultList']:
            ask_uId = tr['ask_user_id']
            bid_uId = tr['bid_user_id']
            id = tr['id']

            if ask_uId != bid_uId and id not in hedged_id[code]: # 出现没有对冲过的外部成交
                # 所需参数
                hedge_code = code
                hedge_vol = tr['volume']
                hedge_dirc = ''

                # 判断
                if ask_uId == user_id:  # 说明该笔成交中，处于卖方，需要做买对冲
                    hedge_dirc = 'BUY'
                elif bid_uId == user_id:
                    hedge_dirc = 'SELL'

                # 返回数据
                d = {'code': hedge_code, 'vol': hedge_vol, 'direction': hedge_dirc, 'id': id}
                result_hedgelist.append(d)

    return result_hedgelist
