from django.shortcuts import render, redirect,get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages  # Import messages
from .forms import EmailForm,ServiceForm
import random
from django.core.files.storage import FileSystemStorage
from QuickFix.models import userData,ContactUs,VendorReg,ServiceDetail,profileView,Checkout

def load(request):
    return render(request, 'Loading_page.html')


def register(request):
    if request.method == 'POST':
        # current_username = request.session[email]
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        data = userData(username=username,email=email,phone=phone,password=password)
        data.save()
        return redirect('home-page')  
    return render(request, 'Register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        request.session['email'] = email
        try:
            user = userData.objects.get(email=email)
            if user.password == password:
                return redirect('home-page')
            else:
                messages.error(request, 'Oops! Password is invalid')
        except userData.DoesNotExist:
             messages.error(request, 'Oops! Email is invalid')
    return render(request, 'Login.html')

    # data = userData.objects.all()
    # return render(request, 'login.html', {'data': data})

def send_otp(email):
    otp = random.randint(100000, 999999)
    subject = 'Your Registration Code' 
    message = f'Your Registration OTP code is {otp}.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return otp

def otp_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Check if the email already exists in the database
            if userData.objects.filter(email=email).exists():  # Assuming you have a User model with an email field
                messages.error(request, 'Alredy Exist')
            else:
                # If the email does not exist, send the OTP
                request.session['email'] = email
                otp = send_otp(email)
                request.session['otp'] = otp
                return redirect('verify-otp')
    else:   
        form = EmailForm()

    return render(request, 'Emailverify.html', {'form': form})


    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.session['email'] = email
            otp = send_otp(email)
            request.session['otp'] = otp
            return redirect('verify-otp')
    else:   
        form = EmailForm()
    return render(request, 'Emailverify.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        otp = ''.join(request.POST.getlist('otp[]'))
        if otp == str(request.session.get('otp')):
            return redirect('register')
        else:
            messages.error(request, 'OTP to Sahi se dal le')
            return redirect('verify-otp')  
    return render(request, 'Otp.html')


# Main website Functions

def homePage(request):
    return render(request, 'Home.html')

def shop(request):
    return render(request, 'Shop.html')

def aboutUs(request):
    return render(request, 'AboutUs.html')

def services(request, service_id=None):
    # Fetch all services
    data = ServiceDetail.objects.all()
    
    # Calculate new prices for each service
    for item in data:
        item.old_price = item.price + (item.price * 0.35)
        # Store new_price in the item for display

   # Check if a service_id is provided for booking
    if service_id is not None:
        # Get the service detail object using the provided service_id
        service = get_object_or_404(ServiceDetail, id=service_id)
        
        # Store relevant service data in the session
        request.session['selected_service'] = {
            'email': service.email,
            'id': service.id, 
            'category': service.category,
            'desc': service.desc,
            'avilable': service.avilable,
            'area': service.area,
            'price': service.new_price  # Assuming this is your new price logic
        }
        return redirect('checkout')


    return render(request, 'Services.html', {'data': data})

def checkOut(request):

    selected_service = request.session.get('selected_service', {})

    if request.method == 'POST':
        # Populate the Checkout model with both form and service data
        checkout = Checkout(
            first_name=request.POST.get('c_fname'),
            last_name=request.POST.get('c_lname'),
            address=request.POST.get('c_address'),
            apartment_suite=request.POST.get('c_apartment'),
            landmark=request.POST.get('c_state_country'),
            postal_zip=request.POST.get('c_postal_zip'),
            email=request.POST.get('c_email_address'),
            phone=request.POST.get('c_phone'),
            # area=request.POST.get('area'),
            
            # Service details from session
            service_category=selected_service.get('category'),
            service_price=selected_service.get('price'),
            service_area=selected_service.get('area'),
            service_email=selected_service.get('email'),
        )
        checkout.save()

        # Store checkout ID in session for later reference in payment step
        request.session['checkout_id'] = checkout.id

        # Redirect to payment interface
        return redirect('payment')

    return render(request, 'Checkout.html', {'selected_service': selected_service})

def create_order(request):
    """Create a Razorpay order"""
    if request.method == "POST":
        data = json.loads(request.body)
        amount = data.get("amount")  # Amount in paise (e.g., 100 INR = 10000 paise)
        currency = "INR"

        # Create an order
        razorpay_order = razorpay_client.order.create({
            "amount": amount,
            "currency": currency,
            "payment_capture": 1  # Auto-capture payment
        })

        return JsonResponse({
            "order_id": razorpay_order["id"],
            "key": settings.RAZORPAY_KEY_ID,
            "amount": amount,
            "currency": currency
        })
    
def handle_payment_callback(request):
    """Handle Razorpay payment callbacks"""
    if request.method == "POST":
        payload = json.loads(request.body)
        try:
            # Verify payment signature
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': payload.get('razorpay_order_id'),
                'razorpay_payment_id': payload.get('razorpay_payment_id'),
                'razorpay_signature': payload.get('razorpay_signature')
            })

            return HttpResponse("Payment verified successfully!", status=200)
        except razorpay.errors.SignatureVerificationError:
            return HttpResponse("Payment verification failed!", status=400)

