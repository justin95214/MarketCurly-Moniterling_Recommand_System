import json
import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table
import warnings
import re
###############################
import which_loc2 as which
import read_loc_data as csv_data

warnings.filterwarnings("ignore")

def get_engine():
	engine = create_engine(engineUrl,convert_unicode=True)
	return engine


def init_db():
	Base.metadata.create_all(engine)


def insertDB(id,scrap_time, title, post_time):
	insert_table.execute(
		name= str(id),
		price=str(scrap_time),
		unit=str(title),
		unit_price=str(post_time)
		)
	print('데이터베이스 삽입완료')
"""		
print("mysql비밀번호를 넣으시오")
engineUrlinput = input()

print("mysql database이름을 넣으시오")
databaseName = input()

engineUrl = 'mysql+pymysql://root:' +engineUrlinput +'@localhost/' +databaseName +'?charset=utf8mb4'

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

table = Table('stock_test0', metadata, autoload=True)
insert_table = table.insert()

conn.execute('SET NAMES utf8;')
conn.execute('SET CHARACTER SET utf8;')
conn.execute('SET character_set_connection=utf8;')

"""
ua = UserAgent()
cat = input()


url = "https://emart.ssg.com/search.ssg?target=all&query="+cat

print(ua.random)
"""
custom_header ={
	#'referer': 'https://www.ssg.com/search.ssg?target=all&query=%EB%B3%B5%EC%88%AD%EC%95%84&src_area=late',
	'referer': 'https://emart.ssg.com/search.ssg?target=all&query=%EC%82%AC%EA%B3%BC',
	#'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
	'user-agent': ua.random,
	#'authority': 'api.mediacategory.com',
	#'authority': 'simg.ssgcdn.com',
	#'authority': 'tk.mediacategory.com',
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}
"""

df_location = csv_data.read_location_csv()
dict_location = csv_data.to_dict(df_location)


#custom_header.update({'user-agent': ua.random})

#req = requests.get(url, headers= custom_header)
#json_txt = req.text
#print(json_txt)

result = []

i=0
import time

while True:
	i+=1
	time.sleep(15)
	print(f'page : {i}')

	
	page_url =  "&page="+str(i)
	
	custom_header ={
        #'referer': 'https://www.ssg.com/search.ssg?target=all&query=%EB%B3%B5%EC%88%AD%EC%95%84&src_area=late',
        'referer': 'https://emart.ssg.com/search.ssg?target=all&query=%EC%82%AC%EA%B3%BC',
        #'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'user-agent': ua.random,  
        #'authority': 'api.mediacategory.com',
        'authority': 'simg.ssgcdn.com',
        #'authority': 'tk.mediacategory.com',
	}
	
	custom_header.update({'user-agent': ua.random})

	res = requests.get(url+page_url, headers= custom_header)
	if res.status_code == 401:
		break;

	if res.status_code == 200:
		html = bs(res.text, 'lxml')	
		#print(html)		
		cont0 = html.find('div', {'class' : 'tmpl_itemlist'})
		cont1 = cont0.find('ul', {'class' : 'cunit_thmb_lst cunit_thmb_lst4 cunit_thmb_w1000'})
		#print(cont)
		try:
			items = cont1.findAll('li', {'class' : 'cunit_t232'})	
			for item0 in items:
				item1 = item0.find('div', {'class' : 'cunit_info'})
				unit_price=None

				name = item1.find('em', {'class' : 'tx_ko'}).text
				price = item1.find('em', {'class' : 'ssg_price'}).text
				unit_tx = item1.find('span', {'class' : 'ssg_tx'}).text
				try:
					unit_price = item1.find('div', {'class' : 'unit'}).text[1:-1]
				except:
					pass
				
				#insertDB(name, price, unit_tx, unit_price)


				weight_root=""

				loc="None"
				map_dict={}
				location_list = []
				candid_name = list(name.split(" "))

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

				#print(location_list)
				
				for place in location_list:

					if place in list(df_location['시도'].values):
						loc = place
						break;


				print(f' product : {name} | price :{price}{unit_tx} | unit : \
{unit_price} | weight " {weight_root} | location : {loc}')
		except Exception as e:

			print(str(e))
			break
