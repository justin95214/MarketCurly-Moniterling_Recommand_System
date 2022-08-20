from datetime import datetime
from turtle import window_height
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

import daedukmuchim

df_location = daedukmuchim.read_location_csv()
dict_location = daedukmuchim.to_dict(df_location)
# Request에서 사용될 header 생성
headers = {
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

warnings.filterwarnings("ignore")

## 함수 부분 ##
#####################################################################################################################

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

def removeEmoji(text):
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)
        
def isRepeat(previousItemList, itemList) :
    
    #같은 값을 응답받으면 True 리턴
    if previousItemList['shoppingResult']['products'][0]['productName'] == itemList['shoppingResult']['products'][0]['productName']:
        print('같아서 끝-----')
        return True
    #아니면 False 리턴
    return False   

def printData(itemList) :
    # 추출하려는 값의 key를 입력
    
    for i in itemList['shoppingResult']['products']:
        title = removeEmoji(i['productName'])
        price = i['price']
        weight = cValue = kind = wordsW = location = ''
        location_list = []
        date = datetime.now()
        date = date.strftime('%Y-%m-%d %H:%M:%S')
        site = "Naver"
        cValue = i['characterValue']
        cValueSplit = cValue.split('|')

        apple_feature_arr = ["부사", "아오리", "홍로"]
        pork_feature_arr = ['구이', '보쌈', '냉장', '냉동']
        kimchi_feature_arr = ['포기', '배추', '실비', '깍두기', '열무', '총각', '갓']
        feature_dict = {'사과': apple_feature_arr, '삼겹살': pork_feature_arr, '김치': kimchi_feature_arr}
        # 부사홍로

        kind = daedukmuchim.get_kind_feature(feature_dict[query], cValue)
        
        for words in cValueSplit:
            if "kg" in words or "KG" in words:
                wordsW = words
                if "," in words:
                    wordsW = words.split(',')[0]        
                weight = wordsW

        titleSplit = title.split(' ')

        for m in titleSplit:
            location = "NONE"
            location = daedukmuchim.location(m, df_location, dict_location)
            location_list.append(location)

        for place in location_list:

            if place in list(df_location['시도'].values):
                location = place
                break;

        if weight == '':
            for words in titleSplit:
                if "kg" in words or "KG" in words:
                    weight = words
                    if "," in words:
                        wordsW = words.split(',')[0]
                        weight = wordsW
        weight = weight.split('kg')[0]
        
        if "~" in weight:
            weight = weight.split('~')[0]
        weight = re.sub(r'[^0-9,.]','',weight)
        
        if kind == '':
            kind = daedukmuchim.get_kind_feature(feature_dict[query], title)
            
        # print(f'## {title}\n{kind}')
        try:
            mallInfo = i['mallInfoCache']['onmktRegisterNo']
        except:
            mallInfo = ''
        
        insertDB(date,title,price,weight,kind,site,location)
        df.loc[title] = [date,title,price,weight,kind,site,location]
        
    return df

def makeRequestAndGetResponse(number,query) :
    pageingIndex = number

    params = (
        ('sort', 'rel'),
        ('pagingIndex', pageingIndex),
        ('pagingSize', '20'),
        ('viewType', 'list'),
        ('productSet', 'total'),
        ('deliveryFee', ''),
        ('comNm',''),
        ('characterValue',''),
        ('deliveryTypeValue', ''),
        ('frm', 'NVSHATC'),
        ('query', query),
        ('origQuery', query),
        ('iq', ''),
        ('eq', ''),
        ('xq', ''),
        ('crurl','')
    )

    
    response = requests.get('https://search.shopping.naver.com/api/search/all', headers=headers, params=params)
    return response

## 로직부분 ##
#####################################################################################################################

engineUrl = 'mysql+pymysql://root:root@localhost/naver_db?charset=utf8mb4'
get_engine()
engine = get_engine()

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
init_db()
#sqlalchemy insert init
conn = engine.connect()
metadata = MetaData(bind=engine)


table = Table('naver', metadata, autoload=True)
insert_table=table.insert()

conn.execute('SET NAMES utf8;')
conn.execute('SET CHARACTER SET utf8;')
conn.execute('SET character_set_connection=utf8;')



df = pd.DataFrame(columns=['date','title','price','weight','kind','site','location'])

# 중복 체크를 위한 변수
previousItemList = []
query = 0
query = input('검색어를 작성하세요')
number = 1
while number < 20 :
    print('page ', number)

    # 네이버를 향한 Request 생성 and 네이버로부터 response 받기
    response = makeRequestAndGetResponse(number,query)

    # json을 리스트로 받기
    itemList = json.loads(response.text)

    # 첫번째 호출에는 list가 비교가 안되니 continue를 한다.
    if number == 1 :
        number = number + 1
        previousItemList = itemList
        printData(itemList)
        continue

# 반복 응답 Check Method
# 응답이 같은 값으로 반복되었는지 확인하는 메서드를 실행한다. True일 경우 중복이라서 break
    if isRepeat(previousItemList, itemList) :
        break

    previousItemList = itemList

    printData(itemList)
    number = number + 1

df.to_csv("naver.csv",encoding="utf-8-sig",mode = "w")
