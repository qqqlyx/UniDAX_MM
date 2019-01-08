# 输入：
# 1计划总成交量
# 2各币种成交量占比
# 3各币种盘口比例（火币）
# 4活跃成交时间（24小时制）

# 输出：
# 用于自成交的数据准备文档

import pandas as pd
from pprint import *
import datetime
import random
import math
import time
import shutil
import os
from Core import Tokens
#显示所有列
# pd.set_option('display.max_columns', None)
# #显示所有行
# pd.set_option('display.max_rows', None)
# #调整显示宽度
# pd.set_option('display.height',1000)
# pd.set_option('display.max_rows',500)
# pd.set_option('display.max_columns',500)
# pd.set_option('display.width',1000)

'''
设置参数
'''
p_trade_time = [25, 45] # 交易间隔范围


'''
读取参数文件,遍历对应文件夹
'''
# os.path.abspath(path)

readPath = 'D:\\GitHub\\UniDAX_MM\\ST_setting\\UniDAX_MarketMaker.xlsx'
#father_path = Tokens._path
#readPath = father_path + '\\ST_setting\\UniDAX_MarketMaker.xlsx'
datas = pd.read_excel(readPath)

# 日期
nextDAY = datetime.datetime.now()# + datetime.timedelta(days=1)
#print(datas)

# 读取成交金额
_totalTradeAmount_min = float(datas.iloc[0][1]) * 10000  # 目标总成交金额范围下限 (万元usdt)
_totalTradeAmount_max = float(datas.iloc[0][2]) * 10000  # 上限 (万元usdt)

# 读取活跃交易时间
_activeTime = []
for i in range(1, 4):
    bt = datas.iloc[i][1]
    et = datas.iloc[i][2]
    r = float(datas.iloc[i][3])
    if bt == bt and et == et and r == r:  # 如果值是NaN，则bt!=bt
        _activeTime.append([bt, et, r])

# 读取币种和比例
_coinTradeRatio = {}  # 各币种成交金额比例，字典
row_count = datas.shape[0]
for i in range(row_count):
    item = str(datas.iloc[i][0])
    if '*' in item:
        coin = item.replace('*','')
        value = datas.iloc[i][1]
        _coinTradeRatio[coin] = value


'''
计算“小时”资金分配方案
'''

# 一个随机函数，给定均值eg、数量n，生成长度为n的list，各个数量为均值附近的随机，但保证生成的list总和=eg*n
def _get_randomList(eg, n):
    result = []
    half = int(n / 2)
    for i in range(half):
        ra = random.uniform(0.8, 1)
        ra2 = 2 - ra
        result.append(ra * eg)
        result.append(ra2 * eg)
    if len(result) < n:
        result.append(eg)

    random.shuffle(result) # 顺序打乱
    return result

_amountTable = pd.DataFrame(columns=list(_coinTradeRatio.keys()))

# 先计算总成交金额
r = random.uniform(0.2, 0.8)
spread = _totalTradeAmount_max - _totalTradeAmount_min
spread = r * spread
_totalTradeAmount = _totalTradeAmount_min + spread

# 分配各币种比例
_amountTable.loc['Ratio'] = list(_coinTradeRatio.values())

# 分配各币种成交金额
_amountTable.loc['Amount'] = _amountTable.loc['Ratio'] * _totalTradeAmount

# 分配各时间成交金额比例
_timeTable = pd.DataFrame(columns=list(_coinTradeRatio.keys()))
for i in range(24):
    s = str(nextDAY.year) + '-'+ str(nextDAY.month) + '-' + str(nextDAY.day)
    s += ' ' + str(i) + ':00:00'
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(s, "%Y-%m-%d %H:%M:%S"))
    _timeTable.loc[t] = None

rR = 1.0

