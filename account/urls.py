from django.urls import path,include
from .import views

urlpatterns = [
    path("",views.CustomerLogin,name="login"),
    path("login/",views.CustomerLogin,name="login"),
    
    path("register/",views.Register, name="register"),
    path("send-otp/",views.OTP_Send, name="send-otp"),
    path("email-verify/",views.Email_Verification, name="email-verify"),
    
    path("change-password/", views.ChangePassword, name="change-password"),
    path("forgot-password/",views.Forgot, name="forgot-password"),
    path("reset-password/<email>/<token_key>",views.ResetPassword, name="reset-password"),
    
    path("profile/",views.Profile, name="profile"),
    path("update-account/",views.UpdateAccount, name="update-account"),
    path("logout/",views.Logout, name="logout"),
]