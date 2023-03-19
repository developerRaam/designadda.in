from django.urls import path,include
from .import views

# admin.site.site_header = "Ecommerce Lucknow Admin"
# admin.site.site_title = "Ecommerce Admin Portal"
# admin.site.index_title = "Welcome to Ecommerce Portal"

urlpatterns = [
    path("",views.Home,name="home"),
    path("detail/<prd_slug>",views.ProductDetail,name="detail"),
    path("filter-by-cat-name/<int:cat_id>",views.CategoryData, name="filter-by-cat-name"),
    path("search",views.SearchProduct, name="search"),
    path("likes/<user_id>/<item_id>/<prd_slug>",views.Likes, name="likes"),
    path("download/<user_id>/<item_id>/<prd_slug>",views.Download, name="download"),
    path("payment/<item_id>/<prd_slug>",views.Payment, name="payment"),
    path("change-password/", views.ChangePassword, name="change-password"),
    
    path("comment/",views.ProductComments, name="comment"),
    path("reply/",views.ProductReply, name="reply")
]