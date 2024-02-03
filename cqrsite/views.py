from django.views.generic import TemplateView

from django.views.generic import CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'

class MyAssetView(TemplateView):
    template_name = 'portfolio/my_asset.html'

class RiskTolQsView(TemplateView):
    template_name = 'portfolio/risktolq_view.html'

class MgrOnlyView(UserPassesTestMixin, TemplateView):
    template_name = 'portfolio/mgronly_view.html'
    login_url = '/'

    def test_func(self):
        return self.request.user.is_superuser
    

class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')

class UserEditView(UpdateView):
    template_name = 'registration/edit_profile.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'

class UserLogoutView(TemplateView):
    template_name = 'registration/logged_out.html'




