# home/views.py
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from home.models import FlowData, FirewallStatus, Settings, UserSettings
from home.helpers import *
import subprocess
import sys
import os
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from home.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib import messages

## login functions ##
def login_page(request):
    # if already logged in
    if request.user.is_authenticated:
        return redirect('/')
    else:
        return render(request, 'main/login.html')

def check_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            settings = UserSettings.objects.filter(user=user).first()
            if not settings:
                settings = UserSettings(user=user,allowed_ip=[],current_ip="", allowed_port=[])
                settings.save()
            
            ip = get_client_ip(request)
            settings.current_ip = ip
            settings.save()
            run_xdp_commands(f"xdp-filter ip {ip} -m src,dst")

                
            messages.success(request, "Successfully logged in!")
            return redirect('/')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('/login')
    else:
        return redirect('/login')

def logout_func(request):
    logout(request)
    return redirect('/login')
    
    