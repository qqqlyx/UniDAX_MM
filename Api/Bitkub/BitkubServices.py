import requests

bitkub_url = 'https://api.bitkub.com'


def getTicker():
    tem = '/api/market/ticker'
    return getUrlContent(tem)


def getAsks(symbol):
    """"""
    tem = '/api/market/asks'
    tem += '?sym=%s&lmt=10' %(symbol)
    return getUrlContent(tem)


def getBids(symbol):
    """"""
    tem = '/api/market/bids'
    tem += '?sym=%s&lmt=10' %(symbol)
    return getUrlContent(tem)


def getTrades(symbol,lmt):
    """"""
    tem = '/api/market/trades'
    tem += '?sym=%s&lmt=%s' %(symbol,lmt)
    return getUrlContent(tem)


# 请求数据
def getUrlContent(tem):
    """"""
    requests.packages.urllib3.disable_warnings()
    url = bitkub_url + tem
    r = requests.get(url,  verify=False)
    return r.json()


#
def getINF2BTC():
    """"""
    q = getTicker()
    price_btc_thb = q['THB_BTC']['last']

    infasks = getAsks('THB_INF')['result']
    infbids = getBids('THB_INF')['result']

    asks = []
    bids = []

    for ask in infasks:
        p = float(ask[3])
        vol = float(ask[4])
        price = p / price_btc_thb
        asks.append([price, vol])

    for bid in infbids:
        p = float(bid[3])
        vol = float(bid[4])
        price = p / price_btc_thb
        bids.append([price, vol])

    result = {
        'tick': {
            'bids': bids,
            'asks': asks,
        }
    }

    return result
