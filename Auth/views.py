from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse

from .models import User
from .forms import RegistrationForm

# Create your views here.

class Auth:
    
    def login(request):
        if request.method == "POST":
            
            username_login = request.POST['username']
            password_login = request.POST['password']
            
            user = authenticate(request, username=username_login, password=password_login)
            
            if user is not None:
                print('kesini')
                login(request, user)
                return redirect('/')
            else:
                print('kesini')
                return redirect('/login')
        # logout(request)
        return render(request, 'auth/loginv2.html')
    def logout(request):
        if request.method == "POST":
            if request.POST["logout"] == "Submit":
                logout(request)
                return redirect('/login')
        return redirect('/login')

