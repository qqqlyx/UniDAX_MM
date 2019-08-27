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

dingUrl = 'https://oapi.dingtalk.com/robot/send?access_token=2a3d70415a15e42f83480e4854372cbb9168d6182f7291ecc4df192c34cf6f41'
# dingUrl_ST = 'https://oapi.dingtalk.com/robot/send?access_token=1c833baa46c9ed28146f2a9111063b458d13eb4f30dcf4ca49b3a8ce7a3f552d'
AllCoins = cons.stock_list

'''
全局变量
'''
DayNotify = ''  # 每日系统通知
lastID = {}

#
def report(content):
    headers = {
        "Accept": "application/json",
        'Content-Type': "application/json ;charset=utf-8"}

    dingData = {}
    dingData['msgtype'] = 'text'
    dingData['text'] = {'content': content}
    dingData['at'] = {"atMobiles": [''], "isAtAll": False}

    String_textMsg = json.dumps(dingData)
    r = requests.post(url=dingUrl, data=String_textMsg, headers=headers)
    return r.text


#
def report_atAll(content):
    headers = {
        "Accept": "application/json",
        'Content-Type': "application/json ;charset=utf-8"}

    dingData = {}
    dingData['msgtype'] = 'text'
    dingData['text'] = {'content': content}
    dingData['at'] = {"atMobiles": [''], "isAtAll": True}

    String_textMsg = json.dumps(dingData)
    r = requests.post(url=dingUrl, data=String_textMsg, headers=headers)
    return r.text
