from django.db import models

# Create your models here.
class Portfolio(models.Model):
    title = models.CharField('TITLE', max_length=100, blank=True, null=True)
    url = models.URLField('URL', unique=True)

    def __str__(self):
        return self.title