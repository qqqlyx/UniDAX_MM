stock_list = ['ethusdt', 'btcusdt', 'ltcusdt', 'etcusdt', 'ethbtc', 'ltcbtc',
              'yoousdt','zrxusdt','omgusdt','mcousdt','manausdt','sntusdt',
              'wtcusdt','gntusdt','repusdt','cmtusdt','aeusdt','elfusdt','pptusdt']


for code in stock_list:
    path = 'run_' + code + '.bat'
    f = open(path,'w')

    f.write('python D:\\Robin\\UniDAX_MM\\Monitor\\run_MM.py ' + code)
    f.write('\npause')
    f.close

