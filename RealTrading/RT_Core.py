import sys
sys.path.append('D:\\Robin\\UniDAX_MM')

import time
from Core import MM_Utils as mmu
from Api.UniDax import Constant as cons
from Api.UniDax import UniDaxServices as uds
from pprint import *
import RealTrading.DingReport as Ding
import datetime

stock_list = cons.stock_list
firstTime = True


#
lastcTime = 0

while True:
    this_run_total_trades = {}
    big_trades = {}

    if firstTime:
        # 第一次不做任何处理
        lastcTime = time.time()
        firstTime = False

    else:
        for code in stock_list:
            #
            real_tradings = []
            # 获取最新成交数据
            tem = uds.all_trade(code, pageSize=1, page=1)
            count = int(tem['data']['count'])
            count += 1

            fpage = 1
            if count > 2000:
                fpage = count // 2000 + 1

            all_trades = uds.all_trade(code, pageSize=2000, page=fpage)
            trading_list = all_trades['data']['resultList']

            if fpage > 1:
                all_trades = uds.all_trade(code, pageSize=2000, page=fpage-1)
                trading_list.extend(all_trades['data']['resultList'])

            for trading in trading_list:
                if trading['ask_user_id'] != trading['bid_user_id']:
                    real_tradings.append(trading)

            # 按时间过滤
            last_real_tradings = []
            for rt in real_tradings:
                ctime = rt['ctime'] / 1000
                if ctime > lastcTime:
                    last_real_tradings.append(rt)

            # 统计
            if len(last_real_tradings) > 0:
                total_amount = 0
                total_user_amount = {}

                #
                for rt in last_real_tradings:
                    real_user = rt['ask_user_id']
                    if rt['ask_user_id'] == 10090:
                        real_user = rt['bid_user_id']

                    amount = float(rt['price']) * float(rt['volume'])
                    total_amount += amount

                    if real_user in total_user_amount:
                        total_user_amount[real_user] += amount
                    else:
                        total_user_amount[real_user] = amount

                    #
                    this_run_total_trades[code] = total_amount
                    big_trades[code] = total_user_amount

        if len(this_run_total_trades) > 0:
            # report ding
            # content = '以下币种产生用户交易：\n'
            # for key in this_run_total_trades:
            #     baseCurrency = 'USDT'
            #     if key[-3:] == 'btc':
            #         baseCurrency = 'BTC'
            #     elif key[-3:] == 'eth':
            #         baseCurrency = 'ETH'
            #
            #     content += '%s = %s %s \n' %(key, this_run_total_trades[key], baseCurrency)
            #
            # Ding.report(content)

            # report big
            for k1 in big_trades:
                baseCurrency = 'USDT'
                big_max = 1000

                if k1[-3:] == 'btc':
                    baseCurrency = 'BTC'
                    big_max = 0.1

                elif k1[-3:] == 'eth':
                    baseCurrency = 'ETH'
                    big_max = 4

                for k2 in big_trades[k1]:
                    amount = float(big_trades[k1][k2])
                    amount = round(amount, 4)
                    if amount > big_max:
                        content = '大额交易：'
                        content += '[user = %s]， [coin = %s]， [amount = %s %s]' %(k2, k1, amount, baseCurrency)
                        #print(content)
                        Ding.report_atAll(content)

        lastcTime = time.time()

        print('runing, nowTime = %s' %(datetime.datetime.now()))
        waitTime = 3600
        time.sleep(waitTime)