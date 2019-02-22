"""
# -*- coding: utf-8 -*-
@author: robin.liu

用来维护做市报价
"""
import sys
sys.path.append('D:\\Robin\\UniDAX_MM')

from Api.Huobi import HuobiServices as hbs
from Api.UniDax import Constant as cons
from Api.UniDax import UniDaxServices as uds
import json
import random
import time

'''
参数：火币成交量比例
'''
Ratio_byHuobi = 0.05

# 获取火币行情
def get_huobi_depth(s_l):
    huobi_quota = {}
    try:
        for stock in s_l:
            r = hbs.get_depth(stock,'step0')
            huobi_quota[stock] = r
    except Exception as e:
        print('---->except<get_huobi_depth>', e)

    return huobi_quota

# 依据火币行情进行下单
def mm_trading(huobi_q):
    # 遍历所有币种行情
    for code in huobi_q:
        try:
            # 最大单边报单数
            max_count = 5
            ask_count = 0
            bid_count = 0

            # 记录用来下单的行情
            ask_p = []
            ask_v = []
            bid_p = []
            bid_v = []

            # 遍历所有ask
            for asks in huobi_q[code]['tick']['asks']:
                # 判断下单数量
                if ask_count < max_count:
                    ask_count += 1
                else:
                    break

                # 如果仍在范围内，才进行下一步
                ask_p.append(asks[0])
                ask_v.append(asks[1])


            # 遍历所有bid
            for bids in huobi_q[code]['tick']['bids']:
                # 判断下单数量
                if bid_count <= max_count:
                    bid_count += 1
                else:
                    break

                price = bids[0]
                vol = bids[1]
                bid_p.append(price)
                bid_v.append(vol)


            # 火币行情数据
            if len(ask_p) < max_count:
                print('火币行情数据缺少: ' + str(code))

            # for i in range(len(ask_p)):
            #     log.info('huobi_quota_ASK: ' + str(code) + ', ' + str(ask_p[i]) + ', ' + str(ask_v[i]))
            #     log.info('huobi_quota_BID: ' + str(code) + ', ' + str(bid_p[i]) + ', ' + str(bid_v[i]))


            # 修改下单数据
            ask_p = get_ask_price(code, ask_p)
            ask_v = get_ask_vol(code, ask_v)
            bid_p = get_bid_price(code, bid_p)
            bid_v = get_bid_vol(code, bid_v)

            # 填充报单
            ask_p = get_more_ask_price(code, ask_p)
            ask_v = get_more_ask_vol(code, ask_v)
            bid_p = get_more_bid_price(code, bid_p)
            bid_v = get_more_bid_vol(code, bid_v)

            # for i in range(len(ask_p)):
            #     log.info('mm_ASK: ' + str(code) + ', ' + str(ask_p[i]) + ', ' + str(ask_v[i]))
            #     log.info('mm_BID: ' + str(code) + ', ' + str(bid_p[i]) + ', ' + str(bid_v[i]))

            # 实际交易下单
            od_id = []
            for i in range(len(ask_p)):
                r = do_trading(code,ask_p[i],ask_v[i],'SELL')
                od_id.append(r)

            for i in range(len(bid_p)):
                r = do_trading(code,bid_p[i],bid_v[i],'BUY')
                od_id.append(r)

        except Exception as e:
            print('---->except<mm_trading>: ' + str(code), e)
    return

# 修改ask下单价格
def get_ask_price(code, a_p):
    r = random.uniform(0.004, 0.005)
    new = []
    for tem in a_p:
        p = tem*(1+r) # ask订单的price*[1+（0.01-0.015）]随机数，
        p = round(p, cons.get_precision(code,'price'))
        new.append(p)
    return new

# 修改ask下单数量
def get_ask_vol(code, a_v):
    r = float(Ratio_byHuobi * random.uniform(0.8, 1.2))

    #print('r',r)

    new = []
    for tem in a_v:
        v = float(tem * r)  # amount*（0.015-0.05)的范围随机数
        precis = cons.get_precision(code, 'volume')
        v = round(v, precis)

        #print('v=',v)
        if v == 0.0:
            v = tick = 1 / (pow(10, precis))

        new.append(v)
    return new

