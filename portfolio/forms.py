from django import forms
from django.forms import ModelForm
from .models import Questionarie


QA1_CHOICES = [
    ('option1', '19세이하'),    
    ('option2', '20-40세'),
    ('option3', '41세-50세'),
    ('option4', '51세-64세'),
    ('option5', '61세-79세'),
    ('option6', '80세이상'),
]

QA2_CHOICES = [
    ('option1', '1년미만'),    
    ('option2', '1년이상-2년미만'),
    ('option3', '2년이상-3년미만'),
    ('option4', '3년이상-5년미만'),
    ('option5', '5년이상'),
]

QA3_CHOICES = [
    ('option1', '은행예금, 적금, 국채, 지방채, MMF'),    
    ('option2', '금융채, 회사채, 채권형펀드'),
    ('option3', '하이일드, 주식형펀드, ELS'),
    ('option4', 'LW, 선물옵션, 파생상품펀드'),
]

QA4_CHOICES = [
    ('option1', '금융투자상품에 투자해 본 경험이 없슴'),    
    ('option2', '주식, 채권, 펀드 등의 금융투자 상품의 내용 및 위험을 일정부분 이해하고 있슴'),
    ('option3', '주식, 채권, 펀드 등의 금융투자 상품의 내용 및 위험을 깊이있게 이해하고 있슴'),
    ('option4', '파생상품을 포함한 대부분의 금융투자상품의 내용 및 위험을 이해하고 있슴'),
]

QA5_CHOICES = [
    ('option1', '무슨일이 있어도 투자 원금은 보전되어야 한다'),    
    ('option2', '원금기준 +- 5%'),
    ('option3', '원금기준 +- 10%'),
    ('option4', '원금기준 +- 20%'),
    ('option5', '원금기준 +- 20% 초과'),
]

QA6_CHOICES = [
    ('option1', '보장성 상품'),    
    ('option2', '투자성 상품'),
    ('option3', '대출성 상품'),
    ('option4', '기타 상품'),
]

QA7_CHOICES = [
    ('option1', '채무상환'),    
    ('option2', '학비'),
    ('option3', '생활비'),
    ('option4', '주택마련'),
    ('option5', '자산증식'),
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
        fields = "__all__"  # Or specify the fields you need

