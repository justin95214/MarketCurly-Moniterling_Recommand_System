from fake_useragent import UserAgent
import warnings
########################################

from daedukmuchim import search_setting
from DB import DB
from crawling import EmartCrawling

warnings.filterwarnings("ignore")

TABLE_NAME = 'emart'
ENGINE_URL = 'mysql+pymysql://awsusr:12345678@awskurly.caeqso43nbt7.ap-northeast-2.rds.amazonaws.com:3306/daduckDB?charset=utf8mb4'
#ENGINE_URL = 'mysql+pymysql://root:root@localhost:3306/kurly?charset=utf8mb4'

db = DB(TABLE_NAME, ENGINE_URL)
conn = db.get_conn()

conn.execute('SET NAMES utf8;')
conn.execute('SET CHARACTER SET utf8;')
conn.execute('SET character_set_connection=utf8;')

ua = UserAgent()
base_url = 'https://emart.ssg.com'
header = {
    # 'referer': 'https://www.ssg.com/search.ssg?target=all&query=%EB%B3%B5%EC%88%AD%EC%95%84&src_area=late',
    'referer': 'https://emart.ssg.com/search.ssg?target=all&query=%EC%82%AC%EA%B3%BC',
    # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'user-agent': ua.random,
    # 'authority': 'api.mediacategory.com',
    'authority': 'simg.ssgcdn.com',
    # 'authority': 'tk.mediacategory.com',
}

emartCrawling = EmartCrawling(TABLE_NAME, base_url, header)

keyword = ''
total_page = 0

keyword, total_page = search_setting()
emartCrawling.crawling(db, keyword, total_page)