def Payment(request):
    return render(request, 'Payment.html')

def blog(request):
    return render(request, 'Blog.html')

def contactUs(request):
    if request.method == 'POST':
        # current_username = request.session[email]
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        msg = request.POST.get('msg')
        data = ContactUs(fname=fname,lname=lname,email=email,msg=msg)
        data.save()
        return redirect('contact-us')  
    return render(request, 'ContactUs.html')

    # data = userData.objects.all()
    # return render(request, 'ContactUs.html', {'data': data})

def user_delete(request,id):
    demo = get_object_or_404(userData, id=id)
    demo.delete()
    return redirect('admin-user')

def feed_delete(request,id):
    demo = get_object_or_404(ContactUs, id=id)
    demo.delete()
    return redirect('admin-contactus')

def cart(request):
    return render(request, 'Cart.html')



# admin site Functions

def dashBoard(request):
    user_count = userData.objects.count()  # Count of registered users
    vendor_count = VendorReg.objects.count()  # Count of vender 
    service_count = ServiceDetail.objects.count()  # Count of services
    feedback_count = ContactUs.objects.count()  # Count of feedback entries  

    context = {
        'user_count': user_count,
        'vendor_count': vendor_count,
        'service_count': service_count,
        'feedback_count': feedback_count,
        'data':Checkout.objects.all(),
    }
    
    return render(request, 'Admin_Dashboard.html',context)
                                                                                                                
def user_tables(request):
    data = userData.objects.all()
    return render(request, 'Admin_User.html', {'data': data})

def contact_tables(request):
    data1 = ContactUs.objects.all()
    return render(request, 'Admin_Contact.html', {'data1' : data1})

def adminVendor(request):
    data = ServiceDetail.objects.all()
    return render(request, 'Admin_Vendor.html', {'data' : data})

def venData(request):
    data = VendorReg.objects.all()
    return render(request, 'Admin_Vendor_Data.html', {'data' : data})

def ven_delete(request,id):
    demo = get_object_or_404(VendorReg, id=id)
    demo.delete()
    return redirect('admin-vendata')
# Vendor 

def vendorSignin(request):
    if request.method == 'POST':
        user_id = request.user.id
        email = request.POST.get('email')
        password = request.POST.get('password')
        request.session['email'] = email

        try:
            user = VendorReg.objects.get(email=email)
            if user.password == password:
                request.session['username'] = user.username
                return redirect('vendor-dash')
            else:
                messages.error(request, 'Oops! Password is invalid')
        except VendorReg.DoesNotExist:
            messages.error(request, 'Oops! Email is invalid')
    return render(request, 'Vendor_Signin.html')

def vendorSignup(request):
    if request.method == 'POST':
        # current_username = request.session[email]
        user_id = request.user.id
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        request.session['username'] = username

        data = VendorReg(username=username,email=email,phone=phone,password=password)
        data.save()
        return redirect('vendor-dash')  
    return render(request, 'Vendor_Signup.html')

