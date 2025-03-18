from django.contrib import admin
from .models import userData,ContactUs,VendorReg,ServiceDetail,profileView,Checkout

admin.site.register(userData)
admin.site.register(ContactUs)
admin.site.register(VendorReg)
admin.site.register(ServiceDetail)
admin.site.register(profileView)
admin.site.register(Checkout)