from django.urls import path
from . import views
from .views import MyAssetView, MgrOnlyView, SurveyView
from .views import PortfolioDV, PortfolioLV

#app_name = 'portfolio'
urlpatterns = [

    path('portfolio/', views.all_port, name='all_port'),
    path('portfolio/<int:pk>/', views.PortfolioDV.as_view(), name='detail'),    
    path('my_asset/', views.my_asset, name='my_asset'),
    path('account_list/', views.account_list, name='account_list'),

    path('account_item/<int:id>', views.account_item, name='account_item'),
    path('util_rebal_00/<int:id>', views.rebalancing_00, name='rebalancing_00'),    #지정가 리밸런싱
    path('util_rebal_06/<int:id>', views.rebalancing_06, name='rebalancing_06'),    #장후시간외 리밸런싱

    #path('show_survey/<profile_id>', views.show_survey, name='show_survey'),
    path('survey/<str:pk>', views.view_survey, name='view_survey'),
    path('update_survey/<str:pk>', views.update_survey, name='update_survey'),
    path('add_survey/<int:pk>', views.add_survey, name='add_survey'),

    #path('mgr_only/<str:fromdate>/<str:todate>/', views.mgr_only, name='mgr_only'), #종목별 weight
    path('mgr_only/ty<int:ty>/', views.mgr_only, name='mgr_only'), #종목별 weight
    path('mgr_only/ty<int:ty>/1/', views.mgr_only1, name='mgr_only1'), #일별수익률추이
    path('mgr_only/ty<int:ty>/2/', views.mgr_only2, name='mgr_only2'), #월별수익률 
    path('mgr_only/ty<int:ty>/3/', views.mgr_only3, name='mgr_only3'), #자산별 weight

    #path('myasset/survey', SurveyView.as_view(), name='survey'),
    path('algo/<int:ty>/', views.algo, name='algo'), #run algo
    path('algoview/<int:ty>', views.algo_View, name='algo_View'),  #모델결과보기

    path('util_daily/<int:ty>/', views.add_daily, name='add_daily'),
    path('util_daily/init/<int:ty>/', views.init_add_daily, name='init_add_daily'),

]

