from django import forms
from django.forms import ModelForm
from .models import Questionarie


class QuestionForm(ModelForm):
    class Meta:
        model = Questionarie
        #fields = "__all__"
        fields = ('userid','QA1','QA2','QA3','QA4','QA5','QA6','QA7','riskscore')

