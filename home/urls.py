# home/urls.py
from django.urls import path
from .controllers import home, auth, users, xdp

from django.shortcuts import redirect

def check_login(request):
    if not request.user.is_authenticated:
        return redirect('login') 

urlpatterns = [
    path('', home.home, name='home'),
    path('post_flow', home.post_flow, name='post_flow'),
    path('start_interface', home.start_interface, name='start_interface'),
    path('get_data', home.get_data, name='get_data'),
    path('clear_db', home.clear_db, name='clear_db'),
    path('stop_interface', home.stop_interface, name='stop_interface'),
    
    path('login', auth.login_page, name='login_page'),
    path('check_login', auth.check_login, name='check_login'),
    path('logout', auth.logout_func, name='logout'),
    
    path('users', users.users, name='users'),
    path('users/create', users.create_user, name='create_user'),
    path('users/update', users.update_user, name='update_user'),
    path('users/delete/<int:id>', users.delete_user, name='delete_user'),
    
    path('xdp/settings', xdp.xdp_settings, name='xdp_settings'),
    path('xdp/force_update', xdp.force_update, name='force_update'),
    path('xdp/status', xdp.xdp_status, name='xdp_status'),
    path('xdp/dump', xdp.xdp_dump, name='xdp_dump'),
    path('xdp/start', xdp.start_xdp, name='start_xdp'),
    path('xdp/stop', xdp.stop_xdp, name='stop_xdp'),
    
    
]