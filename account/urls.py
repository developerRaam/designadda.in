from django.urls import path,include
from .import views

urlpatterns = [
    path("",views.CustomerLogin,name="login"),
    path("login/",views.CustomerLogin,name="login"),
    path("register/",views.Register, name="register"),
    path("profile/",views.Profile, name="profile"),
    path("update-account/",views.UpdateAccount, name="update-account"),
    path("change-password/", views.ChangePassword, name="change-password"),
    path("logout/",views.Logout, name="logout"),
    path("forgot/",views.Forgot, name="forgot"),
]