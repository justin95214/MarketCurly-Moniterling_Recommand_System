from cmath import nan
from django.shortcuts import render
from django.http import HttpResponse
import pymysql
import re
import numpy as np
import pandas as pd


def main_page(request): #아무것도 없는 첫화면
    city_values = {
        "서울특별시":0,
        "부산광역시":0,
        "대구광역시":0,
        "인천광역시":0,
        "광주광역시":0,
        "대전광역시":0,
        "울산광역시":0,
        "세종특별자치시":0,
        "경기도":0,
        "강원도":0,
        "충청북도":0,
        "충청남도":0,
        "전라북도":0,
        "전라남도":0,
        "경상북도":0,
        "경상남도":0,
        "제주특별자치도":0
    }
    return render(request, 'polls/main.html', {'city_values':city_values})



def filter(market_list_input, df):
    # 필터 마켓 리스트
    result_df = pd.DataFrame()
    for market in market_list_input:
        tmp_df = df[df['site'] == market].copy()
        print(tmp_df)
        result_df = pd.concat([result_df, tmp_df], ignore_index= True)

    print(result_df['price'].values.tolist())
    print(result_df['weight'].values.tolist())
    result_df['unit_price'] = result_df['price']/result_df['weight']

    # one_df = pd.pivot_table(result_df,                # 피벗할 데이터프레임
    #                  index = 'location',    # 행 위치에 들어갈 열
    #                  columns = 'unit_price',    # 열 위치에 들어갈 열
    #                  values = 'price',     # 데이터로 사용할 열
    #                  aggfunc = 'count')
    
    return one_df


def read_total_data():
    conn = pymysql.connect(
    host='awskurly.caeqso43nbt7.ap-northeast-2.rds.amazonaws.com',
    user='awsusr',
    password='12345678',
    db='daduckDB')  
  
    curs = conn.cursor()

    #쿠팡
    curs.execute("SELECT * FROM Total WHERE price >0 and weight>0") 
    item_list = curs.fetchall()
    item_df = pd.DataFrame(item_list, columns=[['date','title','price','weight','kind','site','location']])
    return item_df


def calc_city_avg(df, city_list):
    city_dict = {}
    for city in city_list:
        total = 0
        count = 0
        for index, row in df.iterrows():
            if row['location'] == city:
                #if row['price'].isdigit():
                total += row['price']
                count += 1
        mean_value = 0
        if count != 0:
            mean_value = total / count
        temp = f'"{city}"'
        city_dict[temp] = mean_value
    
    return city_dict

def submit(request): 
    productname = request.POST.get('productname') #상품명
    date = request.POST.get('date') #날짜
    market_list = request.POST.getlist('selected') 

        # Initialize example dataframe
    data = {
        'Week': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5],
        'Color': ['Green', 'Red', 'Green', 'Yellow', 'Red', 'Green', 'Yellow', 'Red', 'Yellow', 'Red'],
        'Part': ['A', 'A', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'B'],
        'Value': [10, -20, 20, -20, -10, 10, -5, -8, -9, -10]
    }
    df = pd.DataFrame(data)

    # Merge 'Color' and 'Value' columns into one single column
    df['Value'] = list(zip(df.Color, df.Value))

    # Perform pivot operation
    df = df.pivot(index='Part', columns='Week', values='Value')

    # Split into two dataframes: a colors dataframe and a numerical values dataframe
    color_df = df.applymap(lambda x: x[0])
    value_df = df.applymap(lambda x: x[1])

    # Transform dataframe with colors into formatting commands
    color_df = color_df.applymap(lambda x: f'background-color: {x.lower()}')

    # Apply color styling to values dataframe
    data0 = value_df.style.apply(lambda x: color_df, axis=None)
    #styled_df.to_excel('output.xlsx')

    EVEN_ROW_COLOR = "#00BFFF"
    #data0 = pd.read_csv("https://raw.githubusercontent.com/justin95214/MarketCurly-Moniterling_Recommand_System/main/test11.csv", encoding="utf8")
    # data0 = pd.DataFrame(data)
   

    # data0 = filter(market_list, data0)
    ###
    #data0 = pd.DataFrame(data)
    #data0.style.applymap(draw_color_cell,color='#ff9090',subset=pd.IndexSlice[0:2,'GDP':'hi'])
    # data0 = data0.style.set_table_styles(
    #  [{'selector': 'td:hover',
    #      'props': [('font-size', '25px')]}]
    # )  
    #context = 'df':data0.to_html()
    request.session['test'] = productname

    data = read_total_data()
    city_list = ["서울특별시"
"부산광역시",
"대구광역시",
"인천광역시",
"광주광역시",
"대전광역시",
"울산광역시",
"세종특별자치시",
"경기도",
"강원도",
"충청북도",
"충청남도",
"전라북도",
"전라남도",
"경상북도",
"경상남도",
"제주특별자치도"]
    # temp_list = []
    # for market in market_list:
    #     temp = None
    #     for index, row in data.iterrows():
    #         if row['location'] == market:
    #             temp = data.iloc[index]
    #             temp_list.append(temp)

    # print(temp_list)
    # filter_data = pd.concat(temp_list, axis = 0)
    city_values = calc_city_avg(data, city_list)
    
    return render(request,'polls/main.html',{'productname':productname, 'city_values':city_values, 'df':data.to_html(),'market_list':market_list})

