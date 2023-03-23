from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import *
from comment.models import Comment,Reply    
from django.contrib.auth.hashers import make_password,check_password
import random
import mimetypes
from django.core.paginator import Paginator
from account.context_processors import UserAuthentication

# Create your views here.

#=========================== Home ==============================

def Home(request):
    category = Category.objects.all().order_by('-created_date')
    products = Product.objects.all().order_by('-created_date')
    #Filter product by category is Enable
    product_list = []
    for i in category:
        for j in products:
            if i.status == 1:
                if i.id == j.product_type_id:
                    data = j
                    product_list.append(data)
    
    paginator = Paginator(product_list, 10)  # Show 2 objects per page
    page = request.GET.get('page')
    product = paginator.get_page(page)
    context = {
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
            #Filter product by category is Enable
            products = Product.objects.filter(product_name__icontains=search_bar)
            category = Category.objects.all().order_by('-created_date')
            product_list = []
            for i in category:
                for j in products:
                    if i.status == 1:
                        if i.id == j.product_type_id:
                            data = j
                            product_list.append(data)
            context = {
                'product':product_list,
                "search_bar":search_bar
            }
            return render(request, "app/search.html", context)
    else:
        HttpResponse("page not found")

#================================ Product Detail =======================================================
def ProductDetail(request,prd_slug):
    slug=Product.objects.get(slug=prd_slug)
    comments = Comment.objects.filter(product_id_id = slug.id).order_by('-created_date')
    reply = Reply.objects.all()#.order_by('-created_date')
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
        
    product = Product.objects.all().order_by('-views')
    
    # show releted product
    prd = slug.product_name
    slc = slice(20)
    product = Product.objects.filter(product_name__icontains=str(prd[slc])).order_by("product_name")[:20]
    total_likes = Like.objects.filter(product_id=product_id).count() #Total likes
    
    if request.session.has_key('customer_id'):
        is_customer = request.session['customer_id']
        if Like.objects.filter(product_id=product_id,customer_id=is_customer).exists():
            like_status = 1
        else:
            like_status = 0
        
        context = {
                'product_slug':slug,
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
                'popular_prd':product,
                'total_likes':total_likes,
                'comments':comments,
                'reply':reply
        }
        return render(request,"app/detail.html",context)


#=============================== Category Data  ================================================
def CategoryData(request,cat_id):
    product = Product.objects.filter(product_type=cat_id)   
    paginator = Paginator(product, 2)  # Show 2 objects per page
    page = request.GET.get('page')
    product = paginator.get_page(page)
    context = {
        'product':product,

    }
    return render(request, "app/filter-by-cat-name.html",context)


#=============  Likes =================
def Likes(request, user_id, item_id, prd_slug):
    if request.session.has_key('customer_id'):
        is_customer = request.session['customer_id']
        
        if Like.objects.filter(customer_id_id=is_customer,product_id_id=item_id).exists():
            Like.objects.filter(customer_id_id=is_customer,product_id_id=item_id).delete()
        else:
            likes = Like.objects.create(customer_id_id=is_customer,product_id_id=item_id)
            likes.save()
            
        return redirect('detail',prd_slug)
    else:
        return redirect('login')


#=============  Download =================
def Download(request, user_id, item_id, prd_slug):
    if request.session.has_key('customer_id'):
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
        context = {
            'prd_data':prd_data,
            'filesize':filesize,
            'filename':filename,
            'filetype':filetype,
        }
        return render(request, 'app/download.html',context)
    else:
        return redirect('login')

    
#=============================== Payment ===============================
def Payment(request, item_id,prd_slug):
    if request.session.has_key('customer_id'):
        is_customer = request.session['customer_id']
        order = Product.objects.get(id=item_id)
        filesize=''
        filename=''
        filetype=''
        if order.product_zip != '':
            filesize = order.product_zip.file.size # Get product size
            filename = str(order.product_zip)
            filename = filename.replace('_', ' ') # remove underscrore from filename
            filetype = mimetypes.guess_type(filename)[0]
        
        customer = CustomerAccount.objects.get(id=is_customer) 
        customer_email = customer.email
        
        context={
            'order':order,
            'filename':filename,
            'filetype':filetype,
            'filesize':filesize,
            }
        return render(request, "app/payment.html",context)
    else:
        return redirect('login')
  
  
