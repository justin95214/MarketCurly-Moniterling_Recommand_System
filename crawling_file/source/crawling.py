import numpy as np
import pandas as pd
import requests
import json
import time
import re
from fake_useragent import UserAgent
from datetime import date, datetime
from bs4 import BeautifulSoup as bs
from bs4 import BeautifulSoup

import daedukmuchim as dm


class Crawling:
    def __init__(self, table_name, base_url, header) -> None:
        self.TABLE_NAME = table_name
        self.base_url = base_url
        self.header = header
        self.df_location = dm.read_location_csv()
        self.dict_location = dm.to_dict(self.df_location)

    def print_page_status(self, page_num):
        print(f'###\t{self.TABLE_NAME}\tpage', page_num)

    def crawling(self, db, keyword, total_page):
        print(f'###\t{self.TABLE_NAME}\tcrawling end')

    def get_outlier(self, df=None, column=None, weight=2.5):
        # target 값과 상관관계가 높은 열을 우선적으로 진행
        quantile_25 = df[column].quantile(0.25)
        quantile_75 = df[column].quantile(0.75)

        IQR = quantile_75 - quantile_25
        IQR_weight = IQR*weight

        lowest = quantile_25 - IQR_weight
        highest = quantile_75 + IQR_weight
        outlier_idx = df[column][(df[column] < lowest) |
                                 (df[column] > highest)].index

        return outlier_idx


class EmartCrawling(Crawling):
    def crawling(self, db, keyword, total_page):
        ua = UserAgent()
        url = "https://emart.ssg.com/search.ssg?target=all&query="+keyword
        df = pd.DataFrame(columns=['date', 'title', 'price',
                                   'weight', 'kind', 'site', 'location'])
        i = 0

        while i <= total_page:
            i += 1
            time.sleep(10)
            self.print_page_status(i)

            page_url = "&page="+str(i)
            self.header.update({'user-agent': ua.random})

            res = requests.get(url+page_url, headers=self.header)
            if res.status_code == 401:
                break

            if res.status_code == 200:
                html = bs(res.text, 'lxml')
                # print(html)
                cont0 = html.find('div', {'class': 'tmpl_itemlist'})
                
                # print(cont)
                try:
                    cont1 = cont0.find(
                    'ul', {'class': 'cunit_thmb_lst cunit_thmb_lst4 cunit_thmb_w1000'})
                    items = cont1.findAll('li', {'class': 'cunit_t232'})
                    for item0 in items:
                        item1 = item0.find('div', {'class': 'cunit_info'})
                        unit_price = None

                        name = item1.find('em', {'class': 'tx_ko'}).text
                        price = item1.find('em', {'class': 'ssg_price'}).text
                        unit_tx = item1.find('span', {'class': 'ssg_tx'}).text
                        try:
                            unit_price = item1.find(
                                'div', {'class': 'unit'}).text[1:-1]
                        except:
                            pass

                        # insertDB(name, price, unit_tx, unit_price)

                        weight_root = ""

                        loc = "None"
                        map_dict = {}
                        location_list = []
                        candid_name = list(name.split(" "))

                        weight = ''
                        for m in candid_name:
                            if 'kg' in m or 'KG' in m:
                                try:
                                    weight = m.split("kg")[0]
                                except:
                                    weight = m.split("KG")[0]
                                weight = re.sub(r'[^0-9,.]', '', weight)
                            # print(m)

                            loc = "None"

                            loc = dm.location(
                                m, self.df_location, self.dict_location)
                            location_list.append(loc)

                        for place in location_list:

                            if place in list(self.df_location['시도'].values):
                                loc = place
                                break

                        apple_feature_arr = ["부사", "아오리", "홍로"]
                        pork_feature_arr = ['구이', '보쌈', '냉장', '냉동']
                        kimchi_feature_arr = ['포기', '배추',
                                              '실비', '깍두기', '열무', '총각', '갓']
                        feature_dict = {'사과': apple_feature_arr,
                                        '삼겹살': pork_feature_arr, '김치': kimchi_feature_arr}
                        kind = dm.get_kind_feature(
                            feature_dict[keyword], name)
                        site = "Emart"
                        date = datetime.now()
                        date = date.strftime('%Y-%m-%d %H:%M:%S')
                        if price != "" and weight != "" and loc != "":
                            df.loc[name] = [date, name, int(price),
                                            float(weight), kind, site, loc]
                except Exception as e:
                    print(str(e))
                    break

        df.to_csv(f'{self.TABLE_NAME}.csv', index=False,
                  encoding='utf-8-sig', mode="w")
        # outlier_idx = self.get_outlier(
        #     df=df, column='price', weight=1.5)

        # df.drop(outlier_idx, axis=0, inplace=True)
        # df.to_csv(f"{self.TABLE_NAME}_remove.csv",
        #           index=False, encoding="utf-8-sig", mode="a")
        db.total(df)
        return super().crawling(db, keyword, total_page)


