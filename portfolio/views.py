from django.shortcuts import render

from django.views.generic import ListView, DetailView
from portfolio.models import Portfolio, Profile

from django.http import HttpResponseRedirect
from .forms import QuestionForm
from .models import Questionarie
from .models import ModelPort


# Create your views here.
def all_mp(request):
    mp_list = ModelPort.objects.all()
    return render (request,'portfolio/mgronly_view.html', {'mp_list': mp_list})   

def all_port(request):
    port_list = Portfolio.objects.all()
    return render (request,'portfolio/portfolio_list.html', {'port_list': port_list})   

def my_asset(request):
    if request.user.is_authenticated:
        me = request.user.id
        profile_item = Profile.objects.filter(user_id=me)

        print (profile_item)

        return render(request, 'portfolio/my_asset.html', {"profile_item":profile_item})
        #return render(request, 'portfolio/my_asset.html', {"me":me})
    else:
        return render(request, 'portfolio/mgronly_view.html', {})

class PortfolioLV(ListView):
    model = Portfolio


class PortfolioDV(DetailView):
    model = Portfolio


def add_survey(request):
    submitted = False

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

