from django.db import models
from autoslug import AutoSlugField
from tinymce.models import HTMLField
from account.models import *
from django.contrib.auth.models import User

class Category(models.Model):
    Status = {
        ('Active','Active'),
        ('Deactive','Deactive'),
    }
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=20, null=True, choices=Status, blank=True, default="Active")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(populate_from='name', unique=True,null=True, default=None)

    def __str__(self):
	    return self.name

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_type = models.ForeignKey(Category, verbose_name="Category", on_delete=models.CASCADE)
    description = HTMLField(null=True, blank=True)
    price = models.IntegerField(default='0')
    mrp = models.IntegerField(default='0')
    image = models.ImageField(upload_to="upload/",null=True, blank=True)
    product_zip = models.FileField(upload_to="product_zip/",null=True, blank=True)
    posted_by = models.CharField(max_length=50, null=True, blank=True, default="SKgraphics", editable=False)
    slug = AutoSlugField(populate_from='product_name', unique=True,null=True, default=None)
    views = models.IntegerField(default='0', editable=False)
    share = models.IntegerField(default='0', editable=False)
    downloads = models.IntegerField(default='0', editable=False)
    software_used  = models.CharField(max_length=100, null=True, blank=True, default="N/A")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product_name
    
    
class Like(models.Model):
    customer_id = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    
    
class Payment(models.Model):
    paymentStatus = {
        ('Pending','Pending'),
        ('Failed','Failed'),
        ('Credit','Credit')
    }
    order_no = models.CharField(max_length=150, unique=True)
    customer_id = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    downloads = models.IntegerField(default='0')
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=255, blank=True, null=True, default="")
    payment_request_id = models.CharField(max_length=255, blank=True, null=True, default="")
    payment_status = models.CharField(max_length=50,choices=paymentStatus,default='Pending')
    created_date = models.DateTimeField(auto_now_add=True)

class Cart(models.Model):
    customer_id = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE , null=True, blank=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)