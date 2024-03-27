from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime, timedelta
from datetime import date
import time
import json
import subprocess
import keyring
import requests
import json
import numpy as np
import pandas as pd
import webbrowser
import matplotlib.pyplot as plt
import quantstats as qs
import yfinance as yf
import shutil
import matplotlib.pyplot as plt
from portfolio.utilis.calculator import Calculator
from portfolio.utilis.class_trial import StockData
from cqrsite.utils.pdUpdater import cqrDB
from cqrsite.views import HomeView
from .forms import QuestionForm
from .models import ModelPort, Portfolio, Profile, Questionarie, dailyMPweight, dailyMPvalue, monthlyMPvalue, MPclsweight
from .kisapi import get_app_key, get_app_secret, checkbalance, get_ak

from cqrsite.utils.system_ver1 import systemtrade
import os
os.environ['MPLBACKEND'] = 'Agg'


# 기본할로윈: 모델포트폴리오를 만들고, 일별수익률, 월별수익률, 자산별투자비중, 종목별투자비중, 리밸런싱발생내역 생성 
def algo(request): 
    tic = ["069500.KS", "229200.KS",
             "133690.KS", "143850.KS",
             "114260.KS", "153130.KS", "157450.KS"
             ] #KODEX, Bonds, NASDAQ, S&P, Cash, MMF, KOSDAQ
    fromdate = "2012-01-01"
    todate = date.today().strftime("%Y-%m-%d")

    stock_data = StockData(tic) 
    data = stock_data.download_data(fromdate, todate,'1d') 
    data.Close.dropna(thresh = 6)
    df,ret = stock_data.clean()
    
    odd_stock_w = 1
    odd_bond_w = 0
    even_stock_w = 1
    even_bond_w = 0
    even_passive_stock_w = 1
    even_passive_bond_w = 0

    odd_buy = np.array([0.4*odd_stock_w, (1/3*odd_bond_w), 0.0*odd_stock_w, 0.0*odd_stock_w, (1/3*odd_bond_w), (1/3*odd_bond_w), 0.6*odd_stock_w])          # Even 11 - Odd 4. Active
    odd_hold = np.array([0.0*odd_stock_w, (1/3*odd_bond_w), 0.5*odd_stock_w, 0.5*odd_stock_w, (1/3*odd_bond_w), (1/3*odd_bond_w), 0.0*odd_stock_w])         # Odd 5 - Odd 10. 
    even_buy = np.array([0.5*even_stock_w, (1/3*even_bond_w), 0.0*even_stock_w, 0.0*even_stock_w, (1/3*even_bond_w), (1/3*even_bond_w), 0.5*even_stock_w])  # Odd 11 - Even 4. NOTE: Here, we shift Kospi weight to Nasdaq instead of S&P 500 to be consistent with our logic that 11-4 should be more aggressive than 5-10. 
    even_hold = np.array([0.0*even_passive_stock_w, (1/3*even_passive_bond_w), 0.5*even_passive_stock_w, 0.5*even_passive_stock_w, (1/3*even_passive_bond_w), (1/3*even_passive_bond_w), 0.0*even_passive_stock_w])  # Even 5 - Even 10

    halloween_adj = stock_data.algo1(1000,odd_buy,odd_hold,even_buy,even_hold) #할로윈변형 호출
    
    stock_data.results()[0]
    stock_data.results()[1]
 
    now = datetime.now()
    formatted_now = now.strftime("%Y%m%d")  

    # 1. 일별수익률추이
    source_file_path = rf'portfolio/templates/적극형_일별수익률추이{formatted_now}.csv'
    destination_file_path = r'portfolio/templates/적극형_일별수익률추이.csv'
    daily_ret = stock_data.daily_ret() 
    daily_ret.to_csv(destination_file_path)
    #shutil.copy(source_file_path, destination_file_path)

    # 2. 월별수익률추이
    source_file_path = rf'portfolio/templates/적극형_월별수익률추이{formatted_now}.csv'
    destination_file_path = r'portfolio/templates/적극형_월별수익률추이.csv'
    monthly_ret = stock_data.monthly_ret() 
    monthly_ret.to_csv(destination_file_path)
    #shutil.copy(source_file_path, destination_file_path)
    
    # 3. 자산별투자비중추이
    source_file_path = rf'portfolio/templates/적극형_자산별투자비중추이{formatted_now}.csv'
    destination_file_path = r'portfolio/templates/적극형_자산별투자비중추이.csv'   
    port_weights = stock_data.portfolio_by_asset_class() 
    port_weights = port_weights[1]
    port_weights.to_csv(destination_file_path)
    #shutil.copy(source_file_path, destination_file_path)
    
    # 4. 종목별투자비중추이
    source_file_path = rf'portfolio/templates/적극형_종목별투자비중추이{formatted_now}.csv'
    destination_file_path = r'portfolio/templates/적극형_종목별투자비중추이.csv'  
    cls_weight=stock_data.portfolio_by_ind_assets() 
    cls_weight.to_csv(destination_file_path)
    #shutil.copy(source_file_path, destination_file_path)
   
    # 5. 리밸런싱발생내역
    source_file_path = rf'portfolio/templates/적극형_리밸런싱발생내역{formatted_now}.csv'
    # destination_file_path = r'portfolio/templates/적극형_리밸런싱발생내역.csv'     
    # rebal_history = stock_data.rebalance_history()  
    # rebal_history.to_csv(destination_file_path)
    #shutil.copy(source_file_path, destination_file_path)

    # extend pandas functionality with metrics, etc.
    qs.extend_pandas()
    daily_ret.iloc[:,1]
    
    html_file_path = rf'portfolio/templates/portfolio/AdjHalloween_all.html'

    qs.reports.html(daily_ret['일별수익률']     
                , benchmark="^GSPC", output=html_file_path, title='Halloween_kospi_kosdaq')
    #webbrowser.open(html_file_path)

    #return HttpResponse("success")
    return render(request, 'portfolio/AdjHalloween_all.html')


