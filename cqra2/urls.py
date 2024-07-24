from django.urls import path
from . import views


#app_name = 'portfolio'
urlpatterns = [

    path('cqra2/port_list', views.port_list, name='port_list'), #포트폴리오
    path('cqra2/port_list/ty<int:ty>', views.type_view, name='type_view'),  #모델 결과보기
    path('cqra2/port_list/range/ty<int:ty>', views.type_view_range, name='type_view_range'),  #모델 결과보기

    path('cqra2/acct_list/', views.acct_list, name='acct_list'), #계좌관리

    path('cqra2/mgr_asset_wgt/ty<int:ty>/', views.mgr_asset_wgt, name='mgr_asset_wgt'), #종목별 weight
    path('cqra2/mgr_class_wgt/ty<int:ty>/', views.mgr_class_wgt, name='mgr_class_wgt'), #자산별 weight
    path('cqra2/mgr_daily_ret/ty<int:ty>/', views.mgr_daily_ret, name='mgr_daily_ret'), #일별수익률추이
    path('cqra2/mgr_monthly_ret/ty<int:ty>/', views.mgr_monthly_ret, name='mgr_monthly_ret'), #월별수익률 

    path('cqra2/mp/ty<int:ty>/', views.run_algo, name='run_algo'), #run algo
    path('cqra2/mp/init_mpdb/ty<int:ty>/', views.init_mpdb, name='init_mpdb'),
    path('cqra2/mp/daily_update_mpdb/ty<int:ty>/', views.daily_update_mpdb, name='daily_update_mpdb'),

]