def margin(request):
    conn = pymysql.connect(
    host='awskurly.caeqso43nbt7.ap-northeast-2.rds.amazonaws.com',
    user='awsusr',
    password='12345678',
    db='daduckDB')

    # conn = pymysql.connect(
    # host='awskurly.caeqso43nbt7.ap-northeast-2.rds.amazonaws.com',
    # user='awsusr',
    # password='12345678',
    # db='daduckDB')

  

    curs = conn.cursor()
  
    productname = request.session['test']
    marginpercent = request.POST.get('margin')


    #쿠팡
    curs.execute("SELECT max(coupang) FROM crawling.margintable where coupang ") 
    item_list = curs.fetchall()
    for i in item_list:
        print(i)
    coumax = re.sub(r'[^0-9]', '', str(i))
   
    curs.execute("SELECT min(coupang) FROM crawling.margintable where coupang ") 
    item_list2 = curs.fetchall()
    for j in item_list2:
        print(j)
    coumin = re.sub(r'[^0-9]', '', str(j))

    #네이버
    curs.execute("SELECT max(naver) FROM crawling.margintable where naver ") 
    item_list = curs.fetchall()
    for i in item_list:
        print(i)
    navmax = re.sub(r'[^0-9]', '', str(i))
   
    curs.execute("SELECT min(naver) FROM crawling.margintable where naver ") 
    item_list2 = curs.fetchall()
    for j in item_list2:
        print(j)
    navmin = re.sub(r'[^0-9]', '', str(j))

    #이마트
    curs.execute("SELECT max(emart) FROM crawling.margintable where emart ") 
    item_list = curs.fetchall()
    for i in item_list:
        print(i)
    emax = re.sub(r'[^0-9]', '', str(i))
   
    curs.execute("SELECT min(emart) FROM crawling.margintable where emart ") 
    item_list2 = curs.fetchall()
    for j in item_list2:
        print(j)
    emin = re.sub(r'[^0-9]', '', str(j))

    #G마켓
    curs.execute("SELECT max(gmarket) FROM crawling.margintable where gmarket ") 
    item_list = curs.fetchall()
    for i in item_list:
        print(i)
    gmax = re.sub(r'[^0-9]', '', str(i))
   
    curs.execute("SELECT min(gmarket) FROM crawling.margintable where gmarket ") 
    item_list2 = curs.fetchall()
    for j in item_list2:
        print(j)
    gmin = re.sub(r'[^0-9]', '', str(j))

   
    
    
    conn.close()
    return render(request,'polls/main.html',{'productname':productname,'marginpercent':marginpercent,'coumax':coumax,
    'coumin':coumin,'navmax':navmax,'navmin':navmin,'emax':emax,'emin':emin,'gmax':gmax,'gmin':gmin})

def test(request):
    return render(request,'polls/test2.html')