class GmarketCrawling(Crawling):
    def crawling(self, db, keyword, total_page):
        df = pd.DataFrame(columns=['date', 'title', 'price',
                                   'weight', 'kind', 'site', 'location'])
        ua = UserAgent()
        url = "http://browse.gmarket.co.kr/search?keyword="+keyword
        k = 0

        while k < total_page:
            k += 1
            time.sleep(10)

            print(f'### {self.TABLE_NAME} page : {k}')

            self.header.update({'user-agent': ua.random})

            page_url = "&k=32&p="+str(k)
            page_url = url + page_url
            res = requests.get(page_url, headers=self.header)
            if res.status_code == 401:
                break

            if res.status_code == 200:

                html = bs(res.text, 'lxml')
                # print(html)
                cont = html.find(
                    'div', {'class': 'section__content-body-container'})
                cont0 = cont.find(
                    'div', {'class': 'section__inner-content-body'})
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
                        item1 = item.find(
                            'div', {'class': 'box__item-container'})

                        item2 = item1.find(
                            'div', {'class': 'box__information'})
                        item3 = item2.find(
                            'div', {'class': 'box__information-major'})

                        item_tmp_name = item3.find(
                            'div', {'class': 'box__item-title'})
                        item_name = item_tmp_name.find(
                            'span', {'class': 'text__item'}).text

                        item_tmp_price = item3.find(
                            'div', {'class': 'box__item-price'})
                        item_price = item_tmp_price.find(
                            'strong', {'class': 'text text__value'}).text

                        candid_name = list(item_name.split(" "))
                        # print(candid_name)

                        loc = "None"

                        apple_feature_arr = ["부사", "아오리", "홍로"]
                        pork_feature_arr = ['구이', '보쌈', '냉장', '냉동']
                        kimchi_feature_arr = ['포기', '배추',
                                              '실비', '깍두기', '열무', '총각', '갓']
                        feature_dict = {'사과': apple_feature_arr,
                                        '삼겹살': pork_feature_arr, '김치': kimchi_feature_arr}

                        kind = dm.get_kind_feature(
                            feature_dict[keyword], item_name)
                        location_list = []

                        
                        weight = ""
                        for m in candid_name:
                            if 'kg' in m or 'KG' in m:
                                try:
                                    weight = m.split("kg")[0]
                                except:
                                    weight = m.split("KG")[0]
                                weight = re.sub(r'[^0-9,.]', '', weight)
                            
                            
                            loc = "None"

                            loc = dm.location(
                                m, self.df_location, self.dict_location)
                            location_list.append(loc)

                        for place in location_list:

                            if place in list(self.df_location['시도'].values):
                                loc = place
                                break

                        item_price = int(item_price.replace(',', ''))
                        date = datetime.now()
                        date = date.strftime('%Y-%m-%d %H:%M:%S')
                        site = "Gmarket"
                        if weight != "" and weight != None and item_price != "" :
                            df.loc[item_name] = [date, item_name, item_price, weight, kind, site, loc]

        df.to_csv(f'{self.TABLE_NAME}.csv', index=False,
                  encoding='utf-8-sig', mode="w")
        outlier_idx = self.get_outlier(df=df, column='price', weight=1.5)
        
        df.drop(outlier_idx, axis=0, inplace=True)
        df.to_csv(f"{self.TABLE_NAME}_remove.csv",
                  index=False, encoding="utf-8-sig", mode="a")
        db.total(df)

        return super().crawling(db, keyword, total_page)


