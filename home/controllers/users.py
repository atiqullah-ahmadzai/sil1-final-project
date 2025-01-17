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

## Users Page Functions ##
@login_required
def users(request):

    users = UserSettings.objects.all()
    return render(request, 'main/users.html', {'users': users})

@login_required
def create_user(request):
    if request.method == 'POST':
        check = User.objects.filter(username=request.POST['email']).exists()
        if check:
            messages.error(request, "Username already exists")
            return redirect(request.META.get('HTTP_REFERER'))
        
        else:
            username = request.POST['email']
            password = request.POST['password']
            email    = request.POST['email']
            
            ips      = [] if 'allowed_ips' not in request.POST else request.POST['allowed_ips'].split('\r\n')
            ports    = [] if 'allowed_ports' not in request.POST else request.POST['allowed_ports'].split('\r\n')
            # change ports from array to json
            
            user = User.objects.create_user(username, email, password)
            settings = UserSettings.objects.create(user=user, allowed_ip=ips, allowed_port=ports)
            user.save()
            settings.save()
             
            messages.success(request, "User created successfully")
            return redirect(request.META.get('HTTP_REFERER'))
        
    else:
        redirect('users')

@login_required
def update_user(request):
    if request.method == 'POST':
        user_id  = request.POST['id']
        password = request.POST['password']
        user = User.objects.get(id=user_id)
        
        if password != '':
            user = User.objects.get(id=user_id)
            user.set_password(password)
            user.save()
        
        
        settings = UserSettings.objects.get(user=user)
        
        ips      = [] if 'allowed_ips' not in request.POST else request.POST['allowed_ips'].split('\r\n')
        ports    = [] if 'allowed_ports' not in request.POST else request.POST['allowed_ports'].split('\r\n')
        
        settings.allowed_ip   = ips
        settings.allowed_port = ports
        
        settings.save()
        
        messages.success(request, "User updated successfully")
        return redirect(request.META.get('HTTP_REFERER'))
        
    else:
        redirect('users')
    
