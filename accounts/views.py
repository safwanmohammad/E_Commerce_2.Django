from django.shortcuts import render,redirect,HttpResponse
from . forms import RegistretionForm
from . models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# verification_email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import  EmailMessage

# Create your views here.

def  register(request):
    if request.method == 'POST':
        forms = RegistretionForm(request.POST)
        if forms.is_valid():
            first_name  = forms.cleaned_data['first_name']
            last_name  = forms.cleaned_data['last_name']
            phone_number  = forms.cleaned_data['phone_number']
            email  = forms.cleaned_data['email']
            password  = forms.cleaned_data['password']
            username  = email.split('@')[0]
            user  = Account.object.create_user(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email,
            password = password
            )
            user.phone_number = phone_number
            # user.is_active = True
            user.save()
            #email verification
            current_site = get_current_site(request)
            mail_subject = "please activate your account"
            message = render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message, to=[to_email])
            send_email.send()
           # messages.success(request,'Thank you for registering with us.we have send you a verification email to your email address[your email]. please verify it. ')
            urls = reverse('login') + f'?command=verification&email={email}'
            return redirect(urls)
    else:
        forms = RegistretionForm()
    context = {
        'forms':forms,
    }
    return render(request,'accounts/register.html',context)


def  login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(request,email=email,password=password)
        print({user})
        if user is not None:
            auth.login(request,user)
            messages.success(request,'your now loged in')
            return redirect('dashbord')
        else:
            messages.error(request,'invalid email and password ')
            return redirect('login')
        
    return render(request,'accounts/login.html')


@login_required(login_url = 'login')
def  logout(request):
    auth.logout(request)
    messages.success(request,'you are logged Out')
    return redirect('login')

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulations your  account is activated ,')
        return redirect('login')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('register')
    

@login_required(login_url = 'login')
def dashbord(request):
    return render (request, 'accounts/dashbord.html')

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.object.filter(email=email).exists():
            user = Account.object.get(email__exact=email)

            #Rest Password Mail
            current_site = get_current_site(request)
            mail_subject = "Rest your Password"
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message, to=[to_email])
            send_email.send()
            messages.success(request,'password reset email has been send to your email address')
            return redirect('login')
        else:
            messages.error(request,'Account does not exists')
            return redirect('forgotpassword')
    return render(request, 'accounts/forgotpassword.html')

def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request,'Please rest your password')
        return redirect ('resetpassword')   
    else:
        messages.error(request,'This link has been expired !')
        return redirect('login')
    
    
def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.object.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'Password rest successful')
            return redirect('login')
        else:
            messages.error(request,'Password do not match !')
            return redirect('resetpassword')
    else:
        return render(request,'accounts/resetpassword.html')