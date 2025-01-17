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
from django.http import JsonResponse

@login_required
def xdp_settings(request):
    return render(request, 'main/xdp.html')

def force_update(request):
    run_xdp_commands("xdp-filter unload eth0")
    rsp = run_xdp_commands("xdp-filter load eth0 -f ipv4,tcp -p deny")
    #rsp = run_xdp_commands("xdp-filter port 8000")

    all_ips = UserSettings.objects.all()
    ip_list = []
    for ip in all_ips:
        run_xdp_commands(f"xdp-filter ip {ip.current_ip} -m src,dst")
        for i in ip.allowed_ip:
            run_xdp_commands(f"xdp-filter ip {i} -m src,dst")

    #rsp = run_xdp_commands("xdp-filter port 22")
    #rsp = run_xdp_commands("xdp-filter port 80")
    
    return JsonResponse({"message": "XDP filter updated successfully"})

@login_required
def xdp_status(request):
    status = run_xdp_commands("xdp-filter status")
    print(status)
    return JsonResponse(status)

@login_required
def xdp_dump(request):
    status = run_xdp_commands("xdp-filter poll")
    return JsonResponse(status)

@login_required
def start_xdp(request):
    rsp = run_xdp_commands("xdp-filter load eth0 -f ipv4,tcp -p deny")
    #rsp = run_xdp_commands("xdp-filter port 8000")
    #rsp = run_xdp_commands("xdp-filter port 22")
    return JsonResponse(rsp)

@login_required
def stop_xdp(request):
    rsp = run_xdp_commands("xdp-filter unload eth0")
    return JsonResponse(rsp)

