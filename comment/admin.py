from django.contrib import admin
from .models import *

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ("customer_id","product_id","message","created_date")
admin.site.register(Comment,CommentAdmin)
