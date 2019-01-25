"""
# -*- coding: utf-8 -*-
@author: robin.liu
@github: qqqlyx
"""


import threading
import logging
import datetime
import time
import sys
import subprocess
sys.path.append('D:\\Robin\\UniDAX_MM')
#sys.path.append('D:\\Github\\UniDAX_MM')
from Core import Tokens

param = sys.argv[1]
#param = 'ST2'


if param == 'ST1':
    # 第一种
    # 根据火币成交量比例自成交
    path = Tokens._path + '\\Core\\ST1_Core.py'
else:
    # 第二种
    # 自设定数据成交
    path = Tokens._path + '\\Core\\ST2_All.py'


class st_action():
    def __init__(self, cmd):
        self.cmd = cmd
        self.p = None
        self.begin_time = datetime.datetime.now()
        self.count = 0
        self.param = param

        # 运行
        self.run()

        try:
            while True:
                time.sleep(120)
                self.poll = self.p.poll()  # 判断程序进程是否存在，None：表示程序正在运行 其他值：表示程序已退出

                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                if self.poll is None:
                    print(now_time + "  Self-Trading %s : NORMAL" %(param))
                else:
                    print(now_time + "  Self-Trading : STOP,TRY RE-OPEN")
                    self.run()
        except Exception as e:
            print('---->except<st_action>', e)

    def run(self):
        print('start OK!')
        self.p = subprocess.Popen(['python', '%s' % self.cmd, '%s' % self.param],
                                  stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, shell=False)


app = st_action(path)
