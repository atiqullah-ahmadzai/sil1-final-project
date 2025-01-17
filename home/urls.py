# home/urls.py
from django.urls import path
from . import views
from django.shortcuts import redirect

def check_login(request):
    if not request.user.is_authenticated:
        return redirect('login') 

urlpatterns = [
    path('', views.home, name='home'),
    
    path('login', views.login_page, name='login_page'),
    path('check_login', views.check_login, name='check_login'),
    path('logout', views.logout_func, name='logout'),
    
    path('post_flow', views.post_flow, name='post_flow'),
    path('start_interface', views.start_interface, name='start_interface'),
    path('get_data', views.get_data, name='get_data'),
    path('clear_db', views.clear_db, name='clear_db'),
    path('stop_interface', views.stop_interface, name='stop_interface'),
    
    path('users', views.users, name='users'),
    path('users/create', views.create_user, name='create_user'),
    path('users/update', views.update_user, name='update_user'),
    
    
]