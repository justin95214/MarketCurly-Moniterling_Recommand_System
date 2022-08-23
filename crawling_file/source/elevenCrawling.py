from itertools import product
from mmap import PAGESIZE
from time import sleep
from urllib import request
import requests
from bs4 import BeautifulSoup as bs
from sqlalchemy.exc import IntegrityError

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


keyword = input('입력하시오 : ')
#keyword = "사과"


def productName():
    key = '1336580cf485231ddf50920a29799360'
    
    product_list = []
    for pageNum in range(10):
        
        url = f'http://openapi.11st.co.kr/openapi/OpenApiService.tmall?key={key}&apiCode=ProductSearch&keyword={keyword}&option=Categories&pageNum={pageNum}&pageSize=200'
        
        req = requests.get(url)

        print(url)
        xmlRowdata = req.content.decode('cp949')
        soup = bs(xmlRowdata, 'html.parser')

        apple_feature_arr = ["부사", "아오리", "홍로"]
        pork_feature_arr = ['구이', '보쌈', '냉장', '냉동']
        kimchi_feature_arr = ['포기', '배추', '실비', '깍두기', '열무', '총각', '갓']
        feature_dict = {'사과': apple_feature_arr, '삼겹살': pork_feature_arr, '김치': kimchi_feature_arr}
        
        # item_name : 상품 이름(풀네임)
        
        
        for name, code in zip(soup.find_all("productname"), soup.find_all('productcode')):
            temp = name.text
            kind = daedukmuchim.get_kind_feature(feature_dict[keyword], temp)
            print(f'#### {kind}, {temp}')
            if 'kg' in temp:
                product_list.append(temp)
                print(f'# 이름 ^: {temp}, $ 가격 : {code.text}')
            #else:
                #print(f'# 이름  : {temp}, $ 가격 : {code.text}')
        

            

    print(len(product_list))

    
productName()