def vendorEmail(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Check if the email already exists in the database
            if VendorReg.objects.filter(email=email).exists():  # Assuming you have a User model with an email field
                messages.error(request, 'Already Exist')
            else:
                # If the email does not exist, send the OTP
                request.session['email'] = email
                otp = send_otp(email)
                request.session['otp'] = otp
                return redirect('verify-otp')
    else:   
        form = EmailForm()

    return render(request, 'VendorEmailVeirfy.html', {'form': form})


def VendorOtp(request):
    if request.method == 'POST':
        otp = ''.join(request.POST.getlist('otp[]'))
        if otp == str(request.session.get('otp')):
            return redirect('vendor-signup')
        else:
            messages.error(request, 'OTP to Sahi se dal le')
            return redirect('vendor-otp')  
    return render(request, 'VendorOtp.html')

def VendorDash(request):
    # Fetch the username from the session
    username = request.session.get('username', 'Guest')  # Default to 'Guest' if no username in session
    
    # Filter the Checkout data based on the session email
    session_email = request.session.get('email', None)  # Get session email
    if session_email:
        data = Checkout.objects.filter(service_email=session_email)  # Filter Checkout entries where email matches session email
    else:
        data = Checkout.objects.none()  # Return an empty queryset if no session email
    
    return render(request, 'VendorDash.html', {
        'data': data,
        'username': username,  # Pass the username to the template
    })



def vendorService(request):
    is_certificate_uploaded = False
    certificate_name = None
    service_detail = None

    # Retrieve email from session
    email = request.session.get('email')
    
    # Retrieve all service details for the given email
    service_details = ServiceDetail.objects.filter(email=email)

    if service_details.exists():
        service_detail = service_details.first()  # Get the first matching object
        certificate_name = service_detail.certificate
        if certificate_name:
            is_certificate_uploaded = True
    
    if request.method == 'POST':
        category = request.POST['category']
        area = request.POST['area']
        available = request.POST['availability']
        price = request.POST['price']
        experience = request.POST['experience']
        payment_methods = request.POST.getlist('payment_method')
        desc = request.POST['desc']

           # Define and check if files are uploaded
        service_image = request.FILES.get('service_image')
        certificate = request.FILES.get('certificate')
        
        fs = FileSystemStorage()

        # Initialize file names
        service_image_name = None
        certificate_name = None

        # Save uploaded files if present
        if service_image:
            service_image_name = fs.save(service_image.name, service_image)

        if certificate:
            is_certificate_uploaded = True
            certificate_name = fs.save(certificate.name, certificate)   
        
        # Convert payment_methods list to a comma-separated string (or JSON)
        payment_methods_str = ', '.join(payment_methods)

        # Insert data into the model
        service_detail = ServiceDetail(
            category=category,
            area=area,
            avilable=available,
            price=price,
            experience=experience,
            payment_methods=payment_methods_str,
            desc=desc,
            service_image=service_image_name,
            certificate=certificate_name,
            email=email
        )
        service_detail.save()

        return redirect('vendor-view')  # Replace with the actual URL or view name

    return render(request, 'vendorService.html',{'is_certificate_uploaded': is_certificate_uploaded})

def vendorProfile(request):
    email = request.session.get('email')

    # Get the user data based on email
    user = VendorReg.objects.filter(email=email).first()  # Use .first() to get single user object
    
    # If form is submitted
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        address = request.POST.get('address')
        registration_num = request.POST.get('registration_num')
        business_email = request.POST.get('business_email')
        gst = request.POST.get('gst')

        # Saving the data to the database
        saveData = profileView(
            fname=fname,
            lname=lname,
            address=address,
            registration_num=registration_num,
            business_email=business_email,
            gst=gst,
        )
        saveData.save()
        return redirect('vendor-profile')  # Redirect to the same page to avoid resubmission

    # Render the template with the user data
    # data = profileView.objects.filter(email=email).first() 
    # return render(request, 'VenderProfile.html', {'data':data})
    
    return render(request, 'VenderProfile.html',{'user':user})


def vendorView(request):
    email = request.session.get('email')
    data = ServiceDetail.objects.filter(email=email)
    return render(request, 'VendorServiceView.html', {'data': data})

def serviceDelete(request,id):
    delete_data = get_object_or_404(ServiceDetail, id=id)
    delete_data.delete()
    return redirect('vendor-view')

def vendorTerms(request):
    return render(request, 'T&C_V.html')

#Edit 
def edit_service(request, service_id):

    service = get_object_or_404(ServiceDetail, id=service_id)

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            print("Form is valid")  # Debugging line
            form.save()
            return redirect('vendor-view')  # Redirect to the view services page upon success
        else:
            print("Form errors:", form.errors)  # Debugging line to print form errors
    else:
        form = ServiceForm(instance=service)

    # Check if certificate is uploaded
    is_certificate_uploaded = service.certificate is not None

    context = {
        'form': form,
        'is_certificate_uploaded': is_certificate_uploaded,
        'service': service  # Pass service object for further use if needed
    }
    return render(request, 'edit_service.html', context)
