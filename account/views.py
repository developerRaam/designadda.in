from django.shortcuts import render,redirect,HttpResponse
from .models import *
from app.models import *
from django.contrib.auth.hashers import make_password,check_password
import random
import uuid
import mimetypes
from django.contrib.auth.models import auth
from django.core.paginator import Paginator
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail

#=====  User Registraition ==============
def Register(request):
    if request.session.has_key('customer_id'):
        return redirect('/')
    else:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            mobile = request.POST['mobile']
            email = request.POST['email']
            password = make_password(request.POST['password'])
            
            try:
                if (first_name and last_name and mobile and email and password) == '':
                    messages.warning(request, "Please fill out this field.")
                    return redirect('register')
                else:
                    if CustomerAccount.objects.filter(email=email).exists():
                        messages.warning(request, "Email already exists")
                        return redirect('register')
                    else:
                        email_otp =  random.randint(111111, 999999) # generate random otp
                        user = CustomerAccount.objects.create(first_name=first_name,last_name=last_name,mobile=mobile,email=email,password=password,email_otp=email_otp)
                        user.save()
                        send_mail_after_registration(email, email_otp)
                        messages.success(request, "We have sent OTP Please check your mail inbox/spam")
                        request.session['set_email'] = email
                        return redirect('send-otp')
            except Exception as e:
                messages.warning(request, "Something went wrong! Please check your Internet")
                return redirect('register')
        else:
            return render(request, 'account/register.html')
        
# Send Email otp
def OTP_Send(request):
    if request.session.has_key('set_email'):
        set_email = request.session['set_email']
        return render(request , 'account/email_otp_send.html',{'set_email':set_email})
    else:
        return HttpResponse("Bad request") 

# send mail
def send_mail_after_registration(email, email_otp):
    subject = 'Verify your Email. This otp send from DesignAdda.in'
    message = f"Your OTP number is :{email_otp}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list ) 

# Email Verification
def Email_Verification(request):
    if request.method == 'POST':
        email_otp = request.POST['email_otp']
        set_email = request.session['set_email']
        try:
            profile_obj = CustomerAccount.objects.filter(email_otp=email_otp).first()
            if profile_obj:
                if profile_obj.email_varify == True:
                    messages.success(request, 'Your account is already verified.')
                    return redirect('login')
                else:
                    profile_obj.email_varify = True
                    profile_obj.save()
                    CustomerAccount.objects.filter(email=set_email,email_otp=email_otp).update(email_otp=None)# Delete otp
                    del request.session['set_email'] # destroy session
                    messages.success(request, 'Registration completed successfully.')
                    return redirect('login')
            else:
                messages.warning(request,"OTP is wrong")
                return redirect('send-otp')
        
        except Exception as e:
            messages.warning(request, "Sorry! email not verified")
            return redirect('register')
    else:
        pass


#====  User Login =======================
def CustomerLogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = CustomerAccount.objects.filter(email=email)
        if user:
            user = CustomerAccount.objects.get(email=email)
            encodepass = user.password
            cust_email = user.email
            customer_id = user.id
            customer_name = user.first_name
            decodepass = check_password(password, encodepass)

            if cust_email == email and decodepass == True:
                if user.status == 0:
                    messages.warning(request, "Your account is disable. Please contact your administrator")
                    return redirect('login')
                elif user.email_varify == True:
                    request.session['customer_id']=customer_id
                    request.session['user_email']=email
                    request.session['customer_name']=customer_name
                    messages.success(request,"Login success")
                    return redirect('/')
                else:
                    messages.warning(request, "Your email is not verified. Please forgot your password!")
                    return redirect('login') 
            else:
                messages.warning(request, 'Invalid credentials')
                return redirect('login')
        else:
            messages.warning(request, "Invalid credentials")
            return redirect('login')
    else:
        # Session already login
        if request.session.has_key('customer_id'):
            return redirect('/')
        else:
            return render(request, 'account/login.html')


#===================== Customer Accounts =============================
def Profile(request):
    if request.session.has_key('customer_id'):
        is_customer_id = request.session['customer_id']
        is_customer = request.session['customer_name']
        customer = CustomerAccount.objects.get(id=is_customer_id)
        
        context={
            'customer':customer,
            'is_customer':is_customer
        }
        return render(request, 'account/profile.html', context)
    else:
        return redirect('login')  
    
    
