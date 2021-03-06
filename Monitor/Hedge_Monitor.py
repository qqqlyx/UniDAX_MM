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

param = sys.argv[1]
if param == 'Hedge1':
    # 第一种
    # 根据资产对冲
    path = 'D:\\Robin\\UniDAX_MM\\Core\\Hedge1_Core.py'
else:
    # 第二种
    # 根据成交单对冲
    path = 'D:\\Robin\\UniDAX_MM\\Core\\Hedge2_Core.py'


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
                time.sleep(600)
                self.poll = self.p.poll()  # 判断程序进程是否存在，None：表示程序正在运行 其他值：表示程序已退出

                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                if self.poll is None:
                    print(now_time + "  Hedge : NORMAL")
                else:
                    print(now_time + "  Hedge : STOP,TRY RE-OPEN")
                    self.run()
        except Exception as e:
            print('---->except<st_action>', e)

    def run(self):
        print('start OK!')
        self.p = subprocess.Popen(['python', '%s' % self.cmd, '%s' % self.param],
                                  stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, shell=False)


app = st_action(path)
