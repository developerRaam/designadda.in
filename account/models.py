from django.db import models

# Create your models here.
class CustomerAccount(models.Model):
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    mobile=models.IntegerField()
    country = models.CharField(max_length=50,null=True, blank=True)
    state=models.CharField(max_length=50, null=True, blank=True)
    city=models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50,null=True, blank=True)
    password=models.CharField(max_length=150)
    
    Status = {
        ('Active','Active'),
        ('Deactive','Deactive'),
    }
    email_status = models.CharField(max_length=10, choices=Status, default='Deactive')
    status = models.CharField(max_length=10, choices=Status, default="Active")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    

    def __str__(self):
	    return self.first_name