# 할로윈변형 (짝수해,홀수해) 
def algo1(request):

    # Halloween Adjusted 짝수 홀수 11 - 4 월 (아빠)

    # (짝수해10월말진입. 홀수해 4월말청산): 주식7(코스닥 30% 코스피20% S&P 20% 나스닥30% 주식비중) 채권3 
    # (홀수해 5-10월): 코스닥 30%를 ‘TIGER CD금리투자’(현금)로 교체
    # (홀수해11-짝수해4월): 주식5(코덱스200만). 채권5
    # (짝수해 5-10월): 주식3(코덱스200만). 채권7
        
    tic = ["069500.KS", "229200.KS",
             "133690.KS", "143850.KS",
             "114260.KS", "153130.KS", "157450.KS"
             ]
    stock_data = StockData(tic) #KODEX, Bonds, NASDAQ, S&P, Cash, MMF, KOSDAQ
    data = stock_data.download_data('2000-01-01', '2024-2-20','1d') 
    data.Close.dropna(thresh = 6)
    df,ret = stock_data.clean()
        
    halloween_adj = stock_data.algo1(10000000)
    stock_data.results()[0]
    
    daily_ret = stock_data.daily_ret()  # 1. 일별수익률추이
    
    monthly_ret = stock_data.monthly_ret() # 2. 월별수익률추이
    
    port_weights = stock_data.portfolio_by_asset_class() # 3. 자산별투자비중추이
    port_weights[1]
    
    stock_data.portfolio_by_ind_assets() # 4. 종목별투자비중추이
   
    stock_data.rebalance_history() # 5. 리밸런싱발생내역

    qs.extend_pandas()
    daily_ret.iloc[:,1]

    # Format the date and time as a string in the desired format, e.g., "YYYY-MM-DD_HH-MM-SS"
    # Construct the file path including the formatted date and time
    now = datetime.now()
    formatted_now = now.strftime("%Y%m%d_%H%M")  
    html_file_path = rf'C:\kannie\Halloween_kospi_{formatted_now}.html'

    qs.reports.html(daily_ret.iloc[:,1], benchmark="^KS11", output=html_file_path, title='Halloween1_KS11')
    webbrowser.open(html_file_path)

    return HttpResponse(html_file_path)

