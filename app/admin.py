from django.contrib import admin
from .models import *
from django.utils.html import format_html

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name","status","created_date")
admin.site.register(Category,CategoryAdmin)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("name","category","status","created_date")
admin.site.register(SubCategory,SubCategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:70px; max-height:70px"/>'.format(obj.image.url))
    list_display = ("product_name","image_tag","slug","posted_by","product_type","sub_category","views","downloads","image","created_date")
    list_filter = ("product_type","created_date")
    search_fields=('product_name',)
    list_per_page=15 #record 15 per page
admin.site.register(Product,ProductAdmin)

# class CartAdmin(admin.ModelAdmin):
#     list_display = ("customer_id","product_id","quantity","created_date")
# admin.site.register(Cart,CartAdmin)

# class LikeAdmin(admin.ModelAdmin):
#         list_display = ("customer_id","product_id","created_date")
# admin.site.register(Like,LikeAdmin)