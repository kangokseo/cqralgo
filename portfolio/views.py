from django.shortcuts import get_object_or_404, render

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
#import matplotlib.pyplot as plt
import quantstats as qs
import yfinance as yf
import shutil
import os


from portfolio.utilis.MP_gen import StockData       #cvs 모델링
from portfolio.utilis.dbUpdater import cqrDB 
from portfolio.utilis.dbUpdater import accountDB        #db 클래스
from portfolio.utilis.KIS_api import systemtrade    #한투 트랜잭션

from cqrsite.views import HomeView
from .forms import QuestionForm
from .models import ModelPort, Portfolio, Profile, Questionarie, dailyMPweight, dailyMPvalue, monthlyMPvalue, MPclsweight, Account

import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg' to avoid GUI requirements


#os.environ['MPLBACKEND'] = 'Agg'

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

def account_list (request):  
    user_id = request.user.id
    adb = accountDB()
    account_v = adb.get_account_list()
    if account_v is None:
        return HttpResponse("Error fetching accounts", status=500)
    return render(request, 'portfolio/account_list.html', {
        "user_id": user_id,
        "account_v": account_v,
    })

def all_port(request):
    port_list = Portfolio.objects.all()
    
    return render (request,'portfolio/portfolio_list.html', {
        'port_list': port_list})   

def my_asset(request):
    if request.user.is_authenticated:

        try:
            me = request.user.id
            profile_item = Profile.objects.filter(user_id=me) 
            question_item = Questionarie.objects.filter(userid=me)

            account_v = Account.objects.filter(
                user_id = request.user,
            )
        except Exception as e:
            print("프로파일과 투자성향 가져오기 실패")

        for account in account_v:
            if account.계좌명 == "실전":
                mock='0'
            else:           
                mock='1'
            id = account.user_id
            cano = account.cano

            # try:
            #     keyring.set_password('app_key', id, account.app_key)
            #     keyring.set_password('app_secret', id, account.app_secret)    
            # except Exception as e:
            #     print("패스워드 가져오기 실패")

            # try:    
            #     sys = systemtrade(app_key = 'app_key', app_secret = 'app_secret', ID = id, cano = cano,  mock = mock, custtype = 'P') 
            #     ap, balance = sys.check_account() 
            # except Exception as e:
            #     print("클래스 초기화 실패")

            app_key=account.app_key
            app_secret=account.app_secret
            print(app_key)
            print(app_secret)

            try:    
                sys = systemtrade(app_key = app_key, app_secret = app_secret, ID = id, cano = cano,  mock = mock, custtype = 'P') 
                ap, balance = sys.check_account() 
            except Exception as e:
                print("클래스 초기화 실패")


            print(balance)
            # print(balance['tot_evlu_amt'])
            #print('시작 시간 :', datetime.now().strftime('%m/%d %H:%M:%S'))

        return render(request, 'portfolio/my_asset.html', {
            "profile_item":profile_item, 
            "question_item":question_item,
            "account_v":account_v ,
            "balance": balance,
            })
    else:
        return render(request, 'portfolio/mgronly_view.html', {})

def mgr_only(request, ty): #종목별 투자비중 조회
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

        daily_mp_w = dailyMPweight.objects.filter(
                    date__gte=date_from,
                    date__lte=date_to,
                    port_id=str(ty) #ty
                ).order_by('-date')

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
                "type":ty,
                })   
    else:
        return render (request,'portfolio/mgronly_view.html', {  })   

def mgr_only3(request, ty): #자산별 투자비중 조회
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
        
        daily_mp_w = MPclsweight.objects.filter(
            date__gte=date_from, date__lte=date_to, 
            port_id= str(ty), #ty
            ).order_by('-date')
        
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
                "type":ty,
                })   
    else:
        return render(request, 'portfolio/mgronly3_view.html', {})   
    
def mgr_only1(request, ty): #일별 수익률 조회
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
        daily_mp_w = dailyMPvalue.objects.filter(
            date__gte=date_from, date__lte=date_to, 
            port_id= str(ty), #ty
            ).order_by('-date')

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
                "type": ty,
                })   
    else:
        return render(request, 'portfolio/mgronly1_view.html', {})   

