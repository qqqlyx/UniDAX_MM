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

# UniDAX查询最新成交单比较麻烦
def get_lastTrade(code):
    # 先查询出总成交单数量
    trade = uds.all_trade(symbol=code, pageSize=1, page=1)
    if trade['msg'] != 'suc':
        print('获取成交记录 出错')
        return
    t_count = int(trade['data']['count'])

    # 再计算要查询的页面
    paS = 50
    pa = int(t_count / paS)

    trade = uds.all_trade(symbol=code, pageSize=paS, page=pa)
    if trade['msg'] != 'suc':
        print('获取成交记录 出错')
        return
    list1 = trade['data']['resultList']

    trade = uds.all_trade(symbol=code, pageSize=paS, page=(pa + 1))
    if trade['msg'] != 'suc':
        print('获取成交记录 出错')
        return
    list2 = trade['data']['resultList']
    return list1 + list2


# 采用盯住成交单的方式，进行对冲
def get_outerTrade(user_id, c_l, done_t):
    '''
    :param user_id: 机器人user_id 用来方便成交记录
    :param c_l: 合约列表
    :param done_t: 此时间之前的订单，已经对冲完成
    :return:
    '''

    result_hedgelist = [] # 返回结果
    result_lastCtim = {}  # 返回查询的成交单中最新时间

    for code in c_l:
        # 查询
        quotaList = get_lastTrade(code)
        result_lastCtim[code] = 0

        #
        for tr in quotaList:
            ask_uId = tr['ask_user_id']
            bid_uId = tr['bid_user_id']
            id = tr['id']
            ctime = tr['ctime']


            if ctime > done_t[code]: # 如果订单时间，在done_t时间戳之后，才考虑检查
                #print(str(ctime))

                if ask_uId != bid_uId: # 出现外部成交
                    # 所需参数
                    hedge_code = code
                    hedge_vol = tr['volume']
                    hedge_dirc = ''

                    # 判断
                    if str(ask_uId) == str(user_id):  # 说明该笔成交中，处于卖方，需要做买对冲
                        hedge_dirc = 'BUY'
                    elif str(bid_uId) == str(user_id):
                        hedge_dirc = 'SELL'

                    # 返回数据
                    d = {'code': hedge_code,
                         'vol': hedge_vol,
                         'direction': hedge_dirc,
                         'id': id,
                         'ask_uId': ask_uId,
                         'bid_uId': bid_uId,
                         'ctime':ctime}
                    result_hedgelist.append(d)

            if ctime > result_lastCtim[code]:
                result_lastCtim[code] = ctime

    return result_hedgelist, result_lastCtim


# 在火币下单, 因为对冲，所以直接下市价单
# 使用限价单
def do_trade_huobi(code, he_v, he_d):
    h_quota = hbs.get_depth(code,'step0')

    if he_d == 'BUY':
        p = h_quota['tick']['asks'][0][0]
        t = 'buy-limit'
    elif he_d == 'SELL':
        p = h_quota['tick']['bids'][0][0]
        t = 'sell-limit'

    try:
    # 下单交易
        t = hbs.send_order(
            amount=float(he_v),
            source='api',
            symbol=code,
            _type=t,
            price=p)
        #print(t)
    except Exception as e:
        print('---->except<do_trade_huobi><下单交易>: ' + e)
    return