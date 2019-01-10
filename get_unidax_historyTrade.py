import datetime
from Api.UniDax import Constant as cons
from Api.UniDax import UniDaxServices as uds
from Api.Huobi import HuobiServices as hbs
from pprint import *
import threading
import time
import random
import pandas as pd

t = uds.all_trade('',pageSize='100',page=1)

pprint(t)
