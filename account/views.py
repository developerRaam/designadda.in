from django.shortcuts import render
from .models import *
from app.models import *

#=====  User Registraition ==============
def Register(request):
    category = Category.objects.all()
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
            return render(request, 'account/register.html',{'category':category,})

#====  User Login =======================
def CustomerLogin(request):
    my_data = Category.objects.all()
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
                if user.status == "Active":
                    request.session['customer_id']=customer_id
                    request.session['user_email']=email
                    request.session['customer_name']=customer_name
                    messages.success(request,"Login success")
                    return redirect('/')
                else:
                    messages.warning(request, "Your account is desable. Please forgot your password")
                    return redirect('/login') 
            else:
                messages.warning(request, 'Invalid credentials')
                return redirect('/login')
        else:
            messages.warning(request, "Invalid credentials")
            return redirect('/login')
    else:
        # Session already login
        if request.session.has_key('customer_id'):
            return redirect('/')
        else:
            return render(request, 'account/login.html',{'category':my_data,})


#===================== Customer Accounts =============================
def CustomerAccounts(request):
    if request.session.has_key('customer_id'):
        is_customer_id = request.session['customer_id']
        is_customer = request.session['customer_name']
        customer = CustomerAccount.objects.get(id=is_customer_id)
        
        context={
            'customer':customer,
            'is_customer':is_customer
        }
        return render(request, 'account/customer-account.html', context)
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
                return redirect('/account')
            else:
               messages.success(request, "Profile Updatedation failed")
               return redirect('/account') 
        else:
           return render(request, "account/customer-account-update.html",context)
       
        return render(request, "account/customer-account-update.html",context)
    else:
        return redirect('/login')


#====== Logout ====================

def Logout(request):
    auth.logout(request)
    return redirect('/')


#=============  Forgot =================
def Forgot(request):
    cat_data = Category.objects.all()
    context = {
        'category':cat_data,
    }
    return render(request, "account/forgot.html",context)