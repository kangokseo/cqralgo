from django import forms
from django.forms import ModelForm
from .models import Questionarie


class QuestionForm(ModelForm):
   # QA1 = forms.CharField(widget=forms.widgets.TextInput(attrs={"placeholder":"QA1", "class":"form-control"}), label="QA1")
   # riskscore = forms.CharField(widget=forms.widgets.TextInput(attrs={"placeholder":"riskscore", "class":"form-control"}), label="RiskScore")


    class Meta:
        model = Questionarie
        fields = "__all__"
       
