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

@login_required
def force_update(request):
    #run_xdp_commands("xdp-filter unload eth0")
    #run_xdp_commands("xdp-filter load eth0 -f ipv4 -p deny && xdp-filter port 8000")
    all_ips = UserSettings.objects.all()
    ip_list = []
    for ip in all_ips:
        for i in ip.allowed_ip:
            run_xdp_commands(f"xdp-filter ip {i}")

    return JsonResponse({"message": "XDP filter updated successfully"})