# 할로윈변형 (짝수해,홀수해, 월 변경)
def algo2(request):
    tic = ["069500.KS", "229200.KS",
             "133690.KS", "143850.KS",
             "114260.KS", "153130.KS", "157450.KS"
             ]
    stock_data = StockData(tic) #KODEX, Bonds, NASDAQ, S&P, Cash, MMF, KOSDAQ
    data = stock_data.download_data('2000-01-01', '2024-2-20','1d') 
    data.Close.dropna(thresh = 6)
    df,ret = stock_data.clean()

    halloween_adj = stock_data.algo2(10000000)

    stock_data.results()[0]
    stock_data.results()[1]

    daily_ret = stock_data.daily_ret()  # 1. 일별수익률추이
   
    monthly_ret = stock_data.monthly_ret() # 2. 월별수익률추이
   
    port_weights = stock_data.portfolio_by_asset_class() # 3. 자산별투자비중추이
    port_weights[1]
    
    stock_data.portfolio_by_ind_assets() # 4. 종목별투자비중추이
    
    stock_data.rebalance_history() # 5. 리밸런싱발생내역

    qs.extend_pandas()
    daily_ret.iloc[:,1]
    
    # Format the date and time as a string in the desired format, e.g., "YYYY-MM-DD_HH-MM-SS"
    # Construct the file path including the formatted date and time
    now = datetime.now()
    formatted_now = now.strftime("%Y%m%d_%H%M")  
    html_file_path = rf'C:\kannie\Halloween_kospi_{formatted_now}.html'

    qs.reports.html(daily_ret.iloc[:,1], benchmark="^KS11", output=html_file_path, title='Halloween2_KS11')
    webbrowser.open(html_file_path)

    return HttpResponse(html_file_path)

def algo_View(request):
    return render(request, 'portfolio/AdjHalloween_all.html')

def algo1_View(request):
    return render(request, 'portfolio/templates/AdjHalloween_all.html')

def algo2_View(request):
    return render(request, 'portfolio/templates/Halloween_all_2.html')

def rebalancing(request):

 
    keyring.set_password('real_app_key', 'a_kannie', 'PSnvAltwjE5ZrOaITkVgetxCutSSexVH4qEw')
    keyring.set_password('real_app_secret', 'a_kannie', 'LLhGO6tUDaepjBRFtocxjcYPZbkLfR5mKRFJrPccIkOBVfLsUhkVMFNWy7h7bWAD4CSq3nPowAYX/MMocSI9MAXrbNximason8X8V44iWkrrH/+IJT7E8CAN6fiCQwcnuHLZi/ryI/AzgHLHxwf56cCj/jEMtjrvxf6aITV5WrzSSmYLNOg=')    
    
    app_key = 'real_app_key'
    app_secret = 'real_app_secret'
    ID = 'a_kannie'
    mock = '0' # 실전
    cano = '64099516' # 카니실전
   
    sys1 = systemtrade(app_key, app_secret, ID, mock , cano) 
    df1 = sys1.main()
    print(df1)

    # sys1.rebalancing_trade_at_once()
    # sys1.execute()


    keyring.set_password('mock_app_key', 'v_kannie', 'PSnwe2lboWhKABz4afYQUf5Cnm0x6IlBxt6F')
    keyring.set_password('mock_app_secret', 'v_kannie', 'zFilo09//IcL6SKcVd+VHCxiGuhmVhu+llV1emGjL+J202Y9w1hxyFszqhvzBXjcM34t3QTULxOxM5heeVPCJJQSTSaiZEYMHXyddWCaLVwZiT93dpzgwfnOC0Stc1pmvlxbBAzux5ASV+hZuiYAZ6KTYKxexelADUlR3mIBDbeNfBkNuiw=')
    app_key = 'mock_app_key'
    app_secret = 'mock_app_secret'
    mock = '1' 
    ID = 'v_kannie'  
    cano = '50102070' #카니 모의

    sys2 = systemtrade(app_key, app_secret, ID, mock, cano) 
    df2 = sys2.main()
    print(df2)



    keyring.set_password('mock_app_key', '@2229673', 'PSy3N0hiW3taBNYtIzKpuH2xnZ6jt72KqpQf')
    keyring.set_password('mock_app_secret', '@2229673', '7/xPBWEvxqjEWPZ7R/w5XhA/bXX7ULjmL7da6Amn4/0drE+8HYXf9vAt/GrB93vsOzVp1vxzQ1+95gvpux2GlM9r8O3zs72TabFVezX7usnkA8AKAC+e2YVBXgms5lVxNFRBJ9tXoS9ypS7yjWfm09BB6ZCXtQJkaSmR4gsT21rAJOiZUeA=')

    app_key = 'mock_app_key'
    app_secret = 'mock_app_secret'
    mock = '1' 
    ID = '@2229673' 
    cano = '50102559' #유진 모의
    
    sys3 = systemtrade(app_key, app_secret, ID, mock, cano) 
    df3 = sys3.main()
    print(df3)

    # sys3.rebalancing_trade_at_once()
    # sys3.execute()

    return HttpResponse("Success monthly rebalancing")

