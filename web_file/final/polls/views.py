from cmath import nan
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import pymysql
import re
import numpy as np
import pandas as pd
# from pivot import make_pivot, make_heatmap, make_color

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
                total += row['price']
                count += 1
        mean_value = 0
        if count != 0:
            mean_value = total / count
        city_dict[city] = mean_value

    return city_dict

def submit(request): 
    productname = request.POST.get('productname') #상품명
    date = request.POST.get('date') #날짜
    market_list = request.POST.getlist('selected') 

    conn = pymysql.connect(
    host='awskurly.caeqso43nbt7.ap-northeast-2.rds.amazonaws.com',
    user='awsusr',
    password='12345678',
    db='daduckDB')  
    
    curs = conn.cursor()

  
    curs.execute("select * from Total where DATE(%s)",date) #상품명,
   
    item_date = curs.fetchall()
    print(item_date)
    

    # data0 = read_total_data()
    # result = filter(market_list, data0)
    # table = make_pivot(result)
    #table = make_color(result)
    # make_heatmap(table)

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
    city_list = [
        "서울특별시",
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
        "제주특별자치도"
    ]

    result = calc_city_avg(data, city_list)
    response_dict = {
        'productname':productname,
        'df':data.to_html(),
        'market_list':market_list
    }
    for city in city_list:
        response_dict[city] = result[city] 

    return render(request,'polls/main.html', response_dict)


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
