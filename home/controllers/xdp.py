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

@login_required
def xdp_settings(request):
    return render(request, 'main/xdp.html')

