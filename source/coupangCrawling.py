from itertools import product
import requests
from bs4 import BeautifulSoup as bs
import re
import time
import pandas as pd
from xmlrpc.client import DateTime
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table
from sqlalchemy.exc import IntegrityError
import warnings
from datetime import datetime

import daedukmuchim
#db부분

df_location = daedukmuchim.read_location_csv()
dict_location = daedukmuchim.to_dict(df_location)

def get_engine():
    engine = create_engine(engineUrl,convert_unicode=True)
    return engine

def init_db():
    Base.metadata.create_all(engine)

def insertDB(date,title,price,weight,kind,site,location):
    try:
        insert_table.execute(
                            date = DateTime(date),
                            title= str(title),
                            price= int(price),
                            weight = str(weight),
                            kind = str(kind),
                            site = str(site),
                            location = str(location)
                            )
        print('데이터베이스 삽입완료')
    except IntegrityError as e:
        pass


def coupang_products(keyword, pages):
    baseurl = 'https://www.coupang.com'
    headers = { 'Accept-Language' : 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
                'Accept-Encoding': 'gzip'
    }
    
    products_link = []
    for page in range(1, pages + 1):
        print("page=",page)
        url =f'https://www.coupang.com/np/search?q={keyword}&channel=user&sorter=scoreDesc&listSize=36&isPriceRange=false&rating=0&page={page}&rocketAll=false'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        products_lis = soup.find('ul', id='productList').find_all('li')
        for li in products_lis:
            site = "쿠팡"
            kind = location = ""
            location_list = []
            a_link = li.find('a', href=True)['href']
            prd_link = baseurl + a_link
            prd_name = li.find('div', class_='name').text
            price = ''
            a_li = 0
            result = prd_name.split(' ')
            for m in result:
                location = "NONE"
                location = daedukmuchim.location(m, df_location, dict_location)
                location_list.append(location)
            
            for place in location_list:

                if place in list(df_location['시도'].values):
                    location = place
                    break;

            for word in result:
                if 'KG' in word:
                    a_li = word.split("KG")[0]
                elif 'kg' in word:
                    a_li = word.split("kg")[0]
                elif 'g' in word:
                    a_li = word.split("g")[0]
                    

            # weight = a_li[0]
            weight = re.sub(r'[^0-9,.]','',str(a_li))
            weight = weight.split("~")[0]
                
            price = li.find('strong', class_='price-value').text
            
            date = datetime.now()
            date = date.strftime('%Y-%m-%d %H:%M:%S')
            
            apple_feature_arr = ["부사", "아오리", "홍로"]
            pork_feature_arr = ['구이', '보쌈', '냉장', '냉동']
            kimchi_feature_arr = ['포기', '배추', '실비', '깍두기', '열무', '총각', '갓']
            feature_dict = {'사과': apple_feature_arr, '삼겹살': pork_feature_arr, '김치': kimchi_feature_arr}
            # 부사홍로
            
            price = (re.sub(r'[^0-9,.]','',price))
            price = price.replace(",", "")

            kind = daedukmuchim.get_kind_feature(feature_dict[keyword], prd_name)
            # location = get_feature_location(city_arr, prd_name)
            products_info = {
                'date' : date,
                'name': prd_name,
                'price': price,
                'weight':weight,
                'kind': kind,
                'site' : site,
                'location' : location
            }
            products_link.append(products_info)
            try:
                price = (int)((int)(price)/(float)(weight))
                insertDB(date,prd_name,price,weight,kind,site,location)
            except:
                pass

    df = pd.DataFrame(products_link)
    
    df.to_csv('crawling.csv', index=False, encoding='utf-8-sig',mode = "a")

engineUrl = 'mysql+pymysql://root:root@localhost:3306/kurly?charset=utf8mb4'

get_engine()
engine = get_engine()
print(get_engine())

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
init_db()

#sqlalchemy insert init
conn = engine.connect()
metadata = MetaData(bind=engine)


table = Table('crawling', metadata, autoload=True)

insert_table=table.insert()

if __name__ == '__main__':
    query = input('검색어를 작성하세요')
    coupang_products(query, 1) 