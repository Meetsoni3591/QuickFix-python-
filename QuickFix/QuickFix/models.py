from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class userData(models.Model):
    # user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class ContactUs(models.Model):
    # user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    msg = models.CharField(max_length=100)

class VendorReg(models.Model):

    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class profileView(models.Model):

    # user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    registration_num = models.CharField(max_length=100)
    business_email = models.CharField(max_length=100)
    gst = models.CharField(max_length=100)

class ServiceDetail(models.Model):
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    avilable = models.CharField(max_length=100)
    price = models.IntegerField()
    experience = models.CharField(max_length=100)
    payment_methods = models.CharField(max_length=100)
    desc = models.CharField(max_length=250)
    service_image = models.ImageField(upload_to='static/service_photo/', max_length=250)
    certificate = models.ImageField(upload_to='static/service_photo/', max_length=250)
    email = models.CharField(max_length=100, null=True, blank=True)

    # Use property for dynamic calculation of new price
    @property
    def new_price(self):
        return self.price + (self.price * 0.18)

class Checkout(models.Model):

    # user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    # area = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10, default='')
    address = models.CharField(max_length=255)
    apartment_suite = models.CharField(max_length=255)
    landmark = models.CharField(max_length=100)
    postal_zip = models.CharField(max_length=6)

    # New fields for service details
    service_category = models.CharField(max_length=100)
    service_price = models.DecimalField(max_digits=10, decimal_places=2)
    service_area = models.CharField(max_length=50)
    service_email = models.CharField(max_length=100)

def __str__(self):
    return self.name