from Core import Tokens

stock_list = ['ethusdt', 'btcusdt', 'ltcusdt', 'etcusdt', 'ethbtc', 'ltcbtc',
              'zrxusdt','omgusdt','mcoeth','manaeth','sntusdt',
              'wtceth','gntusdt','cmtusdt','aeeth']

#stock_list = ['zrxusdt','omgusdt','mcoeth','manaeth','sntusdt',
              #'wtceth','gntusdt','cmtusdt','aeeth']


for code in stock_list:
    path = Tokens._path + '\\Run\\MM\\run_' + code + '.bat'
    f = open(path, 'w')

    f.write('python ' + Tokens._path + '\\Monitor\\MM_Monitor.py ' + code)
    f.write('\npause')
    f.close

for code in stock_list:
    path = Tokens._path + '\\Run\\ST\\run_ST_' + code + '.bat'
    f = open(path, 'w')

    path = 'python ' + Tokens._path + '\\Monitor\\SelfTrading_Monitor.py '
    f.write(path + code)
    f.write('\npause')
    f.close

path = Tokens._path + '\\Run\\ST\\run_ST_all.bat'
f = open(path, 'w')
path = 'python ' + Tokens._path + '\\Monitor\\SelfTrading_Monitor.py '
f.write(path + 'all')
f.write('\npause')
f.close
