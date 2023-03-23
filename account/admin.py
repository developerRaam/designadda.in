from django.contrib import admin
from .models import *
# Register your models here.
class CustomerAccountAdmin(admin.ModelAdmin):
    list_display = ("first_name","last_name","email","email_varify","mobile","mobile_varify","country","state","city","status","created_date")
admin.site.register(CustomerAccount,CustomerAccountAdmin)