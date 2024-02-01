"""
URL configuration for cqrsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

# from django.conf.urls.static import static
# from django.conf import settings

from cqrsite.views import HomeView
from cqrsite.views import UserCreateView, UserCreateDoneTV, UserEditView, UserLogoutView
from portfolio.views import PortfolioDV, PortfolioLV



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    #path('accounts/login/', include('django.contrib.auth.urls')),
    path('accounts/register/', UserCreateView.as_view(), name='register'),
    path('accounts/register/done/', UserCreateDoneTV.as_view(), name='register_done'),

    path('accounts/edit_profile/', UserEditView.as_view(), name='edit_profile'),

    #path('1/password/', auth_views.PasswordChangeView.as_view() ),
    path('accounts/logout/', UserLogoutView.as_view(), name='logged_out'),

    #class-based views
    path('', HomeView.as_view(), name='home'),
    path('portfolio/', include('portfolio.urls')),

] 

