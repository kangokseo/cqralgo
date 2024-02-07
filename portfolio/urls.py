from django.urls import path
from . import views
from cqrsite.views import MyAssetView, MgrOnlyView, SurveyView


#app_name = 'portfolio'
urlpatterns = [
    path('portfolio1/', views.PortfolioLV.as_view(), name='index'),
    path('portfolio/', views.all_port, name='all_port'),
    path('portfolio/<int:pk>/', views.PortfolioDV.as_view(), name='detail'),    
    path('myasset/', MyAssetView.as_view(), name='my_asset'),
    path('my_asset/', views.my_asset, name='myasset'),
    path('all_mp/', views.all_mp, name='all_mp'),
    path('mgronly/', MgrOnlyView.as_view(), name='mgronly'),
    path('myasset/survey', SurveyView.as_view(), name='survey'),
    path('myasset/add_survey', views.add_survey, name='add_survey'),

]

