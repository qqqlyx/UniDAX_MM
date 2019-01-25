'''
向钉钉群推送消息
'''
import requests
import json
import urllib.parse
import time
import datetime
from pprint import *
from Core import MM_Utils as utils
from Api.UniDax import Constant as cons
from Api.UniDax import UniDaxServices as uds
from Core import Tokens


'''
参数
'''
dingUrl_MM = 'https://oapi.dingtalk.com/robot/send?access_token=bc99ebaf7ff8f934897108983043402207e900927694e56a90def069673f572b'
dingUrl_ST = 'https://oapi.dingtalk.com/robot/send?access_token=1c833baa46c9ed28146f2a9111063b458d13eb4f30dcf4ca49b3a8ce7a3f552d'
AllCoins = cons.stock_list

'''
全局变量
'''
DayNotify = ''  # 每日系统通知


#
def dingReport(dingUrl, content, atMobiles = '', atAll=False):
    headers = {
        "Accept": "application/json",
        'Content-Type': "application/json ;charset=utf-8"}

    dingData = {}
    dingData['msgtype'] = 'text'
    dingData['text'] = {'content': content}
    dingData['at'] = {"atMobiles": [atMobiles], "isAtAll": atAll}

    String_textMsg = json.dumps(dingData)
    r = requests.post(url=dingUrl, data=String_textMsg, headers=headers)
    return r.text

while(True):
    #
    # 系统每日0点通知
    #
    today = '%s-%s-%s' %(time.localtime().tm_year,time.localtime().tm_mon,time.localtime().tm_mday)
    if DayNotify != today:
        # 进行通知
        report = '(机器人测试) 自检运行正常。[挂单量 = 火币5%] [挂单深度 = 20]'
        dingReport(dingUrl_MM, report)
        DayNotify = today

        path = Tokens._path + '\\ST_setting' + '\\' + today + '\\' + 'Param.txt'
        f = open(path)
        line = f.readlines()
        total_amount = float(line[2].split('\n')[0].split('=')[1])
        total_amount = round(int(total_amount) / 10000, 2)
        
        report = '(机器人测试) 自检运行正常。[今日规划成交金额 = 固定值(%s万) + 火币 10%]' %(total_amount)

    time.sleep(1)
    # for coin in cons.stock_list:
    #     pprint(uds.market())
    #     time.sleep(10000)