def add_daily(request):
    db = cqrDB()
    db.add_daily_weights()  #종목별투자비중추이 업데이트
    db.add_clsweight()  #자산별투자비중추이 업데이트
    db.add_daily_value() #일별수익률추이 업데이트
    db.add_monthly_value() #월별수익률추이 업데이트
    return HttpResponse("Success add_daily_weights")

def add_daily_weights(request): #종목별투자비중추이 업데이트
    db = cqrDB()
    db.add_daily_weights()
    print("Success add_daily_weights")
    return HttpResponse("Success add_daily_weights")

def add_clsweight(request): #자산별투자비중추이 업데이트
    db = cqrDB()
    db.add_clsweight()
    print("Success add_clsweight")
    return HttpResponse("Success add_clsweight")

def add_daily_value(request): #일별수익률추이 업데이트 
    db = cqrDB()    
    db.add_daily_value()
    print("Success add_daily_value")
    return HttpResponse("Success add_daily_value")

def add_monthly_value(request): #월별수익률추이 업데이트
    db = cqrDB()
    db.add_monthly_value()
    print("Success add_monthly_value")
    return HttpResponse("Success add_monthly_value")

##
def update_daily_weights(request): #종목별투자비중추이 업데이트
    db = cqrDB()
    db.update_daily_weights()
    print("success")
    return HttpResponse("Success update_daily_weights")

def update_clsweight(request): #자산별투자비중추이 업데이트
    db = cqrDB()
    db.update_clsweight()
    print("success")
    return HttpResponse("Success update_clsweight")

def update_daily_value(request): #일별수익률추이 업데이트
    print("starting update_daily_value")
    db = cqrDB()    
    db.update_daily_value()
    return HttpResponse("Success update_daily_value")

def update_monthly_value(request): #월별수익률추이 업데이트
    db = cqrDB()
    db.update_monthly_value()
    print("success")
    return HttpResponse("Success update_monthly_value")

class PortfolioLV(ListView):
    model = Portfolio

class PortfolioDV(DetailView):
    model = Portfolio

class MyAssetView(TemplateView):
    template_name = 'portfolio/my_asset.html'

class SurveyView(TemplateView):
    template_name = 'portfolio/survey_view.html'

class MgrOnlyView(UserPassesTestMixin, TemplateView):
    template_name = 'portfolio/mgronly_view.html'
    login_url = '/'

    def test_func(self):
        return self.request.user.is_superuser

def all_port(request):
    port_list = Portfolio.objects.all()

    return render (request,'portfolio/portfolio_list.html', {
        'port_list': port_list})   

