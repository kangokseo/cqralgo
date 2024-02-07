from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import HomeView, UserCreateView, UserCreateDoneTV, UserEditView, UserLogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path('accounts/register/', UserCreateView.as_view(), name='register'),
    path('accounts/register/done/', UserCreateDoneTV.as_view(), name='register_done'),

    path('accounts/edit_profile/', UserEditView.as_view(), name='edit_profile'),

    path('<int:pk>/password/', auth_views.PasswordChangeView.as_view() ),
    path('accounts/logout/', UserLogoutView.as_view(), name='logged_out'),

    path('', HomeView.as_view(), name='home'),
    path('', include('portfolio.urls')),

] 

