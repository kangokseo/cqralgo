from django.shortcuts import render

from django.views.generic import ListView, DetailView
from portfolio.models import Portfolio

# Create your views here.
    
class PortfolioLV(ListView):
    model = Portfolio

class PortfolioDV(DetailView):
    model = Portfolio