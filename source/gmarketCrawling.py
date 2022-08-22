import sys
from fake_useragent import UserAgent

import warnings
import time
import warnings
########################################

from daedukmuchim import search_setting
from crawling import GmarketCrawling
from DB import DB

warnings.filterwarnings("ignore")

TABLE_NAME = 'gmarket'
ENGINE_URL = 'mysql+pymysql://root:qwer1234@localhost:3306/kurly?charset=utf8mb4'
# engineUrl = 'mysql+pymysql://root:root@localhost:3306/kurly?charset=utf8mb4'

db = DB(TABLE_NAME, ENGINE_URL)
conn = db.get_conn()

conn.execute('SET NAMES utf8;')
conn.execute('SET CHARACTER SET utf8;')
conn.execute('SET character_set_connection=utf8;')

ua = UserAgent()

base_url = 'http://www.gmarket.co.kr/'
header = {
    'referer': 'http://www.gmarket.co.kr/',
    # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'user-agent': ua.random,
    'authority': 'stags.bluekai.com'
}

gmarketCrawling = GmarketCrawling(TABLE_NAME, base_url, header)

keyword = ''
total_page = 0

keyword, total_page = search_setting()
gmarketCrawling.crawling(db, keyword, total_page)
