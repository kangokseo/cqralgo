from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    RiskTol = models.CharField(max_length=5, null=True, blank=True) #위험성향
    RiskTolDesc = models.CharField(max_length=10, null=True, blank=True) #위험성향설명
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
    
#5, 229200, KODEX 코스닥150
#3, 133690, TIGER 미국나스닥100
#3, 069500, KODEX 200
##2, 379800, KODEX 미국S&P500TR     
#2,  143850,  TIGER 미국S&P500선물(H)
#1, 114260, KODEX 국고채3년
#1, 153130, KODEX 단기채권
#1,  157450,    TIGER 단기통안채
#0 현금 예수금

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
    riskscore =models.CharField(null=True, blank=True)

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


class dailyMPweight(models.Model): #종목별투자비중추이

    date = models.DateField(null=True, blank=True)
    port_id = models.CharField(null=True, blank=True)
    item1_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    item2_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    item3_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    item4_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    item5_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    item6_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    item7_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    item8_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    port_total = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    
    def __str__(self):
        return self.date 


class MPclsweight(models.Model): #자산별투자비중추이

    date = models.DateField(null=True, blank=True)
    port_id = models.CharField(null=True, blank=True)
    cls5_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    cls4_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    cls3_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    cls2_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    cls1_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    total = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    risk_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    
    def __str__(self):
        return self.date 
    


class dailyMPvalue(models.Model):  #일별수익률추기

    date = models.DateField(null=True, blank=True)
    port_id = models.CharField(null=True, blank=True)
    item1_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    item2_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    item3_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    item4_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    item5_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    item6_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    item7_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    item8_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    port_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    port_ret = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    acum_ret = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    
    def __str__(self):
        return self.date 


class monthlyMPvalue(models.Model): #월별수익률추이

    date = models.DateField(null=True, blank=True)
    port_id = models.CharField(null=True, blank=True)
    item1_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    item2_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    item3_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    item4_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    item5_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    item6_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    item7_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    item8_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    port_val = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    port_ret = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    acum_ret = models.DecimalField (max_digits=20, decimal_places=6,null=True, blank=True)
    
    def __str__(self):
        return self.date 
    
#postgreSQL
# CREATE TABLE portfolio_dailyMPval (
#     date DATE NOT NULL,
# 	port_id integer,
# 	item1_val NUMERIC(20,6),
# 	item2_val NUMERIC(20,6),
# 	item3_val NUMERIC(20,6),
# 	item4_val NUMERIC(20,6),
# 	item5_val NUMERIC(20,6),
# 	item6_val NUMERIC(20,6),
# 	item7_val NUMERIC(20,6),
# 	item8_val NUMERIC(20,6),
# 	port_val NUMERIC(20,6),
# 	port_ret NUMERIC(20,6)
# );
    