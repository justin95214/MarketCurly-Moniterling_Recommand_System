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

#####
import which_loc2 as which
import read_loc_data as csv_data

def check_arr_feature(feature, product_split):
    for product_tmp in product_split:
        if feature in product_tmp:
            return feature
    else:
        return ''

def get_kind_feature(feature_arr, product_name):
    product_split = product_name.split()
    check_arr = set()
    for feature in feature_arr:
        check_arr.add(check_arr_feature(feature, product_split))

    kind = ''
    check_arr = list(check_arr)
    if any(check_arr):
        check_arr.sort()
        if check_arr.count('') < len(feature_arr) - 1:
            kind = check_arr[-1]
        else:
            kind = ''.join(check_arr)

    return kind


result = []

k=0


cat = input('상품을 입력하시오 : ')


url = "http://browse.gmarket.co.kr/search?keyword="+cat


df_location = csv_data.read_location_csv()
dict_location = csv_data.to_dict(df_location)

while True:
	k+=1
	time.sleep(10)
	ua = UserAgent()

	print(f'page : {k}')
	
	custom_header ={
        'referer': 'http://www.gmarket.co.kr/',
        #'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'user-agent': ua.random,  
        'authority': 'stags.bluekai.com'
	}
	
	custom_header.update({'user-agent': ua.random})

	res = requests.get(url.format(k), headers= custom_header)
	print(res.status_code)
	if res.status_code == 401:
		break;

	if res.status_code == 200:
		
		html = bs(res.text, 'lxml')
		#print(html)
		cont = html.find('div', {'class':'section__content-body-container'})
		cont0 = cont.find('div', {'class':'section__inner-content-body'})
		cont1 = cont0.findAll('div', {'class':'section__module-wrap'})
		for i in cont1:


			#print("=========================================")
			#print(i)

			item0 = i.findAll('div', {'class':'box__component box__component-itemcard box__component-itemcard--general'})
			#print(item0)		
			for item in item0:
				#print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
				#print(item)		
				#item1 = item0.find('div', {'class':'box__information-major'})
				item1 = item.find('div', {'class':'box__item-container'})

				item2 = item1.find('div', {'class':'box__information'})
				item3 = item2.find('div', {'class':'box__information-major'})

				item_tmp_name = item3.find('div', {'class':'box__item-title'})
				item_name = item_tmp_name.find('span', {'class':'text__item'}).text	

				item_tmp_price = item3.find('div', {'class':'box__item-price'})
				item_price = item_tmp_price.find('strong', {'class':'text text__value'}).text

				weight = 'None'
				candid_name = list(item_name.split(" "))
				#print(candid_name)
				
				loc="None"

				feature_arr = ["부사", "아오리", "홍로"]
				kind = get_kind_feature(feature_arr, item_name)
				map_dict={}
				location_list = []

				weight_root=""
				for m in candid_name:
					if 'kg' in m or 'KG' in m :
						try:
							weight = m.split("kg")[0]
						except:
							weight = m.split("KG")[0]
						weight = re.sub(r'[^0-9,.,~]','',weight)
						weight_root = weight.split("~")[0] +'kg'
					#print(m)
					
					loc="None"

					loc = which.location(m, df_location, dict_location)
					location_list.append(loc)
				print(location_list)
				
				for place in location_list:

					if place in list(df_location['시도'].values):
						loc = place
						break;
																		
				print(f'name : {item_name} | kind : {kind} | location : {loc} | price : {item_price} | weight : {weight_root}')

