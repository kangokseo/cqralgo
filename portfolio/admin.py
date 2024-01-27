from django.contrib import admin
from portfolio.models import Portfolio

# Register your models here.
@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url')