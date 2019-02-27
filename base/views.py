from django.shortcuts import render
from django import forms
from user.models import User
from user.forms import SignUpForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse


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
#                return HttpResponseRedirect('/user/user_page')
                return HttpResponseRedirect(reverse('user_page'))
            else:
                raise forms.ValidationError('This email already exists')
    else:
        form = SignUpForm()
    return render(request, 'base/sign_up.html', {'form': form})


def sign_in(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        login(request, user)
        return HttpResponseRedirect(reverse('user_page'))
    return render(request, 'base/sign_in.html', {})


def user_page(request):
    return render(request, 'base/user_page.html', {})