def mgr_only2(request, ty): #월별 수익률조회
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
        daily_mp_w = monthlyMPvalue.objects.filter(
            date__gte=date_from, date__lte=date_to, 
            port_id= str(ty), #ty
            ).order_by('-date')

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
                "type": ty,
                })   
    else:
        return render(request, 'portfolio/mgronly2_view.html', {})      

def add_survey(request, pk):

    submitted = False
    form = QuestionForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            a=cal_risk(form)
            instance = form.save(commit=False)
            instance.riskscore = a
            instance.user_name = pk
            instance.save()

            cur_survey = Questionarie.objects.get(user_name=pk)
            # return render(request, 'portfolio/add_survey.html', 
            #     {'form':form, 
            #     'submitted':submitted,
            #     'survey':cur_survey,
            #     })
            return render(request, 'portfolio/view_survey.html', {
                "survey_record": cur_survey,
            })
    else:
        return render(request, 'portfolio/add_survey.html', 
        {'form':form, 
        })

def view_survey(request, pk): #성향분석설문 결과

    try:
        survey_record = Questionarie.objects.get(user_name=pk)

        return render(request, 'portfolio/view_survey.html', {
            "survey_record": survey_record,
        })

    except Questionarie.DoesNotExist:
        
        return add_survey(request, pk)
        #return HttpResponse("설문데이터 없슴")

        # form = QuestionForm(request.POST)
        # submitted=False

        # return render(request, 'portfolio/add_survey.html', {
        #     'form':form, 
        #     'pk':pk,
        #     #'submitted':submitted
        #     })

def update_survey(request, pk): #성향분석설문 제출화면
    cur_survey = Questionarie.objects.get(user_name=pk)
    form = QuestionForm(request.POST or None, instance=cur_survey)

    if form.is_valid():     
        a=cal_risk(form)
        instance = form.save(commit=False)
        instance.riskscore = a
        instance.save()
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

