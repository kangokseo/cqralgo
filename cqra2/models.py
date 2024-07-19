from django.db import models

# Create your models here.

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