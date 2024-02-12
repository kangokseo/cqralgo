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
    if request.user.is_authenticated and request.user.is_superuser:
        daily_mp_w = dailyMPweight.objects.all().order_by('-date')

        p = Paginator(daily_mp_w, 20)
        page = request.GET.get('page')
        mp_w = p.get_page(page)

        #return render (request,'portfolio/mgronly_view.html', {'daily_mp_w': daily_mp_w, 'mp_w': mp_w})   
        return render (request,'portfolio/mgronly_view.html', {'mp_w': mp_w})   

    else:
        return render(request, 'portfolio/mgronly_view.html', {})   

def mgr_only3(request): #자산별 weight
    if request.user.is_authenticated and request.user.is_superuser:
        daily_mp_w = MPclsweight.objects.all().order_by('-date')

        p = Paginator(daily_mp_w, 20)
        page = request.GET.get('page')
        mp_w = p.get_page(page)

        #return render (request,'portfolio/mgronly_view.html', {'daily_mp_w': daily_mp_w, 'mp_w': mp_w})   
        return render (request,'portfolio/mgronly3_view.html', {'mp_w': mp_w})   

    else:
        return render(request, 'portfolio/mgronly3_view.html', {})   
    
def mgr_only1(request): #daily MP value
    if request.user.is_authenticated and request.user.is_superuser:
        daily_mp_v = dailyMPvalue.objects.all().order_by('-date')

        p = Paginator(daily_mp_v, 20)
        page = request.GET.get('page')
        mp_v = p.get_page(page)
 
        return render (request,'portfolio/mgronly1_view.html', {'mp_v': mp_v})   

    else:
        return render(request, 'portfolio/mgronly1_view.html', {})   

def mgr_only2(request): #monthly mp value 
    if request.user.is_authenticated and request.user.is_superuser:
        monthl_mp = monthlyMPvalue.objects.all().order_by('-date')

        p = Paginator(monthl_mp, 20)
        page = request.GET.get('page')
        mp_v = p.get_page(page)
 
        return render (request,'portfolio/mgronly2_view.html', {'mp_v': mp_v})   

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
			"survey_record":survey_record
			})


def update_survey(request, pk):
    cur_survey = Questionarie.objects.get(id=pk)
    
    form = QuestionForm(request.POST or None, instance=cur_survey)


    if form.is_valid():
        form.save()
        messages.success(request, "Record Has Been Updated!")
        return redirect('home')
    
    return render(request, 'portfolio/update_survey.html', {'form':form})



    # print("Update is successful!")
    # messages.success(request, "Update is successful!")

    # daily_mp_vals = Portfolio.objects.all()

    # return render (request,'portfolio/mgronly_view.html', {'daily_mp_vals': daily_mp_vals})  

    
		
        