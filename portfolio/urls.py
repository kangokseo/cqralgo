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

    path('mgr_only/', views.mgr_only, name='mgr_only'),
    path('myasset/survey', SurveyView.as_view(), name='survey'),
    

]

