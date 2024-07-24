from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator

from cqra2.services.biz_logic import run_cqra2_mp, run_cqra2_rpt, run_cqra2_range_rpt
from cqra2.services.db_updater import cqra2_TBL 
from .models import dailyMPweight, dailyMPvalue, monthlyMPvalue, MPclsweight

import requests
from datetime import datetime, timedelta, date
from django.utils import timezone

def port_list(request):   #시큐라2 성능
    default_todate = timezone.now().date()
    default_fromdate = default_todate - timedelta(days=365)

    return render (request,'cqra2/portfolio_list.html', {
        'default_fromdate': default_fromdate.strftime('%Y-%m-%d'),
        'default_todate': default_todate.strftime('%Y-%m-%d'),
    })   

def type_view(request, ty): # 전체리포트 보기
    return render(request, rf'cqra2/cqra2_ty{ty}.html')

def type_view_range (request, ty): # 범위 리포트 보기
    db = cqra2_TBL(type = ty)   
    r_fromdate = request.GET.get('r_fromdate')
    r_todate = request.GET.get('r_todate')

    stock = db.search_daily_value(r_fromdate, r_todate)     #db data search
    run_cqra2_range_rpt(ty, stock) 

    return render(request, rf'cqra2/cqra2_range_ty{ty}.html')

def acct_list (request):  #계좌관리
    return render(request, 'cqra2/account_list.html', {
    })

def mgr_asset_wgt(request, ty): #종목별 투자비중 조회
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
        
        return render (request,'cqra2/mgr_asset_wgt.html', {
                'mp_w': mp_w,
                "querydict":querydict,
                "fromdate":fromdate,
                "todate":todate,
                "date_from":date_from,
                "date_to":date_to,
                "type":ty,
                })   
    else:
        return render (request,'cqra2/mgr_asset_wgt.html', {  })   

def mgr_class_wgt(request, ty): #자산별 투자비중 조회
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
        
        return render (request,'cqra2/mgr_class_wgt.html', {
                'mp_w': mp_w,
                "querydict":querydict,
                "fromdate":fromdate,
                "todate":todate,
                "date_from":date_from,
                "date_to":date_to,
                "type":ty,
                })   
    else:
        return render(request, 'cqra2/mgr_class_wgt.html', {})   

def mgr_daily_ret(request, ty): #일별 수익률 조회
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
        
        return render (request,'cqra2/mgr_daily_ret.html', {
                'mp_v': mp_v,
                "querydict":querydict,
                "fromdate":fromdate,
                "todate":todate,
                "date_from":date_from,
                "date_to":date_to,
                "type": ty,
                })   
    else:
        return render(request, 'cqra2/mgr_daily_ret.html', {})   

def mgr_monthly_ret(request, ty): #월별 수익률 조회
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
        
        return render (request,'cqra2/mgr_monthly_ret.html', {
                'mp_v': mp_v,
                "querydict":querydict,
                "fromdate":fromdate,
                "todate":todate,
                "date_from":date_from,
                "date_to":date_to,
                "type": ty,
                })   
    else:
        return render(request, 'cqra2/mgr_monthly_ret.html', {})   

def run_algo(request, ty):      
    data = run_cqra2_mp (ty) # 모델 CVS 파일생성
    run_cqra2_rpt (ty, data) # quantstat 리포트생성
    return render(request, rf'cqra2/cqra2_ty{ty}.html')

def init_mpdb (request, ty):   # 모델링 DB 초기화
    db = cqra2_TBL(type=ty)
    db.update_daily_weights()     #종목별투자비중추이 업데이트
    db.update_clsweight()         #자산별투자비중추이 업데이트
    db.update_daily_value ()      #일별수익률추이 업데이트
    db.update_monthly_value ()    #월별수익률추이 업데이트
    return HttpResponse("Success init DB")

def daily_update_mpdb (request, ty):     # 모델링 DB 일일 저장
    db = cqra2_TBL(type = ty)    
    db.add_daily_weights()     #종목별투자비중추이 업데이트
    db.add_clsweight()         #자산별투자비중추이 업데이트
    db.add_daily_value ()      #일별수익률추이 업데이트
    db.add_monthly_value ()    #월별수익률추이 업데이트
    return HttpResponse("Success daily_update DB")

