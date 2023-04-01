from django.db import models

# Create your models here.
STATUS = ((1, 'Active'), (0, 'Deactive'))

class CustomerAccount(models.Model):
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    email = models.EmailField(max_length=50,null=True, blank=True)
    mobile=models.BigIntegerField()
    mobile_varify = models.BooleanField(default=False)
    email_varify = models.BooleanField(default=False)
    email_otp = models.IntegerField(null=True, blank=True)
    mobile_otp = models.IntegerField(null=True, blank=True)
    password = models.CharField(max_length=150,editable=None)
    status = models.SmallIntegerField(choices=STATUS, default=1)
    auth_token = models.CharField(max_length=255,null=True, blank=True,editable=None)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
	    return self.first_name