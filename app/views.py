from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import *
from comment.models import *
from django.contrib.auth.hashers import make_password,check_password
import random
import mimetypes
from django.core.paginator import Paginator

# Create your views here.

#=========================== Home ==============================

def Home(request):
    my_data = Category.objects.all()
    product = Product.objects.all().order_by('-created_date')
    
    paginator = Paginator(product, 10)  # Show 2 objects per page
    page = request.GET.get('page')
    product = paginator.get_page(page)
    
    if request.session.has_key('customer_id'):
        is_customer = request.session['customer_name']
        context = {
                'category':my_data,
                'product':product,
                'is_customer':is_customer
        }
        return render(request,"app/home.html",context)
    else:
        context = {
                'category':my_data,
                'product':product,
        }
        return render(request,"app/home.html",context)



#=========================== Search Product ==================================

def SearchProduct(request):
    if request.method == 'GET':
        search_bar = request.GET['q']
        if search_bar == "":
            return redirect('/')
        else:
            search_data = Product.objects.filter(product_name__icontains=search_bar)
            cat_data = Category.objects.all()
            context = {
                'category':cat_data,
                'product':search_data,
                "search_bar":search_bar
            }
            return render(request, "app/search.html", context)
    else:
        HttpResponse("page not found")

#================================ Product Detail =======================================================
def ProductDetail(request,prd_slug):
    slug=Product.objects.get(slug=prd_slug)
    comments = Comment.objects.filter(product_id_id = slug.id).order_by('-created_date')
    reply = Reply.objects.all().order_by('-created_date')
    slug.views= slug.views + 1
    slug.save()
    product_id = slug.id
    
    filesize=''
    filename=''
    filetype=''
    if slug.product_zip != '':
        filesize = slug.product_zip.file.size # Get image size
        filename = str(slug.product_zip)
        filename = filename.replace('_', ' ')
        filetype = mimetypes.guess_type(filename)[0]
    
    my_data = Category.objects.all()
    product = Product.objects.all().order_by('-views')
    
    # show releted product
    prd = slug.product_name
    slc = slice(20)
    product = Product.objects.filter(product_name__icontains=str(prd[slc])).order_by("product_name")[:20]
    total_likes = Like.objects.filter(product_id=product_id).count() #Total likes
    
    if request.session.has_key('customer_id'):
        is_customer = request.session['customer_name']
        is_customer_id = request.session['customer_id']
        if Like.objects.filter(product_id=product_id,customer_id=is_customer_id).exists():
            like_status = 1
        else:
            like_status = 0
        
        context = {
                'product_slug':slug,
                'category':my_data,
                'is_customer':is_customer,
                'is_customer_id':is_customer_id,
                'product':product,
                'filesize':filesize,
                'total_likes':total_likes,
                'like_status':like_status,
                'filename':filename,
                'filetype':filetype,
                'comments':comments,
                'reply':reply
        }
        return render(request,"app/detail.html",context)
    else:
        context = {
                'product_slug':slug,
                'category':my_data,
                'popular_prd':product,
                'total_likes':total_likes,
                'comments':comments,
                'reply':reply
        }
        return render(request,"app/detail.html",context)


#=============================== Category Data  ================================================
def CategoryData(request,cat_id):
    product = Product.objects.filter(product_type=cat_id)
    cat_data = Category.objects.all()
    
    paginator = Paginator(product, 2)  # Show 2 objects per page
    page = request.GET.get('page')
    product = paginator.get_page(page)
    
    if request.session.has_key('customer_id'):
        is_customer = request.session['customer_name']
        context = {
            'product':product,
            'category':cat_data,
            'is_customer':is_customer,

        }
        return render(request, "app/filter-by-cat-name.html",context)
    else:
        context = {
            'product':product,
            'category':cat_data,

        }
        return render(request, "app/filter-by-cat-name.html",context)


