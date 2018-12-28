"""
# -*- coding: utf-8 -*-
@author: robin.liu
"""
import sys
sys.path.append('D:\\Robin\\UniDAX_MM')


from Api.Huobi import HuobiServices as hbs
from Api.UniDax import UniDaxServices as uds, Constant as cons
import json
import random


# 获取unidax仓位
def get_unidax_position():
    # 返回结果是字典
    re_posi = {}

    # 读取unidax持仓
    try:
        posi = uds.account()
    except Exception as e:
        print('---->except<get_unidax_position><读取unidax持仓>: ' + e)

    if posi['msg'] != 'suc':
        print.error(posi)
    else:
        t1 = posi['data']['coin_list']
        for c in t1:
            coin = c['coin']
            vol = float(c['normal'])
            re_posi[coin] = vol

    return re_posi


# 获取huobi仓位
def get_huobi_position():
    # 返回结果是字典
    re_posi = {}
    # 读取持仓
    try:
        posi = hbs.get_balance()
    except Exception as e:
        print('---->except<get_huobi_position><读取HUOBI持仓>: ' + e)

    if posi['status'] != 'ok':
        print(posi)

    else:
        t1 = posi['data']['list']
        for c in t1:
            coin = c['currency']
            vol = float(c['balance'])
            # 货币资产把冻结资产和可交易资产分开，所以需要加起来才是总仓位
            if re_posi.__contains__(coin):
                re_posi[coin] += vol
            else:
                re_posi[coin] = vol

    return re_posi


# 总持仓量与基准持仓量进行对比
def comparePosition(posi_u, posi_h, base_posi_u, base_posi_h, coin_l):
    '''
    :param posi_u: unidax实际持仓
    :param posi_h: houbi实际持仓
    :param base_posi_u: 基准持仓
    :param base_posi_h:
    :param coin_l: 币列表
    :return:
    '''

    # 相关交易数据
    hedge_info = {}

    for c in coin_l:
        hedge_info['c'] = {'vol': 0.0, 'direct': ''}

        # 实际持仓 - 基准持仓
        diff_vol_uni = posi_u[c] - base_posi_u
        diff_vol_hb = posi_h[c] - base_posi_h
        diff_total = diff_vol_uni + diff_vol_hb

        # 额外多头仓位，需要做空
        if diff_total> 0:
            hedge_info['vol'] = diff_total
            hedge_info['direct'] = 'SELL'

        # 做多
        if diff_total < 0:
            hedge_info['vol'] = -diff_total
            hedge_info['direct'] = 'BUY'

    return hedge_info

# 对冲前判断，确认各币种是否需要对冲。并做好相应准备。
def pre_hedge(s_l):
    huobi_quota = {}
    try:
        for stock in s_l:
            r = hbs.get_depth(stock,'step0')
            huobi_quota[stock] = r
    except Exception as e:
        print('---->except<get_huobi_depth>', e)

    return huobi_quota


# 在火币下单, 因为对冲，所以直接下市价单
def do_trade_huobi(coin, he_v, he_d,log):
    sym = coin + 'usdt'
    if he_d == 'BUY':
        t = 'buy-market'
    else:
        t = 'sell-market'

    try:
    # 下单交易
        hbs.send_order(
            amount=he_v,
            source='api',
            symbol=sym,
            _type=t)

    except Exception as e:
        log.error('---->except<do_trade_huobi><下单交易>: ' + e)
    return