from django.shortcuts import render,HttpResponse,redirect
from django.http import HttpResponseBadRequest
from .models import CustomUser,Ad
from django.contrib import messages
from django.contrib.auth import authenticate,  login as auth_login
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required

def index(request):
    data={
        'title':'Home Page'
    }
    return render(request, 'index.html',data)

def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        login=authenticate(request,email=email,password=password)
        if login is not None:
            auth_login(request,login)
            messages.success(request,"Signup successful. You can now log in.")
            return redirect('index')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
    return render(request,'login.html')

def signup(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        if pass1 != pass2:
            return HttpResponseBadRequest("Passwords do not match.") 
        hashed_password = make_password(pass1)
        user=CustomUser()
        user.name=username
        user.email=email
        user.password=hashed_password
        user.save()
        messages.success(request,"Signup successful. You can now log in.")
        return redirect('login')
        
    return render(request, 'signup.html')

def forgot_pass(request):
    if request.method=='POST':
        email=request.POST.get('email')
        user=CustomUser.objects.filter(email=email).first()
        if user:
            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(f'/reset_password/{uid}/{token}/')
            
            subject = 'Password Reset Request'
            message =f' Your reset password link {reset_link} '
            
            
            email_from = settings.EMAIL_HOST_USER
            email_message = EmailMessage(
                subject=subject,
                body=message,
                from_email=email_from,
                to=[email]
            )
            email_message.send(fail_silently=False)
            
            return render(request, 'msg_reset.html', {'message': 'Check your email for the password reset link.'})
        else:
            messages.error(request, 'Email address not found.')
        
        return redirect('forgot')
    
    return render(request,'forgot-password.html')

User = get_user_model()
def update_pass(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            
            form = SetPasswordForm(user, request.POST)
            print("========================")
            print(form)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been updated successfully.')
                return redirect('login')
            else:
                messages.error(request, 'The form data is invalid. Please correct the errors below.')
        else:
            form = SetPasswordForm(user)
        return render(request, "update_reset.html", {'form': form, 'uid': uidb64, 'token': token})
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return redirect('forgot')
from .models import ClassifiedAd
@login_required
def post_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        
        if not title or not description or not price or not category:
            messages.error(request, "All fields are required.")
            return redirect('post_add')
        
        # Create and save the ClassifiedAd instance
        classified_ad = ClassifiedAd(
            title=title,
            description=description,
            price=price,
            category=category,
            user=request.user  # Associate ad with the logged-in user
        )
         
        if image:
            file_name = default_storage.save(image.name, ContentFile(image.read()))
            classified_ad.image = file_name
        
        classified_ad.save()
        
        messages.success(request, "Ad posted successfully!")
        return redirect('success_post') 
    return render(request,"post-ads.html")

def succes_post(request):
    
    return render(request,"posting-success.html")

def msg(request):
    return render(request,"msg_reset.html")

def resetreturnhome(request):
    return render(request,"pass_reset_return_home.html")

def category_prodect(request):
    Ads=ClassifiedAd.objects.all()
    print("===========")
    print(Ad)
    return render(request,'category.html',{'Ads':Ads})

    