def my_asset(request):
    if request.user.is_authenticated:

        me = request.user.id
        profile_item = Profile.objects.filter(user_id=me) ##
        question_item = Questionarie.objects.filter(userid=me)

        keyring.set_password('mock_app_key', '@2229673', 'PSy3N0hiW3taBNYtIzKpuH2xnZ6jt72KqpQf')
        keyring.set_password('mock_app_secret', '@2229673', '7/xPBWEvxqjEWPZ7R/w5XhA/bXX7ULjmL7da6Amn4/0drE+8HYXf9vAt/GrB93vsOzVp1vxzQ1+95gvpux2GlM9r8O3zs72TabFVezX7usnkA8AKAC+e2YVBXgms5lVxNFRBJ9tXoS9ypS7yjWfm09BB6ZCXtQJkaSmR4gsT21rAJOiZUeA=')
        
        key_name = 'mock_app_key'
        secret_name = 'mock_app_secret'
        ID = '@2229673'
        mock = '1' # (1:mock, 0:real)
        cano = '50102559' #계좌번호
        #유진모의


        # keyring.set_password('real_app_key', 'kannie', 'PSnvAltwjE5ZrOaITkVgetxCutSSexVH4qEw')
        # keyring.set_password('real_app_secrect', 'kannie', 'LLhGO6tUDaepjBRFtocxjcYPZbkLfR5mKRFJrPccIkOBVfLsUhkVMFNWy7h7bWAD4CSq3nPowAYX/MMocSI9MAXrbNximason8X8V44iWkrrH/+IJT7E8CAN6fiCQwcnuHLZi/ryI/AzgHLHxwf56cCj/jEMtjrvxf6aITV5WrzSSmYLNOg=')

        # keyring.set_password('mock_app_key', 'kannie', 'PSnwe2lboWhKABz4afYQUf5Cnm0x6IlBxt6F')
        # keyring.set_password('mock_app_secret', 'kannie', 'zFilo09//IcL6SKcVd+VHCxiGuhmVhu+llV1emGjL+J202Y9w1hxyFszqhvzBXjcM34t3QTULxOxM5heeVPCJJQSTSaiZEYMHXyddWCaLVwZiT93dpzgwfnOC0Stc1pmvlxbBAzux5ASV+hZuiYAZ6KTYKxexelADUlR3mIBDbeNfBkNuiw=')

        # app_key = keyring.get_password('mock_app_key', 'kannie')
        # app_secret = keyring.get_password('mock_app_secret','kannie')

        url_base = "https://openapivts.koreainvestment.com:29443" #모의투자
        #url_base = "https://openapivts.koreainvestment.com:9443" #실전투자
        
        headers ={"content-type":"application/json"}
        path = "oauth2/tokenP"
        body = {
            "grant_type": "client_credentials",
            "appkey": key_name,
            "appsecret": secret_name,
        }

        url = f"{url_base}/{path}"

        #access token 발급
        res = requests.post(url, headers=headers, data=json.dumps(body))
        access_token = res.json()['access_token']
                
        path = "/uapi/domestic-stock/v1/trading/inquire-balance"
        url = f"{url_base}/{path}"

        headers = {
            "Content-Type": "application/json",
            "authorization": f"Bearer {access_token}",
            "appKey": key_name,
            "appSecret": secret_name,
            "tr_id": "VTTC8434R"
        }

        params = {
            "CANO": "50102559",  # 계좌번호 앞 8지리
            "ACNT_PRDT_CD": "01",  # 계좌번호 뒤 2자리
            "AFHR_FLPR_YN": "N",  # 시간외단일가여부
            "OFL_YN": "",  # 공란
            "INQR_DVSN": "01",  # 조회구분
            "UNPR_DVSN": "01",  # 단가구분
            "FUND_STTL_ICLD_YN": "N",  # 펀드결제분포함여부
            "FNCG_AMT_AUTO_RDPT_YN": "N",  # 융자금액자동상환여부        
            "PRCS_DVSN": "00",  # 처리구분(00: 전일매매포함)
            "CTX_AREA_FK100": "",  # 연속조회검색조건
            "CTX_AREA_NK100": ""  # 연속조회키
        }
        time.sleep(2)
        res = requests.get(url, headers=headers, params=params) #계좌잔고
        data = res.json()['output2']

        print(data)
        #ap=pd.DataFrame.from_records(res.json()['output2'])
        #ap

        print('시작 시간 :', datetime.now().strftime('%m/%d %H:%M:%S'))


        return render(request, 'portfolio/my_asset.html', {
            "profile_item":profile_item, 
            "question_item":question_item,
            "data":data,
          #  "balance": balance,
            })
    else:
        return render(request, 'portfolio/mgronly_view.html', {})

def mgr_only(request): #종목별 weight 조회
    if request.user.is_authenticated and request.user.is_superuser :

        querydict=request.GET.copy()

        if querydict.get('fromdate') is None:
            today = date.today()
            try:
                fromdate = date(today.year - 10, today.month, today.day)
            except ValueError: 
                fromdate = date(today.year - 10, today.month, 28)

            fromdate = fromdate.strftime("%Y-%m-%d")
            todate = date.today().strftime("%Y-%m-%d")    

        else:
            fromdate= request.GET.get('fromdate')
            todate = request.GET.get('todate' )
            
            if fromdate is None or fromdate.strip() == "" or todate is None or todate.strip() == "":
                today = date.today()
                try:
                    fromdate = date(today.year - 10, today.month, today.day)
                except ValueError: 
                    fromdate = date(today.year - 10, today.month, 28)
                fromdate = fromdate.strftime("%Y-%m-%d")
                todate = date.today().strftime("%Y-%m-%d")    

        date_from = fromdate
        date_to = todate          
        daily_mp_w = dailyMPweight.objects.filter(date__gte=date_from, date__lte=date_to).order_by('-date')

        p = Paginator(daily_mp_w, 20)
        page = request.GET.get('page')
        mp_w = p.get_page(page)
        
        return render (request,'portfolio/mgronly_view.html', {
                'mp_w': mp_w,
                "querydict":querydict,
                "fromdate":fromdate,
                "todate":todate,
                "date_from":date_from,
                "date_to":date_to,
                })   
    else:
        return render (request,'portfolio/mgronly_view.html', {  })   

