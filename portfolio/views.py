from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy

from cqrsite.views import HomeView
from .forms import QuestionForm
from .models import ModelPort, Portfolio, Profile, Questionarie, dailyMPvalue
from django.shortcuts import redirect
from django.contrib import messages

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


def mgr_only(request):
    if request.user.is_authenticated and request.user.is_superuser:
        daily_mp_vals = Portfolio.objects.all()

        return render (request,'portfolio/mgronly_view.html', {'daily_mp_vals': daily_mp_vals})   

    else:
        return render(request, 'portfolio/mgronly_view.html', {})   


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
    #form = QuestionForm(request.POST)
    form = QuestionForm(request.POST or None, instance=cur_survey)
    
    return render(request, 'portfolio/update_survey.html', {'form':form})
    
		
        