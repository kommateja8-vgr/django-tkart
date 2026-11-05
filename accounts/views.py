from django.shortcuts import render, redirect
from accounts.forms import RegistrationForm
from .models import Account

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required

# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# ========================= USER REGISTRATION =========================

def register(request):

    if request.method == 'POST':

        form = RegistrationForm(request.POST)

        if form.is_valid():  

            first_name      = form.cleaned_data['first_name']
            last_name       = form.cleaned_data['last_name']
            email           = form.cleaned_data['email']
            phone_number    = form.cleaned_data['phone_number']
            password        = form.cleaned_data['password']

            username        = email.split('@')[0]

            # Create user account
            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password
            )

            user.phone_number = phone_number
            user.save()


            messages.success(
                request,
                'Registration successful!'
            )

            return redirect('register')

        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }

    return render(request, 'accounts/register.html', context)


# ========================= USER LOGIN =========================

def login(request):

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(
            request,
            email=email,
            password=password
        )

        if user is not None:

            auth.login(request, user)

            messages.success(request, 'You are now logged in.')

            return redirect('dashboard')

        else:

            messages.error(request, 'Invalid login credentials.')

            return redirect('login')

    return render(request, 'accounts/login.html')


# ========================= USER LOGOUT =========================

@login_required(login_url='login')
def logout(request):

    auth.logout(request)

    messages.success(request, 'You are logged out.')

    return redirect('login')



@login_required(login_url='login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')


def forgotPassword(request):
    return render(request,'accounts/forgotPassword.html')