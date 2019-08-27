
import sys
sys.path.append('D:\\Robin\\UniDAX_MM')

import time
from Core import MM_Utils as utils
#code =sys.argv[1]
stock_list = ['infbtc']


while True:
    # 修正逻辑：先记录所有单号，接着进行报单，最后再撤上一批报单
    all_order = utils.mm_get_all_order(stock_list)
    # 获取火币深度行情
    _quota = utils.get_depth(stock_list)
    # 进行报单
    utils.mm_trading(_quota)
    # 最后再删上一次报单
    utils.mm_cancel_all(stock_list, all_order)

    # 等10秒后再重复
    time.sleep(10)
