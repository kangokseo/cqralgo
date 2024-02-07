from django.urls import path
from . import views
from .views import MyAssetView, MgrOnlyView, SurveyView
from .views import PortfolioDV, PortfolioLV

#app_name = 'portfolio'
urlpatterns = [

    path('portfolio/', views.all_port, name='all_port'),
    path('portfolio/<int:pk>/', views.PortfolioDV.as_view(), name='detail'),    
    path('my_asset/', views.my_asset, name='my_asset'),
    path('mgr_only/', views.mgr_only, name='mgr_only'),
    path('myasset/survey', SurveyView.as_view(), name='survey'),
    path('myasset/add_survey', views.add_survey, name='add_survey'),

]

