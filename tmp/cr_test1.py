import json
import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table
import warnings
import time







result = []

i=0


cat = input('상품을 입력하시오')


url = "http://browse.gmarket.co.kr/search?keyword="+cat




while True:
	i+=1
	time.sleep(15)
	ua = UserAgent()

	print(f'page : {i}')
	
	custom_header ={
        'referer': 'http://www.gmarket.co.kr/',
        #'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'user-agent': ua.random,  
        'authority': 'stags.bluekai.com'
	}
	
	custom_header.update({'user-agent': ua.random})

	res = requests.get(url.format(i), headers= custom_header)
	if res.status_code == 401:
		break;

	if res.status_code == 200:
		html = bs(res.text, 'lxml')
		print(html)
