from account.models import CustomerAccount
from app.models import Category

def UserAuthentication(request):
    sitename = "Design Adda"
    if request.session.has_key('customer_id'):        
        is_customer = request.session['customer_id']
        user_email = request.session['user_email']
        user_name = request.session['customer_name']
        context={
            'is_customer':is_customer,
            'user_email':user_email,
            'user_name':user_name,
            'sitename':sitename
        }
        return(context)
    else:
        context={
            "is_customer":None,
            "user_email":None,
            "user_name":None,
            "sitename":sitename,
        }
        return(context)
    
def AllCategories(request):
    categoreis = Category.objects.all()
    cat_list = []
    for cat in categoreis:
        if cat.status == 1:
            data = cat
            cat_list.append(data)
    context={
        'category':cat_list,
    }
    return(context)