
import threading
import logging
import datetime
import time
import sys
import subprocess
sys.path.append('D:\\Robin\\UniDAX_MM')
#sys.path.append('D:\\Github\\UniDAX_MM')
from Core import Tokens
path = Tokens._path + '\\RealTrading\\RT_Core.py'

class st_action():
    def __init__(self, cmd):
        self.cmd = cmd
        self.p = None
        self.begin_time = datetime.datetime.now()
        self.count = 0

        # 运行
        self.run()

        try:
            while True:
                time.sleep(1200)
                self.poll = self.p.poll()  # 判断程序进程是否存在，None：表示程序正在运行 其他值：表示程序已退出

                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                if self.poll is None:
                    print(now_time + "  RealTrading : NORMAL")
                else:
                    print(now_time + "  RealTrading : STOP,TRY RE-OPEN")
                    self.run()
        except Exception as e:
            print('---->except<st_action>', e)

    def run(self):
        print('start OK!')
        self.p = subprocess.Popen(['python', '%s' % self.cmd],
                                  stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, shell=False)


app = st_action(path)