for temp in _activeTime:  # 先分别计算活跃时间比例
    rR -= temp[2]
    count = temp[1].hour - temp[0].hour
    eR = temp[2] / count # 计算出均值和n，下面_get_randomlist函数帮助生成随机数列

    for y in range(_timeTable.shape[1]):
        rList = _get_randomList(eR, count) # 进行随机

        for x in range(temp[0].hour, temp[1].hour):
            _timeTable.iloc[x,y] = rList.pop(0) * _amountTable.iloc[1,y] # 此处使用pop，删除指定位置元素、并返回值


# 再计算普通时间比例
rC = (_timeTable.iloc[:,0] != _timeTable.iloc[:,0]).astype(int).sum() # 好好使用
eR = rR / rC
for y in range(_timeTable.shape[1]):
    rList = _get_randomList(eR, rC)  # 进行随机

    for x in range(_timeTable.shape[0]):
        if _timeTable.iloc[x,y] != _timeTable.iloc[x,y]:
            _timeTable.iloc[x,y] = rList.pop(0) * _amountTable.iloc[1,y]

#print(_timeTable)

'''
计算各币种详细成交方案
'''

# 用来拆分一小时时间, 返回时间拆分和数量拆分
def _randomSplitHour():
    # 记录list
    result = [] #时间拆分
    total = 0
    while True:
        # 随机每次交易时间
        r = random.randint(p_trade_time[0], p_trade_time[1])
        total += r

        if total <= 3600:
            result.append(r)
        else: # 超出1小时后，准备退出
            return result

# 根据拆分的时间，随机具体拆分金额
def _getSpliAmount(amount, splitHour):
    count = len(splitHour)
    tL = []
    sum = 0
    for i in range(count):
        r = random.uniform(0,1)
        tL.append(r)
        sum += r
    for i in range(count):
        tL[i] = round(tL[i]/sum * amount,4)
    return tL


_tradingPlan = {} # 字典，记录各币种的DataFrame
for x in range(_timeTable.shape[1]):
    coin = _timeTable.columns.values.tolist()[x]
    temp = pd.DataFrame(columns=[coin])

    #
    timelist = []
    amountlist = []

    for y in range(24):
        hour_amount = _timeTable.iloc[y,x] # 每小时总成交金额

        # 拆分每小时成交
        split_Time = _randomSplitHour()

        # 成分各成交金额
        split_Amount = _getSpliAmount(hour_amount,split_Time)

        # 赋值到新的table
        rn = _timeTable.index.values.tolist()[y]
        run_Time = datetime.datetime.strptime(rn, "%Y-%m-%d %H:%M:%S")
        for i in range(len(split_Time)):
            delta = datetime.timedelta(seconds=split_Time[i])
            run_Time += delta
            timelist.append(run_Time)
            amountlist.append(split_Amount[i])

    temp = pd.DataFrame()
    temp['Time'] = timelist
    temp['Amount'] = amountlist
    _tradingPlan[coin] = temp



# for key in _tradingPlan:
#     csv_writePath = writePath + '\\' + key + '.csv'
#     _tradingPlan[key].to_csv(csv_writePath)
#     continue


# 重新处理成1个文件
_total_tradingPlan = pd.DataFrame()
for key in _tradingPlan:
    temp = pd.DataFrame()
    #temp['Time'] = _tradingPlan[key].iloc[:, 0]
    temp['Time'] = _tradingPlan[key].loc[:,'Time']
    temp['Amount'] = _tradingPlan[key].loc[:, 'Amount']
    temp['Code'] = key
    _total_tradingPlan = pd.concat([_total_tradingPlan, temp], axis=0)
    continue

# 写入文件
writePath = 'D:\\GitHub\\UniDAX_MM\\ST_setting\\' + str(nextDAY.year) + str(nextDAY.month) + str(nextDAY.day)
if os.path.exists(writePath):
    shutil.rmtree(writePath)
    #time.sleep(3)
os.makedirs(writePath)

_total_tradingPlan = _total_tradingPlan.sort_values(by='Time')
csv_writePath = writePath + '\\all.csv'
_total_tradingPlan.to_csv(csv_writePath)




