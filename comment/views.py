from django.shortcuts import render,HttpResponse,redirect
from .models import *

# Create your views here.
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
        return redirect('login')
        
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
        redirect('login')