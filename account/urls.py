from django.urls import path,include
from .import views

urlpatterns = [
    path("",views.CustomerLogin,name="login"),
    path("login/",views.CustomerLogin,name="login"),
    path("register/",views.Register, name="register"),
    path("account/",views.CustomerAccounts, name="account"),
    path("update-account/",views.UpdateAccount, name="update-account"),
    path("logout/",views.Logout, name="logout"),
    path("forgot/",views.Forgot, name="forgot"),
]