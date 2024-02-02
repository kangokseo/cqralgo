from django.urls import path
from . import views
from cqrsite.views import MyAssetView, MgrOnlyView, RiskTolQ


#app_name = 'portfolio'
urlpatterns = [
    path('portfolio/', views.PortfolioLV.as_view(), name='index'),
    path('portfolio/<int:pk>/', views.PortfolioDV.as_view(), name='detail'),    
    path('myasset/', MyAssetView.as_view(), name='my_asset'),
    path('mgronly/', MgrOnlyView.as_view(), name='mgronly'),


]
