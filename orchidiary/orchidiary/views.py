from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm

from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse

from .forms import SignupForm

def homepage(request):
    return render(request, "index.html")

def signup(request):
    if request.method == "GET":
        form = SignupForm()
    else:
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.is_active=True
            login(request, user)
            return HttpResponseRedirect(reverse('homepage'))

    context = {
        'form':form,
    }

    return render(request, "auth/signup.html", context=context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))

def orchids_sections_view(request):
    return render(request, "orchids.html")

def login_view(request:HttpRequest):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            login(request, user)
            redirect_url = request.get_full_path().split("?next=")[1]
            return HttpResponseRedirect(redirect_url)
    else:
        form = AuthenticationForm()
    return render(request, "auth/login.html", context={'form':form})