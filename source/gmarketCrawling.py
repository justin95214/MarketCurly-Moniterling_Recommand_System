import sys

from datetime import datetime
from xmlrpc.client import DateTime
import requests
import json
import pandas as pd
import re
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table
import warnings


import re
import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table
import warnings
import time
import re

from daedukmuchim import search_setting
import daedukmuchim as dm
from DB import DB

TABLE_NAME = 'gmarket'
ENGINE_URL = 'mysql+pymysql://root:qwer1234@localhost:3306/kurly?charset=utf8mb4'
# engineUrl = 'mysql+pymysql://root:root@localhost:3306/kurly?charset=utf8mb4'

db = DB(TABLE_NAME, ENGINE_URL)
conn = db.get_conn()

conn.execute('SET NAMES utf8;')
conn.execute('SET CHARACTER SET utf8;')
conn.execute('SET character_set_connection=utf8;')

df = pd.DataFrame(columns=['date', 'title', 'price',
                  'weight', 'kind', 'site', 'location'])


keyword = ''
total_page = 0
keyword, total_page = search_setting()

url = "http://browse.gmarket.co.kr/search?keyword="+keyword

# 중복 체크를 위한 변수
previousItemList = []
result = []

k = 0

df_location = dm.read_location_csv()
dict_location = dm.to_dict(df_location)

while k < 4:
    k += 1
    time.sleep(10)
    ua = UserAgent()

    print(f'### {TABLE_NAME} page : {k}')

    custom_header = {
        'referer': 'http://www.gmarket.co.kr/',
        # 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'user-agent': ua.random,
        'authority': 'stags.bluekai.com'
    }

    custom_header.update({'user-agent': ua.random})

    page_url = "&k=32&p="+str(k)
    page_url = url + page_url
    res = requests.get(page_url, headers=custom_header)
    print(res.status_code)
    if res.status_code == 401:
        break

    if res.status_code == 200:

        html = bs(res.text, 'lxml')
        # print(html)
        cont = html.find('div', {'class': 'section__content-body-container'})
        cont0 = cont.find('div', {'class': 'section__inner-content-body'})
        cont1 = cont0.findAll('div', {'class': 'section__module-wrap'})
        for i in cont1:

            # print("=========================================")
            # print(i)

            item0 = i.findAll('div', {
                              'class': 'box__component box__component-itemcard box__component-itemcard--general'})
            # print(item0)
            for item in item0:
                # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                # print(item)
                # item1 = item0.find('div', {'class':'box__information-major'})
                item1 = item.find('div', {'class': 'box__item-container'})

                item2 = item1.find('div', {'class': 'box__information'})
                item3 = item2.find('div', {'class': 'box__information-major'})

                item_tmp_name = item3.find('div', {'class': 'box__item-title'})
                item_name = item_tmp_name.find(
                    'span', {'class': 'text__item'}).text

                item_tmp_price = item3.find(
                    'div', {'class': 'box__item-price'})
                item_price = item_tmp_price.find(
                    'strong', {'class': 'text text__value'}).text

                weight = 'None'
                candid_name = list(item_name.split(" "))
                # print(candid_name)

                loc = "None"

                apple_feature_arr = ["부사", "아오리", "홍로"]
                pork_feature_arr = ['구이', '보쌈', '냉장', '냉동']
                kimchi_feature_arr = ['포기', '배추', '실비', '깍두기', '열무', '총각', '갓']
                feature_dict = {'사과': apple_feature_arr,
                                '삼겹살': pork_feature_arr, '김치': kimchi_feature_arr}

                kind = dm.get_kind_feature(
                    feature_dict[keyword], item_name)
                map_dict = {}
                location_list = []

                weight_root = ""
                for m in candid_name:
                    if 'kg' in m or 'KG' in m:
                        try:
                            weight = m.split("kg")[0]
                        except:
                            weight = m.split("KG")[0]
                        weight = re.sub(r'[^0-9,.,~]', '', weight)
                        weight_root = weight.split("~")[0] + 'kg'
                    # print(m)

                    loc = "None"

                    loc = dm.location(m, df_location, dict_location)
                    location_list.append(loc)

                for place in location_list:

                    if place in list(df_location['시도'].values):
                        loc = place
                        break

                item_price = item_price.replace(',', '')
                date = datetime.now()
                date = date.strftime('%Y-%m-%d %H:%M:%S')
                site = "Gmarket"
                db.insertDB(date, item_name, item_price,
                            weight, kind, site, loc)
                df.loc[item_name] = [date, item_name, item_price,
                                     weight, kind, site, loc]

df.to_csv(f'{TABLE_NAME}.csv', index=False, encoding='utf-8-sig', mode="w")
