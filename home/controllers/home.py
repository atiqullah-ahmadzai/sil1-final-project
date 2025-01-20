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
def home(request):
    interfaces = get_interfaces()
    return render(request, 'main/index.html', {'interfaces': interfaces})

@login_required
@api_view(['GET', 'POST'])
def post_flow(request):
    if request.method == 'POST':
        data = request.data
        prediction = predict_traffic(data)
        if prediction == 'DDoS':
            if not FirewallStatus.objects.filter(ip=data['src_ip']).exists():
                FirewallStatus.objects.create(ip=data['src_ip'], status='Blocked')
            
        flow_data = FlowData.objects.create(name='Flow Data', data=data, prediction=prediction)
        return Response({"message": "Got some data!", "prediction": prediction})
    else:
        return Response({"message": "Got some data!"})

@login_required
@api_view(['POST'])
def start_interface(request):
    interface  = request.data.get('interface')
    model_name = request.data.get('model_name')
    
    process   = start_cicflowmeter(interface)

    create_config('interface',interface)
    create_config('cic_status',True)
    create_config('model_name',model_name)
    
    return Response({"message": "Monitoring has started started!"})

@login_required
@api_view(['GET'])
def clear_db(request):
    FlowData.objects.all().delete()
    return Response({"message": "Database is cleared!"})

@login_required
@api_view(['GET'])
def stop_interface(request):
    
    stop_cicflowmeter()

    create_config('cic_status',False)
    
    return Response({"message": "cicflowmeter has been stopped!"})

@login_required
@api_view(['GET'])
def get_data(request):
    
    # get limit from url
    if 'num_records' in request.GET:
        rows_limit = int(request.GET['num_records'])
        if rows_limit == 0:
            rows_limit = 50
        if rows_limit == 1:
            rows_limit = 5000
    else:
        rows_limit = 50
    
    data = FlowData.objects.all().values('id','data', 'prediction').order_by('-id')[:rows_limit]
    blocked = FirewallStatus.objects.all().values('id','ip', 'status').order_by('-id')[:rows_limit]
    
    graphs   = {}
    graphs["graph_1"]      = get_records_per_minute()
    graphs["graph_2"]      = get_label_count()
    
    settings = {}
    settings["cic_status"] = check_cic_process()
    settings["interface"]  = get_config('interface')
    settings["model_name"] = get_config('model_name')
    settings["current_ip"] = request.user.usersettings.current_ip
    
    rsp = {}
    rsp["data"]     = list(data)
    rsp["graphs"]   = graphs
    rsp["settings"] = settings
    rsp["blocked"]  = list(blocked)
    

    return Response(rsp)

