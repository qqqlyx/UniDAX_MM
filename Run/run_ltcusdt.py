"""
# -*- coding: utf-8 -*-
@author: robin.liu
@github: qqqlyx
"""

from MM import MM_Utils as mma
import threading
import logging
import datetime
import time
import sys
import subprocess

# 参与报价币种
code = 'ltcusdt'
path = 'D:\\GitHub\\UniDAX_MM\\MM\\MM_Core.py'


class mm_action():
    def __init__(self, code, cmd):
        self.code = code
        self.cmd = cmd
        self.p = None
        self.begin_time = datetime.datetime.now()
        self.count = 0

        # 运行
        self.run()

        try:
            while True:
                time.sleep(5)
                self.poll = self.p.poll() #判断程序进程是否存在，None：表示程序正在运行 其他值：表示程序已退出
                if self.poll is None:
                    print(code + ": NORMAL")
                else:
                    print(code + ": STOP,TRY RE-OPEN")
                    self.run()
        except Exception as e:
            print('---->except<mm_action>', e)

    def run(self):
        print('start OK!')
        self.p = subprocess.Popen(['python', '%s' % self.cmd, '%s' % self.code],
                                  stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, shell=False)


app = mm_action(code, path)