#======================= Update Account ================================
def UpdateAccount(request):
    if request.session.has_key('customer_id'):
        is_customer_id = request.session['customer_id']
        is_customer_name = request.session['customer_name']
        session = request.session['user_email']
        user_profile = CustomerAccount.objects.get(email=session)
        context={
            'is_customer_id':is_customer_id,
            'is_customer':is_customer_name,
            'user_profile':user_profile,
        }
        if request.method == 'POST':
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            mobile = request.POST.get('mobile')

            profile_update = CustomerAccount.objects.get(email=session)
            profile_update.first_name=fname
            profile_update.last_name=lname
            profile_update.mobile=mobile
            profile_update.save()
            if profile_update:
                messages.success(request, "Profile Successfully Updated")
                return redirect('profile')
            else:
               messages.success(request, "Profile Updatedation failed")
               return redirect('update-account') 
        else:
           return render(request, "account/customer-account-update.html",context)
       
        return render(request, "account/customer-account-update.html",context)
    else:
        return redirect('login')


#====== Logout ====================
def Logout(request):
    del request.session['customer_id']
    del request.session['user_email']
    del request.session['customer_name']
    messages.success(request, "Logout Success")
    return redirect('login')

 
#==================== Forgot Password ================================
def Forgot(request):
    if request.session.has_key('customer_id'):
        return redirect('/')
    else:
        if request.method == "POST":
            email = request.POST['email']
            try:
                if CustomerAccount.objects.filter(email=email).exists():
                    token_key = uuid.uuid4()
                    CustomerAccount.objects.filter(email=email).update(auth_token=token_key)
                    send_mail_reset_password(email,token_key)
                    messages.success(request, "We have send email for reset password please check your mail")
                    return redirect('forgot-password')
                else:
                    messages.warning(request,"Email does not exists")
                    return redirect('forgot-password')
            except:
                return HttpResponse("Check your internet")
        else:
            return render(request, "account/forgot.html")
# send mail for reset
def send_mail_reset_password(email, token_key):
    subject = 'Reset Your Password'
    message = f"Click here to reset your password :http://127.0.0.1:8000/account/reset-password/{email}/{token_key}"
    #message = f"Click here to reset your password :https://www.herculeen.com/reset-password/{email}/{token_key}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list ) 
#======================= Reset Password ===========================
def ResetPassword(request,email,token_key):
    if request.session.has_key('customer_id'):
        return redirect('/')
    else:
        context={
                'email':email,
                'token_key':token_key
        }
        if request.method == 'POST':
            npassword = request.POST['npassword']
            rpassword = request.POST['rpassword']
            try:
                if npassword == rpassword:
                    npassword = make_password(npassword)
                    change_pass = CustomerAccount.objects.get(email=email,auth_token=token_key)
                    change_pass.password=npassword
                    change_pass.email_varify = True
                    change_pass.save()
                    messages.success(request,"Congratulations! Your password has been changed successfully.")
                    CustomerAccount.objects.filter(email=email,auth_token=token_key).update(auth_token=None)# Delete otp
                    return redirect('login')
                else:
                    messages.warning(request,"Password not match.")
                    return redirect('reset-password',email,token_key)
            except:
                return HttpResponse("Invalid url request")
        else:
            return render(request, "account/reset-password.html",context)

#=================== Change Password ========================
def ChangePassword(request):
    if request.session.has_key('customer_id'):
        is_customer_id = request.session['customer_id']
        is_customer_name = request.session['customer_name']
        session = request.session['user_email']
        cart_count = Cart.objects.all().count()
        context={
            'is_customer_id':is_customer_id,
            'is_customer':is_customer_name,
        }
        customer = CustomerAccount.objects.get(email=session)
        password = customer.password

        if request.method == 'POST':
            old_password = request.POST['old_Password']
            new_Password = request.POST['new_Password']
            re_Password = request.POST['re_Password']

            #Check password (old password to new password)
            o_password = check_password(old_password, password)

            if new_Password == re_Password:
                if o_password == True:
                    n_password = make_password(new_Password)
                    update_password = CustomerAccount.objects.get(email=session)
                    update_password.password=n_password
                    update_password.save()
                    messages.success(request, "Password Successfuly Changed")
                    return redirect('change-password')
                else:
                    messages.warning(request, "password not match")
                    return redirect('change-password')
            else:
                messages.warning(request, "password not match")
                return redirect('change-password')
        else:
            return render(request, "account/change-password.html",context)
    else:
        return redirect('login')