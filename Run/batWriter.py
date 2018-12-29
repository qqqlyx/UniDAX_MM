from Core import Tokens

stock_list = ['ethusdt', 'btcusdt', 'ltcusdt', 'etcusdt', 'ethbtc', 'ltcbtc',
              'zrxusdt','omgusdt','mcoeth','manaeth','sntusdt',
              'wtceth','gntusdt','cmtusdt','aeeth']


for code in stock_list:
    path = 'MM\\run_' + code + '.bat'
    f = open(path, 'w')

    f.write('python D:\\Robin\\UniDAX_MM\\Monitor\\MM_Monitor.py ' + code)
    f.write('\npause')
    f.close

for code in stock_list:
    path = Tokens._path + '\\Run\\ST\\run_ST_' + code + '.bat'
    f = open(path, 'w')

    path = 'Python ' + Tokens._path + '\\Monitor\\SelfTrading_Monitor.py '
    f.write(path + code)
    f.write('\npause')
    f.close
