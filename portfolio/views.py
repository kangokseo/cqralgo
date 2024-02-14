from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy

from cqrsite.views import HomeView
from .forms import QuestionForm
from .models import ModelPort, Portfolio, Profile, Questionarie, dailyMPweight, dailyMPvalue, monthlyMPvalue, MPclsweight
from django.shortcuts import redirect
from django.contrib import messages
from django.core.paginator import Paginator

from django.http import HttpResponse
from portfolio.utilis.calculator import Calculator
from cqrsite.utils.pdUpdater import cqrDB
from datetime import datetime
from datetime import date
from django.utils import timezone

def update_daily_weights(request):
    db = cqrDB()
    db.update_daily_weights()
    print("success")
    return HttpResponse("Success")
    

def update_clsweight(request):
    db = cqrDB()
    db.update_clsweight()
    print("success")
    return HttpResponse("Success")

def update_daily_value(request):
    db = cqrDB()
    db.update_daily_value()
    print("success")
    return HttpResponse("Success")


def update_monthly_value(request):
    db = cqrDB()
    db.update_monthly_value()
    print("success")
    return HttpResponse("Success")



def calculate_sum(request):
    calc = Calculator()  # Create an instance of the Calculator class
    
    # Use the methods of the Calculator instance
    sum_result = calc.sum(10,5)
    
    # Prepare a response string
    response_content = (
        f"Sum: {sum_result}<br>"
    )
    
    return HttpResponse(response_content)

def calculate_minus(request):
    calc = Calculator()  # Create an instance of the Calculator class
    
    # Use the methods of the Calculator instance
    minus_result = calc.minus(10,5)
    
    # Prepare a response string
    response_content = (
        f"Minus: {minus_result}<br>"
    )
    
    return HttpResponse(response_content)

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
    return render (request,'portfolio/portfolio_list.html', {'port_list': port_list})   

def my_asset(request):
    if request.user.is_authenticated:
        me = request.user.id
        profile_item = Profile.objects.filter(user_id=me) ##
        question_item = Questionarie.objects.filter(userid=me)

        print(profile_item)
        print(question_item)
        return render(request, 'portfolio/my_asset.html', {"profile_item":profile_item, "question_item":question_item})

    else:
        return render(request, 'portfolio/mgronly_view.html', {})




def mgr_only(request): #종목별 weight
    if request.user.is_authenticated and request.user.is_superuser :

        querydict=request.GET.copy()

        if querydict.get('fromdate') is None:
            today = date.today()
            fromdate = date(today.year - 2, today.month, today.day)
            fromdate = fromdate.strftime("%Y-%m-%d")
            todate = date.today().strftime("%Y-%m-%d")

        else:
            fromdate= request.GET.get('fromdate')
            todate = request.GET.get('todate' )
        
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

def mgr_only3(request): #자산별 weight
    if request.user.is_authenticated and request.user.is_superuser:
        querydict=request.GET.copy()

        if querydict.get('fromdate') is None:
            today = date.today()
            fromdate = date(today.year - 2, today.month, today.day)
            fromdate = fromdate.strftime("%Y-%m-%d")
            todate = date.today().strftime("%Y-%m-%d")

        else:
            fromdate= request.GET.get('fromdate')
            todate = request.GET.get('todate' )
        
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
    
def mgr_only1(request): #daily MP value
    if request.user.is_authenticated and request.user.is_superuser:
        querydict=request.GET.copy()

        if querydict.get('fromdate') is None:
            today = date.today()
            fromdate = date(today.year - 2, today.month, today.day)
            fromdate = fromdate.strftime("%Y-%m-%d")
            todate = date.today().strftime("%Y-%m-%d")

        else:
            fromdate= request.GET.get('fromdate')
            todate = request.GET.get('todate' )
        
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

def mgr_only2(request): #monthly mp value 
    if request.user.is_authenticated and request.user.is_superuser:
        querydict=request.GET.copy()

        if querydict.get('fromdate') is None:
            today = date.today()
            fromdate = date(today.year - 2, today.month, today.day)
            fromdate = fromdate.strftime("%Y-%m-%d")
            todate = date.today().strftime("%Y-%m-%d")

        else:
            fromdate= request.GET.get('fromdate')
            todate = request.GET.get('todate' )
        
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

        #instance = form.save(commit=False)
        #instance.riskscore=a

        a=cal_risk(form)
        instance = form.save(commit=False)
        instance.riskscore = a
        instance.save()
        #form.cleaned_data['riskscore'] = a
        #instance.save
        #form.save()
        print (a)
        print("success")


    else:
        print("not success")

    return render(request, 'portfolio/update_survey.html', {
        'form':form,
        'survey':cur_survey,
        })


    
##

    
    

def cal_risk(request):  

    QA1_scores = {'1': 12.5,'2': 12.5,'3': 9.3,'4': 6.2, '5': 3.1,}
    QA2_scores = {'1': 3.1, '2': 6.2, '3': 9.3,'4': 12.5,'5': 15.6,}
    QA3_scores = {'1': 3.1, '2': 6.2, '3': 9.3,'4': 12.5,'5': 15.6,}
    QA4_scores = {'1': 3.1, '2': 6.2, '3': 9.3,'4': 12.5,}
    QA5_scores = {'1': 15.6,'2': 12.5,'3': 9.3,'4': 6.2, '5': 3.1,}
    QA6_scores = {'1': 9.3, '2': 6.2, '3': 3.1,}
    QA7_scores = {'1': -6.2,'2': 6.2, '3': 12.5,'4': 18.7,}

    score_mappings = {'QA1': QA1_scores,'QA2': QA2_scores,'QA3': QA3_scores,'QA4': QA4_scores,'QA5': QA5_scores,'QA6': QA6_scores,'QA7': QA7_scores,}
    
    total_score = 0
    questions_and_scores = [
                ('QA1', QA1_scores),
                ('QA2', QA2_scores),
                ('QA3', QA3_scores),
                ('QA4', QA4_scores),
                ('QA5', QA5_scores),
                ('QA6', QA6_scores),
                ('QA7', QA7_scores),
            ]

    for field, scores in questions_and_scores:
            input_option = request.cleaned_data.get(field)
            score = scores.get(input_option, 0) 
            total_score += score
            
    else:
        return total_score
    
    return total_score