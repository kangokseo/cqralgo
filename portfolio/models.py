from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    RiskTol = models.CharField(max_length=5, null=True, blank=True) #위험성향
    def __str__(self):
        return str(self.user)



class Portfolio(models.Model):
    #id = 포트폴리오id
    title = models.CharField('TITLE', max_length=100, blank=True, null=True) 
    portid = models.IntegerField(null=True, blank=True) #알고리즘id
    url = models.URLField('URL', unique=True)
    minRiskTol = models.CharField(max_length=5, null=True, blank=True) #최저가능 위험성향
    astcls5_h =models.IntegerField(null=True, blank=True) #위험등급자산5_최고값 
    astcls5_l =models.IntegerField(null=True, blank=True) #위험등급자산5_최저값
    astcls4_h =models.IntegerField(null=True, blank=True) #위험등급자산4_최고값 
    astcls4_l =models.IntegerField(null=True, blank=True) #위험등급자산4_최저값
    astcls3_h =models.IntegerField(null=True, blank=True) #위험등급자산3_최고값 
    astcls3_l =models.IntegerField(null=True, blank=True) #위험등급자산3_최저값
    astcls2_h =models.IntegerField(null=True, blank=True) #위험등급자산2_최고값 
    astcls2_l =models.IntegerField(null=True, blank=True) #위험등급자산2_최저값
    astcls1_h =models.IntegerField(null=True, blank=True) #위험등급자산1_최고값 
    astcls1_l =models.IntegerField(null=True, blank=True) #위험등급자산1_최저값
    rskast_h = models.IntegerField(null=True, blank=True) #위험자산비중_최고값 
    rskast_l = models.IntegerField(null=True, blank=True) #위험자산비중_최저값 
    rskdgr_h = models.IntegerField(null=True, blank=True) #위험도_최고값
    rskdgr_l = models.IntegerField(null=True, blank=True) #위험도_최저값
    astcls_max = models.IntegerField(null=True, blank=True) #동일자산군 투자한도
    astclsi_max = models.IntegerField(null=True, blank=True) #동일상품 투자한도
    def __str__(self):
        return self.title
    

class ModelPort(models.Model):
    portid = models.CharField(null=True, blank=True) 
    incept_date = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.portid


class InvUniv(models.Model):
    종목코드 = models.CharField(null=True, blank=True) 
    종목명 = models.CharField(max_length=30, blank=True, null=True) 
    시장구분 = models.CharField(null=True, blank=True) #국내/해외
    자산군 = models.CharField(null=True, blank=True)  #ETF/주식
    자산종류 = models.CharField(null=True, blank=True) #지수ETF/채권ETF
    위험도 = models.CharField(null=True, blank=True) #1-5
    def __str__(self):
        return self.종목명 
    

class Questionarie(models.Model):
    userid = models.CharField(max_length=5, null=True, blank=True)
    QA1 = models.CharField(max_length=5, null=True, blank=True)
    QA2 = models.CharField(max_length=5, null=True, blank=True)
    QA3 = models.CharField(max_length=5, null=True, blank=True)
    QA4 = models.CharField(max_length=5, null=True, blank=True)
    QA5 = models.CharField(max_length=5, null=True, blank=True)
    QA6 = models.CharField(max_length=5, null=True, blank=True)
    QA7 = models.CharField(max_length=5, null=True, blank=True)
    riskscore =models.IntegerField(null=True, blank=True) #

    def __str__(self):
        return str(self.userid)


class Account(models.Model):
    user_id = models.CharField(null=True, blank=True) 
    계좌번호 = models.CharField(max_length=10, blank=True, null=True) 
    계좌명 = models.CharField(null=True, blank=True) 
    은행코드 = models.CharField(null=True, blank=True)  
    개설일시 = models.CharField(null=True, blank=True) 

    def __str__(self):
        return self.계좌번호 