#=============  Likes =================
def Likes(request, user_id, item_id, prd_slug):
    if request.session.has_key('customer_id'):
        is_customer_id = request.session['customer_id']
        
        if Like.objects.filter(customer_id_id=is_customer_id,product_id_id=item_id).exists():
            Like.objects.filter(customer_id_id=is_customer_id,product_id_id=item_id).delete()
        else:
            likes = Like.objects.create(customer_id_id=is_customer_id,product_id_id=item_id)
            likes.save()
            
        return redirect('detail',prd_slug)
    else:
        return redirect('login')


#=============  Download =================
def Download(request, user_id, item_id, prd_slug):
    if request.session.has_key('customer_id'):
        is_customer_name = request.session['customer_name']
        update = Product.objects.get(id=item_id)
        downloads = update.downloads
        update.downloads = downloads + 1
        update.save()

        filesize=''
        filename=''
        filetype=''
        if update.product_zip != '':
            filesize = update.product_zip.file.size # Get image size
            filename = str(update.product_zip)
            filename = filename.replace('_', ' ')
            filetype = mimetypes.guess_type(filename)[0]

        prd_data=Product.objects.get(id=item_id)
        category = Category.objects.all()
        context = {
            'prd_data':prd_data,
            'is_customer':is_customer_name,
            'filesize':filesize,
            'filename':filename,
            'filetype':filetype,
            'category':category,
        }
        return render(request, 'app/download.html',context)
    else:
        return redirect('login')

    
#=============================== Payment ===============================
def Payment(request, item_id,prd_slug):
    if request.session.has_key('customer_id'):
        is_customer_id = request.session['customer_id']
        is_customer_name = request.session['customer_name']
        
        order = Product.objects.get(id=item_id)
        
        filesize=''
        filename=''
        filetype=''
        if order.product_zip != '':
            filesize = order.product_zip.file.size # Get product size
            filename = str(order.product_zip)
            filename = filename.replace('_', ' ')
            filetype = mimetypes.guess_type(filename)[0]
        
        customer = CustomerAccount.objects.get(id=is_customer_id) 
        customer_email = customer.email
        category = Category.objects.all()
        
        context={
            'is_customer_id':is_customer_id,
            'is_customer':is_customer_name,
            'customer_email':customer_email,
            'order':order,
            'filename':filename,
            'filetype':filetype,
            'filesize':filesize,
            'category':category,
            }
        return render(request, "app/payment.html",context)
    else:
        return redirect('login')
    
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
            return render(request, "app/change-password.html",context)
    else:
        return redirect('/login')
  
  
#============== Comments =================================
def ProductComments(request):
    if request.session.has_key('customer_id'):
        if request.method == 'POST':
            product_id = request.POST['product_id']
            prd_slug = request.POST['prd_slug']
            user_id = request.session['customer_id']
            comment = request.POST['comment']
            if (product_id and user_id and comment) != '' :
                save_comment = Comment.objects.create(product_id_id=product_id,customer_id_id=user_id,message=comment)
                save_comment.save()
                return redirect('detail',prd_slug)
            else:
                return HttpResponse("All field are required")
        else:
            return HttpResponse("Comment not send check your internet") 
    else:
        return redirect('/login')
        
def ProductReply(request):
    if request.session.has_key('customer_id'):
        if request.method == 'POST':
            reply_user_id = request.session['customer_id']
            comment_id = request.POST['comment_id']
            product_id = request.POST['product_id']
            prd_slug = request.POST['prd_slug']
            message = request.POST['message']
            if (reply_user_id and comment_id and product_id and prd_slug and message) != '' :
                save_comment = Reply.objects.create(reply_user_id_id=reply_user_id,comment_id_id=comment_id,product_id_id=product_id,message=message)
                save_comment.save()
                return redirect('detail',prd_slug)
            else:
                return HttpResponse("All field are required")
        else:
            return HttpResponse("Comment not send check your internet")
    else:
        redirect('/login')