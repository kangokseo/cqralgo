from django.contrib import admin
from portfolio.models import Portfolio, Profile, InvUniv, ModelPort, Account, Questionarie, dailyMPweight, dailyMPvalue

# Register your models here.
@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',  'minRiskTol' , 'astcls5_h', 'astcls4_h', 'astcls3_h', 'astcls2_h', 'astcls1_h', 'rskast_h', 'astcls_max', 'astclsi_max')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=('id', 'RiskTol', "RiskTolDesc")


#admin.site.register(InvUniv)
@admin.register(InvUniv)
class InvUnivAdmin(admin.ModelAdmin):
    list_display=('종목코드', '종목명','시장구분','자산군', '자산종류','위험도')

@admin.register(ModelPort)
class ModelPortAdmin(admin.ModelAdmin):
    list_display=('id', 'portid', 'incept_date')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display=('id', 'user_id','계좌번호','계좌명', '은행코드','개설일시')

@admin.register(Questionarie)
class QuestionarieAdmin(admin.ModelAdmin):
    list_display=('userid', 'QA1', 'QA2', 'QA3', 'QA4', 'QA5', 'QA6', 'QA7', 'riskscore')

@admin.register(dailyMPweight)
class dailyMPweightAdmin(admin.ModelAdmin):
    list_display=('date' ,'port_id')   

@admin.register(dailyMPvalue)
class dailyMPvalueAdmin(admin.ModelAdmin):
    list_display=('date', 'port_id')   