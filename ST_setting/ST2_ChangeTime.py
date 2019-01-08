import pandas as pd
import os, shutil
from pprint import *
import time
import datetime


readPath = 'D:\\GitHub\\UniDAX_MM\\ST_setting\\201914'
filenames = os.listdir(readPath)

p_t = '2019-01-04 13:20:00'

p_tradeTime=datetime.datetime.strptime(p_t, "%Y-%m-%d %H:%M:%S")

for file in filenames:
    filepath = readPath + '\\' + file
    datas = pd.read_csv(filepath)

    base_date = datetime.datetime.strptime(datas.iloc[0,1], "%Y-%m-%d %H:%M:%S")
    h = p_tradeTime.hour - base_date.hour
    m = p_tradeTime.minute - base_date.minute

    for i in range(len(datas.iloc[:,0])):
        date = datetime.datetime.strptime(datas.iloc[i,1], "%Y-%m-%d %H:%M:%S")

        if date < p_tradeTime:
            date += datetime.timedelta(hours=h, minutes=m)
            datas.iloc[i, 1] = date.strftime("%Y-%m-%d %H:%M:%S")
        # pprint(row)
        # time.sleep(10000)
    # pprint(datas)
    # time.sleep(10000)

    if os.path.exists(filepath):
        os.remove(filepath)
        # time.sleep(3)
    datas.to_csv(filepath, index=False)










