from django.contrib import admin
from portfolio.models import Portfolio, Profile

# Register your models here.
@admin.register(Portfolio)

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url')


admin.site.register(Profile)