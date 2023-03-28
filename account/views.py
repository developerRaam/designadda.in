from django.shortcuts import render,redirect,HttpResponse
from .models import *
from app.models import *
from django.contrib.auth.hashers import make_password,check_password
import random
import mimetypes
from django.core.paginator import Paginator
from django.contrib import messages
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
            
            if CustomerAccount.objects.filter(email=email).exists():
                messages.warning(request, "Email already exists")
                return redirect('register')
            else:
                user = CustomerAccount.objects.create(first_name=first_name,last_name=last_name,mobile=mobile,email=email,password=password)
                user.save()
                messages.success(request, "User created successful")
                return redirect('login')
        else:
            return render(request, 'account/register.html')


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
                if user.status == 1:
                    request.session['customer_id']=customer_id
                    request.session['user_email']=email
                    request.session['customer_name']=customer_name
                    messages.success(request,"Login success")
                    return redirect('/')
                else:
                    messages.warning(request, "Your account is disable. Please forgot your password")
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


#=============  Forgot =================
def Forgot(request):
    return render(request, "account/forgot.html")

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