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
            
            detect_ip    = False if "detect_ip" not in request.POST else True
            ips      = [] if 'allowed_ips' not in request.POST else request.POST['allowed_ips'].split('\r\n')
            ports    = [] if 'allowed_ports' not in request.POST else request.POST['allowed_ports'].split('\r\n')
            # change ports from array to json
            
            user = User.objects.create_user(username, email, password)
            settings = UserSettings.objects.create(user=user, allowed_ip=ips, allowed_port=ports, detect_ip=detect_ip)
            user.save()
            settings.save()
            for ip in ips:
                if ip != '':
                    run_xdp_commands(f"xdp-filter ip {ip}")
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
        for ip in settings.allowed_ip:
            run_xdp_commands(f"xdp-filter ip {ip} -r")
        
        ips      = [] if 'allowed_ips' not in request.POST else request.POST['allowed_ips'].split('\r\n')
        ports    = [] if 'allowed_ports' not in request.POST else request.POST['allowed_ports'].split('\r\n')
        detect_ip    = False if "detect_ip" not in request.POST else True
        
        settings.allowed_ip   = ips
        settings.allowed_port = ports
        settings.detect_ip    = detect_ip
        
        settings.save()
        
        for ip in ips:
            if ip != '':
                run_xdp_commands(f"xdp-filter ip {ip}") 
        messages.success(request, "User updated successfully")
        return redirect(request.META.get('HTTP_REFERER'))
        
    else:
        redirect('users')
        
@login_required
def delete_user(request,id):
    if request.method == 'GET':
        user_id = id
        user = User.objects.get(id=user_id)
        
        if user.is_superuser:
            messages.error(request, "Cannot delete superuser")
            return redirect(request.META.get('HTTP_REFERER'))
        
        settings = UserSettings.objects.get(user=user)
        for ip in settings.allowed_ip:
            run_xdp_commands(f"xdp-filter ip {ip} -r")
        user.delete()
        settings.delete()
        messages.success(request, "User deleted successfully")
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        redirect('users')
    
