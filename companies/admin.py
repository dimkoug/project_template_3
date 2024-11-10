from django.contrib import admin

# Register your models here.
from companies.models import Company

class CompanyAdmin(admin.ModelAdmin):
    pass


admin.site.register(Company, CompanyAdmin)