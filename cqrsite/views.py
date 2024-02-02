from django.views.generic import TemplateView

from django.views.generic import CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy





class HomeView(TemplateView):
    template_name = 'home.html'

class MyAssetView(TemplateView):
    template_name = 'portfolio/my_asset.html'

class RiskTolQ(TemplateView):
    template_name = 'portfolio/risktolq_view.html'

class MgrOnlyView(TemplateView):
    template_name = 'portfolio/mgronly_view.html'

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




