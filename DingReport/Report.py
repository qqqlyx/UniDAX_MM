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
import random


'''
参数
'''
dingUrl = 'https://oapi.dingtalk.com/robot/send?access_token=bc99ebaf7ff8f934897108983043402207e900927694e56a90def069673f572b'
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

    '''
    系统每日0点通知
    '''
    today = '%s-%s-%s' %(time.localtime().tm_year,time.localtime().tm_mon,time.localtime().tm_mday)
    if DayNotify != today:
        # 进行通知
        #report = '(深度系统) 自检运行正常。[挂单量 = 火币5%] [挂单深度 = 20]'
        #report = '(机器人测试) 自检运行正常。'
        #dingReport(dingUrl, report)

        r = random.uniform(0.95,1.05)
        r = round(4000 * r, 2)

        #report = '(刷单系统) 自检运行正常。[今日UniDAX规划成交金额 = %s万 USDT]' %(str(r))
        #report = '(机器人测试) 自检运行正常。%s' %(str(r))

        #dingReport(dingUrl, report)

        # report = 'Ding自动报警！ ->成交价偏离火币<- 深度系统开始自检。'
        # dingReport(dingUrl, report)
        # #time.sleep(2)
        # report = '自检通过，通知人工查验。'
        # dingReport(dingUrl, report, atMobiles='13640905689')
        report = '测试完成！'
        dingReport(dingUrl, report)


        DayNotify = today

    '''
    
    '''
    time.sleep(1)
    # for coin in cons.stock_list:
    #     pprint(uds.market())
    #     time.sleep(10000)
