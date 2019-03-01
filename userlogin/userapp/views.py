# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from userapp.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request, "userapp/index.html")

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES["profile_pic"]
                profile.save()
                registered=True

            else:
                print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, "userapp/registration.html",{"user_form": user_form, "profile_form": profile_form, "registered": registered})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)

                return HttpResponseRedirect(reverse("index"))

            else:
                return HttpResponse("USER IS NOT ACTIVE")

        else:
            print("username: {} password: {}".format(username, password))
            return HttpResponse("invalid credentials")

    else:
        return render(request, "userapp/login.html", {})

@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect(reverse("index"))