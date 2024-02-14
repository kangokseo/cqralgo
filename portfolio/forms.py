from django import forms
from django.forms import ModelForm
from .models import Questionarie


QA1_CHOICES = [
    ('1', '19세이하'),    
    ('2', '20-40세'),
    ('3', '41세-50세'),
    ('4', '51세-64세'),
    ('5', '61세-79세'),
    ('6', '80세이상'),
]

QA2_CHOICES = [
    ('1', '1년미만'),    
    ('2', '1년이상-2년미만'),
    ('3', '2년이상-3년미만'),
    ('4', '3년이상-5년미만'),
    ('5', '5년이상'),
]

QA3_CHOICES = [
    ('1', '은행예금, 적금, 국채, 지방채, MMF'),    
    ('2', '금융채, 회사채, 채권형펀드'),
    ('3', '하이일드, 주식형펀드, ELS'),
    ('4', 'LW, 선물옵션, 파생상품펀드'),
]

QA4_CHOICES = [
    ('1', '금융투자상품에 투자해 본 경험이 없슴'),    
    ('2', '주식, 채권, 펀드 등의 금융투자 상품의 내용 및 위험을 일정부분 이해하고 있슴'),
    ('3', '주식, 채권, 펀드 등의 금융투자 상품의 내용 및 위험을 깊이있게 이해하고 있슴'),
    ('4', '파생상품을 포함한 대부분의 금융투자상품의 내용 및 위험을 이해하고 있슴'),
]

QA5_CHOICES = [
    ('1', '무슨일이 있어도 투자 원금은 보전되어야 한다'),    
    ('2', '원금기준 +- 5%'),
    ('3', '원금기준 +- 10%'),
    ('4', '원금기준 +- 20%'),
    ('5', '원금기준 +- 20% 초과'),
]

QA6_CHOICES = [
    ('1', '보장성 상품'),    
    ('2', '투자성 상품'),
    ('3', '대출성 상품'),
    ('4', '기타 상품'),
]

QA7_CHOICES = [
    ('1', '채무상환'),    
    ('2', '학비'),
    ('3', '생활비'),
    ('4', '주택마련'),
    ('5', '자산증식'),
]


class QuestionForm(ModelForm):
    QA1 = forms.ChoiceField(
        choices=QA1_CHOICES, 
        widget=forms.RadioSelect, 
        label="1. 연령대"
    )

    QA2 = forms.ChoiceField(
        choices=QA2_CHOICES, 
        widget=forms.RadioSelect, 
        label="2. 투자가능기간"
    ) 

    QA3 = forms.ChoiceField(
        choices=QA3_CHOICES, 
        widget=forms.RadioSelect, 
        label="3. 투자경험"
    ) 

    QA4 = forms.ChoiceField(
        choices=QA4_CHOICES, 
        widget=forms.RadioSelect, 
        label="4. 금융지식 이해도"
    ) 

    QA5 = forms.ChoiceField(
        choices=QA5_CHOICES, 
        widget=forms.RadioSelect, 
        label="5. 기대 이익수준 및 손실감내 수준"
    ) 

    QA6 = forms.ChoiceField(
        choices=QA6_CHOICES, 
        widget=forms.RadioSelect, 
        label="6. 총자산대비 금융상품 기준"
    ) 
    
    QA7 = forms.ChoiceField(
        choices=QA7_CHOICES, 
        widget=forms.RadioSelect, 
        label="7. 금융투자상품 처분목적"
    ) 

    class Meta:
        model = Questionarie
        #fields = "__all__"  # Or specify the fields you need
        fields = ['QA1', 'QA2', 'QA3', 'QA4', 'QA5', 'QA6', 'QA7']