def algo(request, ty):      # 모델링 CVS 파일생성: 일별수익률, 월별수익률, 자산별투자비중, 종목별투자비중
    tic = [ "114260.KS",    # Bond, cash, mmf, kosdq, KOSPI, NASDAQ, S&P
           "153130.KS", "157450.KS","229200.KS", "278530.KS", "379810.KS", "379800.KS"] 

    fromdate = "2021-04-05"
    todate = date.today().strftime("%Y-%m-%d")

    stock_data = StockData(tic) 
    data = stock_data.download_data(fromdate, todate,'1d') 
    data.Close.dropna(thresh = 6)
    df,ret = stock_data.clean()

    values = {
        5: (1, 0, 1, 0, 1, 0),                  #공격형
        4: (0.7, 0.3, 0.7, 0.3, 0.7, 0.3),      #적극형
        3: (0.5, 0.5, 0.5, 0.5, 0.5, 0.5),      #중립형
        2: (0.3, 0.7, 0.3, 0.7, 0.3, 0.7),      #안정형
    }

    # Retrieve values based on ty
    odd_stock_w, odd_bond_w, even_stock_w, even_bond_w, even_passive_stock_w, even_passive_bond_w = values.get(ty, (None, None, None, None, None, None))

    #Bond, cash, mmf, kosdq, KOSPI, NASDAQ, S&P
    #홀수11-4월 (코스닥60, 코스피40). 홀수 5-10월(나스닥50,S&P50)
    #짝수11-4월 (코스닥50, 코스피50). 짝수 5-10월(나스닥50,S&P50)
    odd_buy = np.array([(1/3*odd_bond_w), (1/3*odd_bond_w), (1/3*odd_bond_w), 0.6*odd_stock_w, 0.4*odd_stock_w, 0.0*odd_stock_w, 0.0*odd_stock_w])          # Even 11 - Odd 4. Active
    odd_hold = np.array([(1/3*odd_bond_w), (1/3*odd_bond_w), (1/3*odd_bond_w), 0.0*odd_stock_w, 0.0*odd_stock_w, 0.5*odd_stock_w, 0.5*odd_stock_w])         # Odd 5 - Odd 10. 
    even_buy = np.array([(1/3*even_bond_w), (1/3*even_bond_w), (1/3*even_bond_w), 0.5*even_stock_w, 0.5*even_stock_w, 0.0*even_stock_w, 0.0*even_stock_w])  # Odd 11 - Even 4. NOTE: Here, we shift Kospi weight to Nasdaq instead of S&P 500 to be consistent with our logic that 11-4 should be more aggressive than 5-10. 
    even_hold = np.array([(1/3*even_passive_bond_w), (1/3*even_passive_bond_w), (1/3*even_passive_bond_w), 0.0*even_passive_stock_w, 0.0*even_passive_stock_w, 0.5*even_passive_stock_w, 0.5*even_passive_stock_w])  # Even 5 - Even 10

    halloween_adj = stock_data.algo1(1000,odd_buy,odd_hold,even_buy,even_hold) 
    
    stock_data.results()[0]
    stock_data.results()[1]
 
    now = datetime.now()
    formatted_now = now.strftime("%Y%m%d")  

    # 1. 일별수익률추이
    source_file_path = rf'portfolio/templates/{ty}_일별수익률추이{formatted_now}.csv'
    destination_file_path = rf'portfolio/templates/{ty}_일별수익률추이.csv'
    daily_ret = stock_data.daily_ret() 
    daily_ret.to_csv(destination_file_path)
    #shutil.copy(source_file_path, destination_file_path)

    # 2. 월별수익률추이
    source_file_path = rf'portfolio/templates/{ty}_월별수익률추이{formatted_now}.csv'
    destination_file_path = rf'portfolio/templates/{ty}_월별수익률추이.csv'
    monthly_ret = stock_data.monthly_ret() 
    monthly_ret.to_csv(destination_file_path)
    #shutil.copy(source_file_path, destination_file_path)
    
    # 3. 자산별투자비중추이
    source_file_path = rf'portfolio/templates/{ty}_자산별투자비중추이{formatted_now}.csv'
    destination_file_path = rf'portfolio/templates/{ty}_자산별투자비중추이.csv'   
    port_weights = stock_data.portfolio_by_asset_class() 
    port_weights = port_weights[1]
    port_weights.to_csv(destination_file_path)
    #shutil.copy(source_file_path, destination_file_path)
    
    # 4. 종목별투자비중추이
    source_file_path = rf'portfolio/templates/{ty}_종목별투자비중추이{formatted_now}.csv'
    destination_file_path = rf'portfolio/templates/{ty}_종목별투자비중추이.csv'  
    cls_weight=stock_data.portfolio_by_ind_assets() 
    cls_weight.to_csv(destination_file_path)
    #shutil.copy(source_file_path, destination_file_path)
   
    # 5. 리밸런싱발생내역
    source_file_path = rf'portfolio/templates/{ty}_리밸런싱발생내역{formatted_now}.csv'
    # destination_file_path = r'portfolio/templates/{ty}_리밸런싱발생내역.csv'     
    # rebal_history = stock_data.rebalance_history()  
    # rebal_history.to_csv(destination_file_path)
    #shutil.copy(source_file_path, destination_file_path)

    # extend pandas functionality with metrics, etc.
    qs.extend_pandas()
    daily_ret.iloc[:,1]
    
    html_file_path = rf'portfolio/templates/portfolio/chesleyalgo_ty{ty}.html'

    qs.reports.html(daily_ret['일별수익률']     
                , benchmark="^GSPC", output=html_file_path, title=rf'chesleyalgo_ty{ty}')
    #webbrowser.open(html_file_path)

    #return HttpResponse("success")
    return render(request, rf'portfolio/chesleyalgo_ty{ty}.html')

def algo_View(request, ty): # 모델결과보기
    return render(request, rf'portfolio/chesleyalgo_ty{ty}.html')

def add_daily(request, ty):     # 모델링 DB 일일 저장
    db = cqrDB(type = ty)
                      
    print("success constructor - {db.type}")

    db.add_daily_weights()     #종목별투자비중추이 업데이트
    print("Success add_daily_weights")

    db.add_clsweight()         #자산별투자비중추이 업데이트
    print("Success add_clsweight")

    db.add_daily_value ()      #일별수익률추이 업데이트
    print("Success add_daily_value")

    db.add_monthly_value ()    #월별수익률추이 업데이트
    print("Success add_monthly_value")

    return HttpResponse("Success add_daily_weights")

