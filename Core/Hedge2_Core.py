import sys
sys.path.append('D:\\Robin\\UniDAX_MM')

import time
from Core import Hedge2_Utils as hed2
from pprint import *
import datetime
from Core import Tokens

'''
参数
'''
# 对冲合约
# CODE_LIST = ['ethusdt', 'etcusdt', 'btcusdt', 'ltcusdt', 'ethbtc', 'ltcbtc']
CODE_LIST = ['btcusdt']

# userID，需要与使用的账号严格
USER_ID = '10090'

'''
变量
'''
# 记录已检查完成的时间戳，只检查其后的订单
# 每个币种都有单独的时间记录
done_time = {}
for coin in CODE_LIST:
    done_time[coin] = int(round(time.time() * 1000)) # 毫秒级时间戳

while True:
    #print('begin' + str(datetime.datetime.now()))

    # 获取未对冲订单信息
    hedge_info, d_t = hed2.get_outerTrade(USER_ID, CODE_LIST, done_time)
    for key in d_t:
        if d_t[key] > done_time[key]:
            done_time[key] = d_t[key]
        elif d_t[key] == 0:
            print('查询成交单最新CTime = 0')

    # 进行对冲
    for info in hedge_info:
        code = info['code']
        vol = info['vol']
        direc = info['direction']
        id = info['id']

        hed2.do_trade_huobi(code, vol, direc)

        #loc_t = time.localtime(info['ctime'])
        #print('执行对冲， ' + code + '   Vol=' + vol + ' Dir=' + direc + '   外部成交时间=' + loc_t)
        print('执行对冲， ' + code + '   Vol=' + vol + ' Dir=' + direc)


    # print('finish' + str(datetime.datetime.now()))
    # 等10秒后再重复
    # time.sleep(3)
