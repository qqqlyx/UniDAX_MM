'''
UniDAX OpenAPI
'''
import hashlib
import requests
import datetime
import urllib3
import json


# 正式账户的api信息
# APIKEY = 'c59256c6ae13e3d45b4c9386111a6ee4'
# SECRET = '09bb015463410a1844066df46a223db3'
# unidax_url = "https://api.unidax.com/exchange-open-api"


# test
# APIKEY = '180706c4c319c665fdf05d35c9ec5950'
# SECRET = '6f106b0a2f3f01de5beb049dfb4e07e2'
# unidax_url = "https://testwww.unidax.com/exchange-open-api"

# # test 机器人
# APIKEY = '8595327a8947cf06492285588d761e01'
# SECRET = 'b2a9019765c0a64cc54214581c7366cd'
# unidax_url = "https://testwww.unidax.com/exchange-open-api"

# 机器人
APIKEY = '8595327a8947cf06492285588d761e01'
SECRET = 'b2a9019765c0a64cc54214581c7366cd'
unidax_url = "https://api.unidax.com/exchange-open-api"


# 计算md5加密
def getMD5(tem):
    return hashlib.new('md5', tem.encode("utf8")).hexdigest()


# 请求数据
def getUrlContent(tem):
    requests.packages.urllib3.disable_warnings()
    url = unidax_url + tem
    # url = 'www.unidax.com/exchange-open-api/open/api/create_order' + tem
    r = requests.get(url,  verify=False)
    return r.json()


# # post数据
# def postUrlContent(tem):
#     url = "http://api.unidax.com/exchange-open-api" + tem
#     requests.post(url=url,headers={'Content-Type': 'application/x-www-form-urlencoded'})
#     #requests.post(url=url, data={'key1': 'value1', 'key2': 'value2'},headers={'Content-Type': 'application/x-www-form-urlencoded'})

# 获取当前时间戳
def getTime():
    #n_t = datetime.datetime.now().strftime('%H%M%S%f')  # 这种方法在0:00-9:59会报错，似乎是因为开头不能为0
    n_t = '100000000000'  # 时间戳没有用，所以随便找一个代替
    return n_t


'''
行情api
'''


# 获取当前行情
def get_ticker(symbol):
    url = '/open/api/get_ticker?'
    url += 'symbol=' + symbol
    return getUrlContent(url)


# 获取K线数据
# period 单位为分钟，比如1分钟则为1，一天则为1440
def get_records(symbol, period):
    url = '/open/api/get_records?'
    url += 'symbol=' + symbol
    url += '&period=' + period
    return getUrlContent(url)


# 获取行情成交记录
def get_trades(symbol):
    url = '/open/api/get_trades?'
    url += 'symbol=' + symbol
    return getUrlContent(url)


# 查询买卖盘深度
# type 深度类型，step0, step1, step2（合并深度0-2）；step0时，精度最高
def market_dept(symbol, type):
    url = '/open/api/market_dept?'
    url += 'symbol=' + symbol
    url += '&type=' + type
    return getUrlContent(url)


# 获取各个币对的最新成交价
def market():
    api_key = APIKEY
    secret = SECRET
    time = getTime()

    string = 'api_key' + api_key + 'time' + time
    sign = getMD5(string + secret)

    url = '/open/api/market?'
    url += 'api_key=' + api_key
    url += '&time=' + time
    url += '&sign=' + sign
    return getUrlContent(url)


# 查询系统支持的所有交易对及精度
def symbols():
    url = '/open/api/common/symbols?'
    return getUrlContent(url)


'''
交易API
'''

# 获取当前委托
'''
INIT(0,"初始订单，未成交未进入盘口"), 
NEW_(1,"新订单，未成交进入盘口"), 
FILLED(2," 完 全 成 交 "), 
PART_FILLED(3," 部 分 成 交 "), 
CANCELED(4," 已 撤 单 "), 
PENDING_CANCEL(5," 待 撤 单 "), 
EXPIRED(6,"异常订单"); 
'''


def new_order(symbol, pageSize='10000', page='1'):
    url = '/open/api/new_order?'
    api_key = APIKEY
    secret = SECRET
    time = getTime()

    dic = {'api_key': api_key, 'time': time, 'symbol': symbol, 'pageSize': pageSize, 'page': page}
    sort = sorted(dic.items(), key=lambda item: item[0])
    string = ''
    for tem in sort:
        string += tem[0] + tem[1]
        url += tem[0] + '=' + tem[1] + '&'

    sign = getMD5(string + secret)
    url += 'sign=' + sign
    return getUrlContent(url)


# 创建订单
# fee_is_user_exchange_coin,0，当交易所有平台币时，此参数表示是否使用用平台币支付手续费，0否，1是
# side = BUY、SELL
def create_order(symbol, side, price, volume, type='1', fee_is_user_exchange_coin='0'):
    url = unidax_url + '/open/api/create_order'
    # url = 'https://api.unidax.com/exchange-open-api/open/api/create_order'
    # url = 'https://testwww.unidax.com/exchange-open-api/open/api/create_order'

    api_key = APIKEY
    secret = SECRET
    time = getTime()
    price = str(price)
    volume = str(volume)

    dic = {'symbol': symbol, 'side': side, 'price': price, 'volume': volume, 'type': type,
           'fee_is_user_exchange_coin': fee_is_user_exchange_coin, 'api_key': api_key, 'time': time}
    sort = sorted(dic.items(), key=lambda item: item[0])
    string = ''
    for tem in sort:
        string += tem[0] + tem[1]

    sign = getMD5(string + secret)
    dic['sign'] = sign

    headers = {
        "Accept": "application/json",
        'Content-Type': 'application/x-www-form-urlencoded'}

    urllib3.disable_warnings()
    r = requests.post(url=url, data=dic, headers=headers, verify=False)
    return r.text


# 撤单
def cancel_order(symbol, order_id):
    url = unidax_url + '/open/api/cancel_order'
    # url = 'https://api.unidax.com/exchange-open-api/open/api/cancel_order'

    api_key = APIKEY
    secret = SECRET
    time = getTime()
    symbol = str(symbol)
    order_id = str(order_id)

    dic = {'symbol': symbol, 'order_id': order_id, 'api_key': api_key, 'time': time}
    sort = sorted(dic.items(), key=lambda item: item[0])
    string = ''
    for tem in sort:
        string += tem[0] + tem[1]

    sign = getMD5(string + secret)
    dic['sign'] = sign

    headers = {
        "Accept": "application/json",
        'Content-Type': 'application/x-www-form-urlencoded'}

    urllib3.disable_warnings()
    r = requests.post(url=url, data=dic, headers=headers, verify=False)
    return r.text


# 资产余额
def account():
    api_key = APIKEY
    secret = SECRET
    time = getTime()

    string = 'api_key' + api_key + 'time' + time
    sign = getMD5(string + secret)

    url = '/open/api/user/account?'
    url += 'api_key=' + api_key
    url += '&time=' + time
    url += '&sign=' + sign
    return getUrlContent(url)


# 获取全部成交记录
def all_trade(symbol, pageSize='10000', page='1'):
    url = '/open/api/all_trade?'

    api_key = APIKEY
    secret = SECRET
    time = getTime()

    dic = {'api_key': api_key, 'time': time, 'symbol': symbol, 'pageSize': pageSize, 'page': page}
    sort = sorted(dic.items(), key=lambda item: item[0])
    string = ''
    for tem in sort:
        string += tem[0] + tem[1]
        url += tem[0] + '=' + tem[1] + '&'

    sign = getMD5(string + secret)
    url += 'sign=' + sign
    return getUrlContent(url)

