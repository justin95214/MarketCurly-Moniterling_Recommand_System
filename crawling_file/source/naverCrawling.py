import warnings

########################################

from daedukmuchim import search_setting
from crawling import NaverCrawling
from DB import DB

warnings.filterwarnings("ignore")

TABLE_NAME = 'naver'
ENGINE_URL = 'mysql+pymysql://awsusr:12345678@awskurly.caeqso43nbt7.ap-northeast-2.rds.amazonaws.com:3306/daduckDB?charset=utf8mb4'
# engineUrl = 'mysql+pymysql://root:root@localhost:3306/kurly?charset=utf8mb4'

db = DB(TABLE_NAME, ENGINE_URL)
conn = db.get_conn()

conn.execute('SET NAMES utf8;')
conn.execute('SET CHARACTER SET utf8;')
conn.execute('SET character_set_connection=utf8;')

base_url = 'https://www.naver.com'
header = {
    'authority': 'search.shopping.naver.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'NNB=P2OJ4TKGTXDGE; autocomplete=use; AD_SHP_BID=25; ASID=d3d1e8c100000181de00a6c80000005f; _ga_YTT2922408=GS1.1.1657891947.1.1.1657892026.0; _gcl_au=1.1.601090528.1659459312; _fbp=fb.1.1659459312548.2084023565; nx_ssl=2; _ga_4BKHBFKFK0=GS1.1.1659889803.1.1.1659889846.17; _ga=GA1.2.227194149.1657273330; _gid=GA1.2.927446653.1660726025; _ga_7VKFYR6RV1=GS1.1.1660726025.24.0.1660726027.58.0.0; spage_uid=; sus_val=CMgcskyYXOS33Ct+uIlH2R+X',
    'referer': 'https://search.shopping.naver.com/search/all?query=%EC%82%AC%EA%B3%BC&frm=NVSHATC&prevQuery=%EC%82%AC%EA%B3%BC',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
}

naverCrawl = NaverCrawling(TABLE_NAME, base_url, header)

keyword = ''
total_page = 0

keyword, total_page = search_setting()
naverCrawl.crawling(db=db, keyword=keyword, total_page=total_page)

# iqr = 0
# q3 = df['price'].quantile(0.75)
# q1 = df.quantile(0.25)

# iqr = q3 - q1

# def is_kor_outlier(df):
#     score = df['price']
#     if score > q3['price'] + 1.5 * iqr['price'] or score < q1['price'] - 1.5 * iqr['price']:
#         return True
#     else:
#         return False

# # apply 함수를 통하여 각 값의 이상치 여부를 찾고 새로운 열에 결과 저장
# df['price_이상치여부'] = df.apply(is_kor_outlier, axis = 1) # axis = 1 지정 필수
# df_trim = df.loc[df['price_이상치여부'] == False]

# # 이상치여부를 나타내는 열 제거
# del df_trim['price_이상치여부']

# df_trim
