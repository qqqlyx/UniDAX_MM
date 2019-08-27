
import sys
sys.path.append('D:\\Robin\\UniDAX_MM')

import time
from Core import MM_Utils as utils
stock_list = ['btcusdt']

last_id = []

# begin
#utils.cancelAll(stock_list)

while True:
    # 修正逻辑：先记录所有单号，接着进行报单，最后再撤上一批报单
    _quota = utils.get_depth(stock_list)
    #
    od_id = utils.mm_trading(_quota)
    #
    for id in last_id:
        utils.mm_cancel(stock_list[0], id)
    #
    last_id = od_id

    # 等10秒后再重复
    time.sleep(10)
