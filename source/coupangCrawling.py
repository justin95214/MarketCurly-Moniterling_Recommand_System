import sys
from itertools import product
import warnings

from daedukmuchim import search_setting
from DB import DB
from crawling import CoupangCrawling
# db부분


TABLE_NAME = 'coupang'

ENGINE_URL = 'mysql+pymysql://root:qwer1234@localhost:3306/kurly?charset=utf8mb4'
# ENGINE_URL = 'mysql+pymysql://root:root@localhost:3306/kurly?charset=utf8mb4'
db = DB(TABLE_NAME, ENGINE_URL)
conn = db.get_conn()

conn.execute('SET NAMES utf8;')
conn.execute('SET CHARACTER SET utf8;')
conn.execute('SET character_set_connection=utf8;')

base_url = 'https://www.coupang.com'
header = {
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Accept-Encoding': 'gzip'
}

coupangCrawl = CoupangCrawling(TABLE_NAME, base_url, header)

keyword = ''
total_page = 0

keyword, total_page = search_setting()
coupangCrawl.crawling(db, keyword, total_page)
