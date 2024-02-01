from django.urls import path
from . import views

#app_name = 'portfolio'
urlpatterns = [
    #path('portfolio/', PortfolioLV.as_view(), name='index'),
    # path('portfolio/<int:pk>/', PortfolioDV.as_view(), name='detail'),    

    path('', views.PortfolioLV.as_view(), name='index'),
    path('<int:pk>/', views.PortfolioDV.as_view(), name='detail'),    
]
