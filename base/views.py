import hashlib
import random
from datetime import timedelta, datetime, timezone
from django.shortcuts import render
from django import forms
from user.models import User, LoginToken
from user.forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail


def home(request):
    return render(request, 'base/home.html', {})


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            email = userObj['email']
            password = userObj['password']
            if not User.objects.filter(email=email).exists():
                form.save()
                user = authenticate(email=email, password=password)
                login(request, user)
                return HttpResponseRedirect(reverse('user_page'))
            else:
                raise forms.ValidationError('This email already exists')
    else:
        form = SignUpForm()
    return render(request, 'base/sign_up.html', {'form': form})


def sign_in(request):
    context = {}
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('user_page'))
        else:
            context['errors'] = 'Sorry, that user does not exists'
    return render(request, 'base/sign_in.html', context)


def logout_user(request):
    logout(request)
    return render(request, 'base/logout_user.html', {})


def user_page(request):
    return render(request, 'base/user_page.html', {})


def create_magic_link(request):
    context = {}
    if request.method == 'POST':
        email = request.POST['email']
        if not User.objects.filter(email=email).exists():
            context['error'] = 'User not registered, please go to \
                                the Sign-Up Page'
        else:
            salt = hashlib.sha1(str(random.random()).encode(
                    'utf-8')).hexdigest()[:5]
            token_id = hashlib.sha1(str(
                        salt+email).encode('utf-8')).hexdigest()
            expiration = datetime.now(timezone.utc) + timedelta(hours=1)
            login_token = LoginToken(email=email, token_id=token_id,
                                     token_expires=expiration)
            login_token.save()
            home = 'http://127.0.0.1:8000'
            email_body = 'Hello {}, Please click this link to login: {}{}' \
                         .format(email, home, login_token.get_absolute_url())

            send_mail('Magic Link', email_body, 'mymail@mail.es',
                      [email], fail_silently=True)
            context['success'] = 'Check your inbox!'
    return render(request, 'base/magic_link.html', context)


def magic_login_confirm(request, activation_key):
    context = {}
    if request.user.is_authenticated:
        HttpResponseRedirect(reverse('user_page'))
    try:
        login_token = LoginToken.objects.get(token_id=activation_key)
        if login_token.token_expires < datetime.now(timezone.utc):
            context['error'] = 'This token has expired.'
        elif login_token.is_used:
            context['error'] = 'This token has already been used.'
        else:
            login_token.is_used = True
            login_token.save()
            user = User.objects.get(email=login_token.email)
            login(request, user)
            return HttpResponseRedirect(reverse('user_page'))
    except LoginToken.DoesNotExist:
        context['error'] = 'This token does not exist.'
    return render(request, 'base/magic_link_confirm.html', context)
