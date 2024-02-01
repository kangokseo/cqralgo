from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    RiskTol = models.CharField(max_length=5)
    def __str__(self):
        return str(self.user)


class Portfolio(models.Model):
    title = models.CharField('TITLE', max_length=100, blank=True, null=True)
    url = models.URLField('URL', unique=True)

    def __str__(self):
        return self.title