def init_add_daily (request, ty):   # 모델링 DB 초기화
    db = cqrDB(type=ty)
    print("success constructor - {db.type}")

    db.update_daily_weights()     #종목별투자비중추이 업데이트
    print("Success init_종목별투자비중")

    db.update_clsweight()         #자산별투자비중추이 업데이트
    print("Success init_자산별투자비중")

    db.update_daily_value ()      #일별수익률추이 업데이트
    print("Success init_일별수익률")

    db.update_monthly_value ()    #월별수익률추이 업데이트
    print("Success init_월별수익률")

    return HttpResponse("Success add_daily_weights")

def rebalancing_00(request, id):       # 지정가 리밸런싱

    account_v = Account.objects.filter(
        id = id,
        )
    account = account_v.first()

    if account.계좌명 == "실전":
        mock='0'
    else:           
        mock='1'
    user_id = account.user_id
    cano = account.cano
    port_id = account.portfolio_id

    port_v = Portfolio.objects.filter(
        portfolio_id = port_id,
        )
    port = port_v.first()

    app_key=account.app_key
    app_secret=account.app_secret
    # keyring.set_password('app_key', user_id, account.app_key)
    # keyring.set_password('app_secret', user_id, account.app_secret)    
    sys = systemtrade(app_key = app_key, app_secret = app_secret, ID = user_id, cano = cano,  mock = mock, custtype = 'P', port_subtype=port.sub_type) 

    sys.schedule_rebalancing_00()
    sys.execute()

    return HttpResponse("Success monthly rebalancing 00")

def rebalancing_06(request, id):       # 장후시간외 리밸런싱

    account_v = Account.objects.filter(
        id = id,
        )
    account = account_v.first()

    if account.계좌명 == "실전":
        mock='0'
    else:           
        mock='1'
    user_id = account.user_id
    cano = account.cano
    port_id = account.portfolio_id

    port_v = Portfolio.objects.filter(
        portfolio_id = port_id,
        )
    port = port_v.first()

    app_key=account.app_key
    app_secret=account.app_secret
    # keyring.set_password('app_key', user_id, account.app_key)
    # keyring.set_password('app_secret', user_id, account.app_secret)   
  
    sys = systemtrade(app_key = app_key, app_secret = app_secret, ID = user_id, cano = cano,  mock = mock, custtype = 'P', port_subtype=port.sub_type) 

    sys.schedule_rebalancing_06()
    sys.execute()

    return HttpResponse("Success monthly rebalancing 06")

def account_item(request, id):  

    try:
        account_v = Account.objects.filter(
            id = id,
            )
        account = account_v.first()
        print("Account 가져오기 성공")
    except Exception as e:
        print("Account 가져오기 실패")


    if account.계좌명 == "실전":
        mock='0'
    else:           
        mock='1'

    try:
        id = account.user_id
        cano = account.cano

        app_key=account.app_key
        app_secret=account.app_secret
        # keyring.set_password('app_key', id, account.app_key)
        # keyring.set_password('app_secret', id, account.app_secret)    
        print("패스워드 저장 성공")
    except Exception as e:
        print("패스워드 저장 실패")

    #(증권사) 계좌 평가손 가져오기  
    try:
        sys = systemtrade(app_key = app_key, app_secret = app_secret, ID = id, cano = cano,  mock = mock, custtype = 'P') 
        ap, balance = sys.check_account() 
        
        print(balance['tot_evlu_amt'])
        print("평가손 가져오기 성공")
    except Exception as e:
        print("평가손 가져오기 실패")



    #사용자, 투자자리스크 성향 가져오기
    try:
        me = account.user_id
        profile_item = Profile.objects.filter(user_name=me) 
        question_item = Questionarie.objects.filter(user_name=me)

        return render(request, 'portfolio/account_item.html', {
            "profile_item":profile_item, 
            "question_item":question_item,
            "account":account ,
            "balance": balance,
            })
    except Exception as e:
         print("투자자성향 가져오기 실패")