# 修改bid下单价格
def get_bid_price(code, a_p):
    r = random.uniform(0.004, 0.005)
    new = []
    for tem in a_p:
        p = tem*(1-r) # bid订单的price*[1-（0.01-0.015）随机数]
        p = round(p, cons.get_precision(code,'price'))
        new.append(p)
    return new

# 修改bid下单数量
def get_bid_vol(code, b_v):
    r = float(Ratio_byHuobi * random.uniform(0.8, 1.2))

    new = []
    for tem in b_v:
        v = float(tem * r)  # amount*（0.015-0.05)的范围随机数
        precis = cons.get_precision(code, 'volume')

        v = round(v, precis)

        if v == 0.0:
            v = tick = 1 / (pow(10, precis))

        new.append(v)
    return new

# 填充askprice
# 现在填充报单是15个
def get_more_ask_price(code, a_p):
    new = a_p
    for i in range(15):
        r = random.randint(0, 6) # 每一单1,2,3,4,5中随机跳
        precis = cons.get_precision(code, 'price')
        tick = 1/(pow(10,precis))
        p = a_p[-1] + r * tick

        p = round(p, cons.get_precision(code, 'price'))
        new.append(p)
    return new

# 填充ask vol
def get_more_ask_vol(code, a_v):
    new = a_v
    for i in range(15):
        r = random.uniform(0.5, 10)  # 量也随机, 根据买一卖一量进行扩大
        v = (a_v[0] + a_v[1] + a_v[2]) * r

        v = round(v, cons.get_precision(code, 'volume'))
        new.append(v)
    return new


# 填充 bidprice
def get_more_bid_price(code, b_p):
    new = b_p
    for i in range(15):
        r = random.randint(0, 6)  # 每一单1,2,3,4,5中随机跳
        precis = cons.get_precision(code, 'price')
        tick = 1 / (pow(10, precis))
        p = b_p[-1] - r * tick

        p = round(p, cons.get_precision(code, 'price'))
        new.append(p)
    return new

# 填充bid vol
def get_more_bid_vol(code, b_v):
    new = b_v
    for i in range(15):
        r = random.uniform(0.5, 10) # 量也随机
        v = (b_v[0] + b_v[1] + b_v[2]) * r
        v = round(v, cons.get_precision(code, 'volume'))
        new.append(v)
    return new


# 实际下单，返回订单id
def do_trading(code, price, vol, direction):

    result = '000'
    # test
    #vol = '0.01'
    try:
        time.sleep(0.1)
        r = uds.create_order(code, direction, price, vol)
        re = json.loads(r)  # 使用eval会报错，因次用了json方法转换str -> dict

        # 打印log
        if re['msg'] != 'suc':
            print('%s CODE=%s  D=%s  P=%s  V=%s' %(re, code, direction, price,vol))
            result = '000'
        else:
            # log.info(re)
            result = re['data']['order_id']
            
    except Exception as e:
        print('---->except<do_trading>: ' + str(code), e)

    return result




# 撤掉UniDAX全部挂单
def mm_cancel_all(stock_list, all_order):
    for code in stock_list:
        # 如果报单的key中有该代码，则进入撤单
        if all_order.__contains__(code):
            orders = all_order[code]

            if orders['data']['count'] > 0:
                for order in orders['data']['resultList']:
                    #if order['status'] == 1:
                    id = str(order['id'])
                    r = uds.cancel_order(code, id)
                    re = json.loads(r)  # 使用eval会报错，因次用了json方法转换str -> dict

    return

# 获取全部订单
def mm_get_all_order(stock_list):
    all_order = {}
    for code in stock_list:
        orders = uds.new_order(code)
        # # 打印log
        # if orders['msg'] != 'suc':
        #     log.error(orders)
        # else:
        #     log.info(orders)

        # 记录orders
        all_order[code] = orders

    return all_order
