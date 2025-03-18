"""
URL configuration for QuickFix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.load,name='load'),
    path('admin/', admin.site.urls),
    path('login', views.login,name='login'),
    path('verify-mail', views.otp_view,name='verify-mail'),    
    path('verify-otp', views.verify_otp,name='verify-otp'),
    path('reg', views.register,name='register'),
    # Main Website
    path('home-page',views.homePage,name='home-page'),
    path('shop',views.shop,name='shop'),
    path('about-us',views.aboutUs,name='about-us'),
    path('services',views.services,name='services'),
    path('services/<int:service_id>/', views.services, name='book_service'),
    path('checkout',views.checkOut,name='checkout'),
    path('payment',views.Payment,name='payment'),
    path('blog',views.blog,name='blog'),
    path('contact-us',views.contactUs,name='contact-us'),
    path('delete/<int:id>/',views.user_delete,name='user_delete'),
    path('feed_delete/<int:id>/',views.feed_delete,name='feed_delete'),
    
    # Admin Side
    path('admin-dashboard',views.dashBoard,name='admin-dashboard'),
    path('admin-user',views.user_tables,name='admin-user'),
    path('admin-contactus',views.contact_tables,name='admin-contactus'),
    path('admin-vendata',views.venData,name='admin-vendata'),
    path('admin-vendor',views.adminVendor,name='admin-vendor'),
    path('ven_delete/<int:id>/',views.ven_delete,name='ven_delete'),


    # Service Provdier Side
    path('vendor-email',views.vendorEmail,name='vendor-email'),
    path('vendor-otp',views.VendorOtp,name='vendor-otp'),
    path('vendor-signin',views.vendorSignin,name='vendor-signin'),
    path('vendor-signup',views.vendorSignup,name='vendor-signup'),
    path('vendor-dash',views.VendorDash,name='vendor-dash'),
    path('vendor-service',views.vendorService,name='vendor-service'),
    path('vendor-profile',views.vendorProfile,name='vendor-profile'),
    path('vendor-view',views.vendorView,name='vendor-view'),
    path('vendor-terms',views.vendorTerms,name='vendor-terms'),
    path('service_delete/<int:id>/',views.serviceDelete,name='service_delete'),

    #edit
   path('edit-service/<int:service_id>/', views.edit_service, name='edit_service'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)