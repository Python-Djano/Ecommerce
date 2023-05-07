
from django.shortcuts import render, redirect, HttpResponse
from .forms import RegisterationForm
from accounts.models import Account
from django.contrib import messages
from django.contrib import auth
from carts.views import _cart_id
from carts.models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Create your views here.
def register(request):
    if request.method == "POST":
            form = RegisterationForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone_number = form.cleaned_data['phone_number']
                password = form.cleaned_data['password']
                username = email.split('@')[0]
                user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password, username=username)
                user.phone_number = phone_number
                user.save()

                # user activation
                current_site = get_current_site(request)
                print(current_site)
                mail_subject = "Please avtivate your account"
                message = render_to_string('accounts/account_verifiaction_email.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()
                return redirect('/accounts/login/?command=verification&email='+email)


    else:
        form = RegisterationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/registeration.html', context)


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try: 
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_item_exists = CartItem.objects.filter(cart=cart).exists()

                if cart_item_exists:
                    cart_items = CartItem.objects.filter(cart=cart)
                    for item in cart_items:
                        item.user = user
                        item.save()
            except:
                pass    
            auth.login(request, user)
            messages.success(request, "you are logged in successfully")
            return redirect('dashboard')
    
        else:
            messages.error(request, 'invalid credintials')
            return redirect('login')

    return render(request, 'accounts/login.html')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, OverflowError,  ValueError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'your account is activated')
        return redirect('login')
    else:
        messages.error(request, 'invalid activation link')
        return redirect('register')      





def forgotPassword(request):
    if request.method =="POST":
        email =request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # reset password email
            current_site = get_current_site(request)
            mail_subject = "Reset Your Password"
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'password reset link has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, "user with this email doesnot exist")
            return redirect('forgotPassword')


    return render(request, 'accounts/forgot_password.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token): 
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')

    else:
        messages.error(request, 'this link has been expired')
        return redirect('forgotPassword')


def resetPassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "you have successfully reset your password")
            return redirect('login')

        else:
            messages.error(request, 'passwords doesnot match')
            return redirect('resetPassword')
            
    return render(request, 'accounts/resetPassword.html')



@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')



@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, "you are logged out successfully")
    return redirect('login')