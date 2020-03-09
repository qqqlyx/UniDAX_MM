
import sys
sys.path.append('D:\\Robin\\UniDAX_MM')

import time
from Core import MM_Utils as utils
code =sys.argv[1]
stock_list = [code]
# stock_list = ['infbtc']

last_id = []
# print('---0')
# begin
utils.cancelAll(stock_list)

while True:
    if code != 'ontusdt':
        # 修正逻辑：先记录所有单号，接着进行报单，最后再撤上一批报单
        # print('---1')
        _quota = utils.get_depth(stock_list)
        #
        # print('---2')
        od_id = utils.mm_trading(_quota)
        #
        #utils.self_trading()
        #
        for id in last_id:
            utils.mm_cancel(stock_list[0], id)
        #
        last_id = od_id

        # 等10秒后再重复
        time.sleep(60)
    else:
        print(1)
        _quota = utils.get_depth(stock_list)
        #
        # print('---2')
        od_id = utils.mm_trading(_quota)
        # 等10秒后再重复
        time.sleep(60)