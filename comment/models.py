from django.db import models
from account.models import *
from app.models import *

# Create your models here.
class Comment(models.Model):
    customer_id = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE , null=True, blank=True, editable=False)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,editable=False)
    message = models.TextField(editable=False,)
    created_date = models.DateTimeField(auto_now_add=True)
    
class Reply(models.Model):
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE , null=True, blank=True)
    reply_user_id = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE , null=True, blank=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,editable=False)
    message = models.TextField(editable=False,)
    created_date = models.DateTimeField(auto_now_add=True)
    
class Rating(models.Model):
    customer_id = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE , null=True, blank=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)