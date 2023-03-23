from django.db import models

# Create your models here.
STATUS = ((1, 'Active'), (0, 'Deactive'))

class CustomerAccount(models.Model):
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    country = models.CharField(max_length=50,null=True, blank=True)
    state=models.CharField(max_length=50, null=True, blank=True)
    city=models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50,null=True, blank=True)
    mobile=models.BigIntegerField()
    mobile_varify = models.BooleanField(default=False,editable=None)
    email_varify = models.BooleanField(default=False,editable=None)
    password=models.CharField(max_length=150,editable=None)
    status = models.SmallIntegerField(choices=STATUS, default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
	    return self.first_name