class NaverCrawling(Crawling):
    def removeEmoji(self, text):
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)

    def isRepeat(self, previousItemList, itemList):

        # 같은 값을 응답받으면 True 리턴
        if previousItemList['shoppingResult']['products'][0]['productName'] == itemList['shoppingResult']['products'][0]['productName']:
            print('같아서 끝-----')
            return True
        # 아니면 False 리턴
        return False

    def printData(self, db, keyword, itemList, df):
        # 추출하려는 값의 key를 입력

        for i in itemList['shoppingResult']['products']:
            title = self.removeEmoji(i['productName'])
            price = int(i['price'])
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
            feature_dict = {'사과': apple_feature_arr,
                            '삼겹살': pork_feature_arr, '김치': kimchi_feature_arr}
            # 부사홍로

            kind = dm.get_kind_feature(feature_dict[keyword], cValue)

            for words in cValueSplit:
                if "kg" in words or "KG" in words:
                    wordsW = words
                    if "," in words:
                        wordsW = words.split(',')[0]
                    weight = wordsW

            titleSplit = title.split(' ')

            for m in titleSplit:
                location = "NONE"
                location = dm.location(
                    m, self.df_location, self.dict_location)
                location_list.append(location)

            for place in location_list:
                if place in list(self.df_location['시도'].values):
                    location = place
                    break

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
            weight = re.sub(r'[^0-9,.]', '', weight)

            if kind == '':
                kind = dm.get_kind_feature(
                    feature_dict[keyword], title)

            # print(f'## {title}\n{kind}')
            # price = int(price)
            if location != " " and location != "" and price != "":
                df.loc[title] = [date, title, price, weight, kind, site, location]
        return df

    def makeRequestAndGetResponse(self, page, query):
        pageingIndex = page

        params = (
            ('sort', 'rel'),
            ('pagingIndex', pageingIndex),
            ('pagingSize', '20'),
            ('viewType', 'list'),
            ('productSet', 'total'),
            ('deliveryFee', ''),
            ('comNm', ''),
            ('characterValue', ''),
            ('deliveryTypeValue', ''),
            ('frm', 'NVSHATC'),
            ('query', query),
            ('origQuery', query),
            ('iq', ''),
            ('eq', ''),
            ('xq', ''),
            ('crurl', '')
        )

        response = requests.get(
            'https://search.shopping.naver.com/api/search/all', headers=self.header, params=params)
        return response

    def crawling(self, db, keyword, total_page):
        df = pd.DataFrame(columns=['date', 'title', 'price',
                                   'weight', 'kind', 'site', 'location'])
        previousItemList = []        # 중복 체크를 위한 변수

        page = 1
        while page <= total_page:
            self.print_page_status(page)

            # 네이버를 향한 Request 생성 and 네이버로부터 response 받기
            response = self.makeRequestAndGetResponse(page, keyword)

            # json을 리스트로 받기
            itemList = json.loads(response.text)

            # 첫번째 호출에는 list가 비교가 안되니 continue를 한다.
            if page == 1:
                page = page + 1
                previousItemList = itemList
                self.printData(db, keyword, itemList, df)
                continue

        # 반복 응답 Check Method
        # 응답이 같은 값으로 반복되었는지 확인하는 메서드를 실행한다. True일 경우 중복이라서 break
            if self.isRepeat(previousItemList, itemList):
                break

            previousItemList = itemList

            self.printData(db, keyword, itemList, df)
            page = page + 1

        df.to_csv(f'{self.TABLE_NAME}.csv', index=False,
                  encoding='utf-8-sig', mode="w")
        outlier_idx = self.get_outlier(df=df, column='price', weight=1.5)

        df.drop(outlier_idx, axis=0, inplace=True)
        df.to_csv(f"{self.TABLE_NAME}_remove.csv",
                  index=False, encoding="utf-8-sig", mode="a")
        db.total(df)

        return super().crawling(db, keyword, total_page)


class CoupangCrawling(Crawling):
    def crawling(self, db, keyword, total_page):
        products_link = []
        for page in range(1, total_page + 1):
            self.print_page_status(page)
            url = f'https://www.coupang.com/np/search?q={keyword}&channel=user&sorter=scoreDesc&listSize=36&isPriceRange=false&rating=0&page={page}&rocketAll=false'
            response = requests.get(url, headers=self.header)
            soup = BeautifulSoup(response.content, 'html.parser')
            products_lis = soup.find('ul', id='productList').find_all('li')
            for li in products_lis:
                site = "Coupang"
                kind = location = ""
                location_list = []
                name = li.find('div', class_='name').text
                price = ''
                a_li = 0
                result = name.split(' ')
                for m in result:
                    location = "NONE"
                    location = dm.location(
                        m, self.df_location, self.dict_location)
                    location_list.append(location)

                for place in location_list:
                    if place in list(self.df_location['시도'].values):
                        location = place
                        break

                for word in result:
                    if 'KG' in word:
                        a_li = word.split("KG")[0]
                    elif 'kg' in word:
                        a_li = word.split("kg")[0]
                    # elif 'g' in word:
                    #     a_li = word.split("g")[0]

                # weight = a_li[0]
                weight = re.sub(r'[^0-9,.]', '', str(a_li))
                weight = weight.split("~")[0]

                price = li.find('strong', class_='price-value').text

                date = datetime.now()
                date = date.strftime('%Y-%m-%d %H:%M:%S')

                apple_feature_arr = ["부사", "아오리", "홍로"]
                pork_feature_arr = ['구이', '보쌈', '냉장', '냉동']
                kimchi_feature_arr = ['포기', '배추', '실비', '깍두기', '열무', '총각', '갓']
                feature_dict = {'사과': apple_feature_arr,
                                '삼겹살': pork_feature_arr, '김치': kimchi_feature_arr}
                # 부사홍로

                price = (re.sub(r'[^0-9,.]', '', price))
                price = price.replace(",", "")

                kind = dm.get_kind_feature(
                    feature_dict[keyword], name)
                # location = get_feature_location(city_arr, name)

                price = int(price)

                products_info = {
                    'date': date,
                    'title': name,
                    'price': price,
                    'weight': weight,
                    'kind': kind,
                    'site': site,
                    'location': location
                }
                if products_info['weight'] != 0 and products_info['location'] != "":
                    products_link.append(products_info)

        df = pd.DataFrame(products_link)
        df.to_csv(f'{self.TABLE_NAME}.csv', index=False,
                  encoding='utf-8-sig', mode="w")
        outlier_idx = self.get_outlier(df=df, column='price', weight=1.5)

        df.drop(outlier_idx, axis=0, inplace=True)
        df.to_csv(f"{self.TABLE_NAME}_remove.csv",
                  index=False, encoding="utf-8-sig", mode="a")
        db.total(df)

        return super().crawling(db, keyword, total_page)
