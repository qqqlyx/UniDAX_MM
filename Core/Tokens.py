import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

# 文件地址
_path = 'D:\\Robin\\UniDAX_MM'
#_path = 'D:\\GitHub\\UniDAX_MM'



# UniDAX  TOKEN

#test 机器人
# UniDAX_APIKEY_TEST = '8595327a8947cf06492285588d761e01'
# UniDAX_SECRET_TEST = 'b2a9019765c0a64cc54214581c7366cd'
# UniDAX_unidax_url_TEST = "https://testwww.unidax.com/exchange-open-api"

# 正式-机器人
UniDAX_APIKEY = '8595327a8947cf06492285588d761e01'
UniDAX_SECRET = 'b2a9019765c0a64cc54214581c7366cd'
UniDAX_unidax_url = "https://api.unidax.com/exchange-open-api"








# HuoBi  TOKEN
Huobi_ACCESS_KEY = 'b2488e5b-949435a5-ace24a32-10db8'
Huobi_SECRET_KEY = '17591fde-cad95e9d-6f253767-477e8'