def mgr_only3(request): #자산별투자비중조회
    if request.user.is_authenticated and request.user.is_superuser:
        querydict=request.GET.copy()

        if querydict.get('fromdate') is None:
            today = date.today()
            try:
                fromdate = date(today.year - 10, today.month, today.day)
            except ValueError: 
                fromdate = date(today.year - 10, today.month, 28)

            fromdate = fromdate.strftime("%Y-%m-%d")
            todate = date.today().strftime("%Y-%m-%d")    

        else:
            fromdate= request.GET.get('fromdate')
            todate = request.GET.get('todate' )
            
            if fromdate is None or fromdate.strip() == "" or todate is None or todate.strip() == "":
                today = date.today()
                try:
                    fromdate = date(today.year - 10, today.month, today.day)
                except ValueError: 
                    fromdate = date(today.year - 10, today.month, 28)
                fromdate = fromdate.strftime("%Y-%m-%d")
                todate = date.today().strftime("%Y-%m-%d")    
        
        date_from = fromdate
        date_to = todate
        daily_mp_w = MPclsweight.objects.filter(date__gte=date_from, date__lte=date_to).order_by('-date')

        p = Paginator(daily_mp_w, 20)
        page = request.GET.get('page')
        mp_w = p.get_page(page)
        
        return render (request,'portfolio/mgronly3_view.html', {
                'mp_w': mp_w,
                "querydict":querydict,
                "fromdate":fromdate,
                "todate":todate,
                "date_from":date_from,
                "date_to":date_to,
                })   
    else:
        return render(request, 'portfolio/mgronly3_view.html', {})   
    
def mgr_only1(request): #일별수익률조회
    if request.user.is_authenticated and request.user.is_superuser:
        querydict=request.GET.copy()

        if querydict.get('fromdate') is None:
            today = date.today()
            try:
                fromdate = date(today.year - 10, today.month, today.day)
            except ValueError: 
                fromdate = date(today.year - 10, today.month, 28)

            fromdate = fromdate.strftime("%Y-%m-%d")
            todate = date.today().strftime("%Y-%m-%d")    

        else:
            fromdate= request.GET.get('fromdate')
            todate = request.GET.get('todate' )
            
            if fromdate is None or fromdate.strip() == "" or todate is None or todate.strip() == "":
                today = date.today()
                try:
                    fromdate = date(today.year - 10, today.month, today.day)
                except ValueError: 
                    fromdate = date(today.year - 10, today.month, 28)
                fromdate = fromdate.strftime("%Y-%m-%d")
                todate = date.today().strftime("%Y-%m-%d")    
        
        date_from = fromdate
        date_to = todate
        daily_mp_w = dailyMPvalue.objects.filter(date__gte=date_from, date__lte=date_to).order_by('-date')

        p = Paginator(daily_mp_w, 20)
        page = request.GET.get('page')
        mp_v = p.get_page(page)
        
        return render (request,'portfolio/mgronly1_view.html', {
                'mp_v': mp_v,
                "querydict":querydict,
                "fromdate":fromdate,
                "todate":todate,
                "date_from":date_from,
                "date_to":date_to,
                })   
    else:
        return render(request, 'portfolio/mgronly1_view.html', {})   

