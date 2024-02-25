from django.urls import path
from . import views
from .views import MyAssetView, MgrOnlyView, SurveyView
from .views import PortfolioDV, PortfolioLV

#app_name = 'portfolio'
urlpatterns = [

    path('portfolio/', views.all_port, name='all_port'),
    path('portfolio/<int:pk>/', views.PortfolioDV.as_view(), name='detail'),    
    path('my_asset/', views.my_asset, name='my_asset'),
    
    #path('show_survey/<profile_id>', views.show_survey, name='show_survey'),
    path('survey/<int:pk>', views.customer_survey, name='view_survey'),
    path('update_survey/<int:pk>', views.update_survey, name='update_survey'),
    path('add_survey/<int:pk>', views.add_survey, name='add_survey'),

    #path('mgr_only/<str:fromdate>/<str:todate>/', views.mgr_only, name='mgr_only'), #종목별 weight
    path('mgr_only/', views.mgr_only, name='mgr_only'), #종목별 weight
    path('mgr_only1/', views.mgr_only1, name='mgr_only1'), #daily value 
    path('mgr_only2/', views.mgr_only2, name='mgr_only2'), #monthly return 
    path('mgr_only3/', views.mgr_only3, name='mgr_only3'), #자산별 weight

    #path('myasset/survey', SurveyView.as_view(), name='survey'),
    path('algo', views.algo, name='algo'), #run algo
    path('algo1', views.algo1, name='algo1'), #run algo1
    path('algo2', views.algo2, name='algo2'), #run algo2

    path('algoview/', views.algo_View, name='algo_View'), 
    path('algo1view/', views.algo1_View, name='algo1_View'), 
    path('algo2view/', views.algo2_View, name='algo2_View'), 


    path('util', views.update_daily_weights, name='update_daily_weights'),
    path('util1', views.update_daily_value, name='update_daily_value'),
    path('util2', views.update_monthly_value, name='update_monthly_value'),
    path('util4', views.update_clsweight, name='update_clsweight'),

    path('cal/sum', views.calculate_sum, name='calculate_sum'),
    path('cal/minus', views.calculate_minus, name='calculate_minus'),
]

