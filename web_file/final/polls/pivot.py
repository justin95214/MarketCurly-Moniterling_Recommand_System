import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

import matplotlib.colors as mcl

matplotlib.rcParams['axes.unicode_minus'] =False

#네이버/쿠팡/지마켓/이마트
def filter(market_list, total_df):

	naver_df = pd.DataFrame()  
	coupang_df = pd.DataFrame()
	gmarket_df = pd.DataFrame()
	emart_df = pd.DataFrame()

	if 'Naver' in market_list:
		#naver_df = pd.read_csv("./naver.csv", encoding='utf8')
		naver_df = total_df[total_df['site']=='Naver'].copy()
	
		naver_df['unit_price'] = naver_df['price'].copy()
		naver_df['unit_price'] = naver_df['unit_price'].round(-3)
		naver_df['price'] = naver_df['unit_price']* naver_df['weight']
		naver_df.fillna(np.NaN)
		naver_df['weight'].dropna()
		total_df = pd.concat([total_df, naver_df],  ignore_index=True)

	if 'Coupang' in market_list:
		#coupang_df = pd.read_csv("./coupang.csv", encoding='utf8')
		coupang_df = total_df[total_df['site']=='Coupang'].copy()
		coupang_df['unit_price'] = coupang_df['price'].copy()
		coupang_df['unit_price'] = coupang_df['unit_price'].round(-3)
		coupang_df['price'] = coupang_df['unit_price']* coupang_df['weight']
		#coupang_df['unit_price'] = coupang_df['unit_price']
		total_df = pd.concat([total_df, coupang_df],  ignore_index=True)
		

	if 'Gmarket' in market_list:
		#gmarket_df = pd.read_csv("./gmarket.csv", encoding='utf8')
		gmarket_df = total_df[total_df['site']=='Gmarket'].copy()
		gmarket_df['weight'].replace('None',np.NaN)
		gmarket_df['weight'].dropna()
		print(gmarket_df['weight'].values.tolist())		
	
		idx = gmarket_df[gmarket_df['weight']=='9~10'].index
		
		gmarket_df['weight'] = gmarket_df['weight'].drop(idx)
		gmarket_df['weight'] = gmarket_df['weight'].astype('float')
	
		gmarket_df['unit_price'] = gmarket_df['price']/gmarket_df['weight']
		#gmarket_df['unit_price'] = gmarket_df['unit_price'].round(-3)

		#gmarket_df['unit_price'] = gmarket_df['unit_price']
		gmarket_df = pd.concat([total_df, gmarket_df],  ignore_index=True)

	return total_df



## 특정 위치의 배경색 바꾸기
def draw_color_cell(x,color):
	color = f'background-color:{color}'
	return color 

	


def make_pivot(df):
	
	df.style.applymap(draw_color_cell,color='#ff9090',subset=pd.IndexSlice[2:5,'kind':'site'])
	df.to_csv("result_temp.csv", encoding='cp949')
	df0 = pd.pivot_table(df, index='location', columns = 'unit_price', values='price', aggfunc='count')
	df0 = df0.fillna(0)
	print(df0.columns)
	#df0.style.applymap(draw_color_cell,color='#ff9090',subset=pd.IndexSlice[2:5,'1333':'1490'])
	return df0


def make_color(df):
	df.dropna()
	sum = df['unit_price'].sum()
	print(df['unit_price'].values.tolist())
	df['dist'] = df['unit_price']/ sum
	print(df['dist'].values.tolist()) 

	df0 = pd.pivot_table(df, index='location', columns = 'unit_price', values='price', aggfunc='count')
	loc_df = df.applymap(lambda x : x[0])
	print(loc_df)
	return df0

def make_heatmap(df):

	h = 9
	s = 0.99 #현재 예제에선 필요없음
	v = 1

	colors = [mcl.hsv_to_rgb((h/360,0,v)),mcl.hsv_to_rgb((h/360,0.5,v)),mcl.hsv_to_rgb((h/360,1,v))]

	cmap = LinearSegmentedColormap.from_list('my_cmap',colors,gamma=2)

	fig, axes = plt.subplots(figsize=(50,10))
	sns.heatmap(df, cmap=cmap, ax=axes, annot=True)
	plt.rcParams['font.family'] ='Malgun Gothic'
	plt.rc('font', family='AppleGothic') #맥
	#plt.rcParams['axes.unicode_minus'] = False 
	plt.xlabel('unit_price')
	plt.ylabel('location')
	plt.xticks(rotation =90)
	plt.savefig('temp.png')
	plt.show()


"""
result = filter(True, True, False, True)
table = make_pivot(result)
#table = make_color(result)
make_heatmap(table)


table.to_excel("result.xlsx", encoding='cp949', engine='openpyxl')
print(table)


"""