def mgr_only2(request): #월별수익률조회
    if request.user.is_authenticated and request.user.is_superuser:
        querydict=request.GET.copy()

        if querydict.get('fromdate') is None:
            today = date.today()
            try:
                fromdate = date(today.year - 10, today.month, today.day)
            except ValueError: 
                fromdate = date(today.year - 10, today.month, 28)

            fromdate = fromdate.strftime("%Y-%m-%d")
            todate = date.today().strftime("%Y-%m-%d")    

        else:
            fromdate= request.GET.get('fromdate')
            todate = request.GET.get('todate' )
            
            if fromdate is None or fromdate.strip() == "" or todate is None or todate.strip() == "":
                today = date.today()
                try:
                    fromdate = date(today.year - 10, today.month, today.day)
                except ValueError: 
                    fromdate = date(today.year - 10, today.month, 28)
                fromdate = fromdate.strftime("%Y-%m-%d")
                todate = date.today().strftime("%Y-%m-%d")    
        
        date_from = fromdate
        date_to = todate
        daily_mp_w = monthlyMPvalue.objects.filter(date__gte=date_from, date__lte=date_to).order_by('-date')

        p = Paginator(daily_mp_w, 20)
        page = request.GET.get('page')
        mp_v = p.get_page(page)
        
        return render (request,'portfolio/mgronly2_view.html', {
                'mp_v': mp_v,
                "querydict":querydict,
                "fromdate":fromdate,
                "todate":todate,
                "date_from":date_from,
                "date_to":date_to,
                })   
    else:
        return render(request, 'portfolio/mgronly2_view.html', {})      

def add_survey(request, pk):
    submitted = False
    quest = Questionarie.objects.get(id=pk)
    
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save() #save to db
            submitted=True
            #return HttpResponseRedirect('myasset/add_survey?submitted=True')
    else:
        form=QuestionForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'portfolio/add_survey.html', {'form':form, 'submitted':submitted})

def customer_survey(request, pk):

	survey_record  = Questionarie.objects.get(id=pk)

	return render(request, 'portfolio/view_survey.html', {
			"survey_record":survey_record,
			})

def update_survey(request, pk):
    cur_survey = Questionarie.objects.get(id=pk)
    form = QuestionForm(request.POST or None, instance=cur_survey)

    if form.is_valid():     
        a=cal_risk(form)
        instance = form.save(commit=False)
        instance.riskscore = a
        instance.save()
        #form.cleaned_data['riskscore'] = a
        #instance.save
        #form.save()
        print("success")
    else:
        print("not success")

    return render(request, 'portfolio/update_survey.html', {
        'form':form,
        'survey':cur_survey,
        })

def cal_risk(request):  
    QA1_scores = {'1': 12.5,'2': 12.5,'3': 9.3,'4': 6.2, '5': 3.1,}
    QA2_scores = {'1': 3.1, '2': 6.2, '3': 9.3,'4': 12.5,'5': 15.6,}
    QA3_scores = {'1': 3.1, '2': 6.2, '3': 9.3,'4': 12.5,'5': 15.6,}
    QA4_scores = {'1': 3.1, '2': 6.2, '3': 9.3,'4': 12.5,}
    QA5_scores = {'1': 15.6,'2': 12.5,'3': 9.3,'4': 6.2, '5': 3.1,}
    QA6_scores = {'1': 9.3, '2': 6.2, '3': 3.1,}
    QA7_scores = {'1': -6.2,'2': 6.2, '3': 12.5,'4': 18.7,}
    
    score_mappings = {'QA1': QA1_scores,'QA2': QA2_scores,'QA3': QA3_scores,'QA4': QA4_scores,'QA5': QA5_scores,'QA6': QA6_scores,'QA7': QA7_scores,}
    questions_and_scores = [
                ('QA1', QA1_scores),
                ('QA2', QA2_scores),
                ('QA3', QA3_scores),
                ('QA4', QA4_scores),
                ('QA5', QA5_scores),
                ('QA6', QA6_scores),
                ('QA7', QA7_scores),
            ]
    
    total_score = 0
    for field, scores in questions_and_scores:
            input_option = request.cleaned_data.get(field)
            score = scores.get(input_option, 0) 
            total_score += score
    
    return total_score

    #1, 안정형, 0-20
    #2, 안정추구형, 21-40
    #3, 중립형, 41-60
    #4, 적극형, 61-80
    #5, 공격형, 81-90
    
def calculate_sum(request):
    calc = Calculator()  # Create an instance of the Calculator class  
    sum_result = calc.sum(10,5)
    
    response_content = (f"Sum: {sum_result}<br>")
    return HttpResponse(response_content)

def calculate_minus(request):
    calc = Calculator()  # Create an instance of the Calculator class
    minus_result = calc.minus(10,5)

    response_content = (f"Minus: {minus_result}<br>")
    return HttpResponse(response_content)

