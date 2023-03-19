from django.contrib import admin
from .models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name","status","created_date","updated_date")
admin.site.register(Category,CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name","slug","posted_by","product_type","views","downloads","price","image","created_date")
admin.site.register(Product,ProductAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ("customer_id","product_id","quantity","created_date")
admin.site.register(Cart,CartAdmin)

class LikeAdmin(admin.ModelAdmin):
        list_display = ("customer_id","product_id","created_date")
admin.site.register(Like,LikeAdmin)