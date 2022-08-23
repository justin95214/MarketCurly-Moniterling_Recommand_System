from django.shortcuts import render
from django.http import HttpResponse
import pymysql
import re
import numpy as np
import pandas as pd


def first(request): #아무것도 없는 첫화면
    return render(request,'polls/first.html')


def rain_condition(v):
    if v < 1.75:
        return "Dry"
    elif v < 2.75:
        return "Rain"
    return "Heavy Rain"

def make_pretty(styler):
    styler.set_caption("Weather Conditions")
    styler.format(rain_condition)
    styler.format_index(lambda v: v.strftime("%A"))
    styler.background_gradient(axis=None, vmin=1, vmax=5, cmap="YlGdnBu")
    return styler


def submit(request): 
    productname = request.POST.get('productname')

    ## 특정 위치의 배경색 바꾸기
    def draw_color_cell(x,color):
        color = f'background-color:{color}'
        return color
 
    data = {
        'year': [2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,1,1,1,1,1],
        'GDP rate': [2.8, 3.1, 3.0,2.8, 3.1, 3.0,2.8, 3.1, 3.0,2.8, 3.1, 3.0,2.8, 3.1, 3.0,2.8, 3.1, 3.0,2.8, 3.1, 3.0,1,1,1,1,1],
        'GDP': ['1.637M', '1.73M', '1.83M','1.637M', '1.73M', '1.83M','1.637M', '1.73M', '1.83M','1.637M', '1.73M', '1.83M','1.637M', '1.73M', '1.83M','1.637M', '1.73M', '1.83M','1.637M', '1.73M', '1.83M',1,1,1,1,1],
        'hi1': [2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,1,1,1,1,1],
        'hi2': [2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,1,1,1,1,1],
        'hi3': [2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,1,1,1,1,1],
        'hi4': [2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,1,1,1,1,1],
        'hi5': [2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,1,1,1,1,1],
        'hi6': [2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,1,1,1,1,1],
        'hi7': [2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,1,1,1,1,1],
        'hi8': [2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,1,1,1,1,1],
        'hi9': [2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,1,1,1,1,1],
        'hi10': [2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,1,1,1,1,1],
        'hi11': [2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,2016, 2017, 2018,1,1,1,1,1],

        
        
    }

    EVEN_ROW_COLOR = "#00BFFF"
    #data0 = pd.read_csv("https://raw.githubusercontent.com/justin95214/MarketCurly-Moniterling_Recommand_System/main/test11.csv", encoding="utf8")
    data0 = pd.DataFrame(data)
    data0.style.apply(draw_color_cell,color='#ff9090',subset=pd.IndexSlice[1,['GDP']])

    weather_df = pd.DataFrame(np.random.rand(10,2)*5,
                          index=pd.date_range(start="2021-01-01", periods=10),
                          columns=["Tokyo", "Beijing"])


    weather_df.loc["2021-01-04":"2021-01-08"].style.pipe(make_pretty)
    #data0 = pd.DataFrame(data)

    #data0 = data0.style.set_table_styles(
    #[dict(selector='td', props='font-size : 5px; '),dict(selector='tr', props='font-size : 5px;'),dict(selector = 'tbody tr:nth-child(even)', props='background-color: #00BFFF;')]
    #) 
  
    #data0.style.applymap(draw_color_cell,color='#ff9090',subset=pd.IndexSlice[0:2,'GDP':'hi'])

   
    # data0 = data0.style.set_table_styles(
    #  [{'selector': 'td:hover',
    #      'props': [('font-size', '25px')]}]
    # )  
    

    #data0 = pd.read_csv("test11.csv", encoding="utf8")
    #context = 'df':data0.to_html()
    
    request.session['test'] =productname
    
    return render(request,'polls/main.html',{'productname':productname, 'df':weather_df.to_html()})
def margin(request):
    conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='227899',
    db='crawling')


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
    return render(request,'polls/margin.html',{'productname':productname,'marginpercent':marginpercent,'coumax':coumax,
    'coumin':coumin,'navmax':navmax,'navmin':navmin,'emax':emax,'emin':emin,'gmax':gmax,'gmin':gmin})

def test(request):
    return render(request,'polls/test2.html')




