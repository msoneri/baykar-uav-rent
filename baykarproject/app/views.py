from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
import requests

@login_required(login_url='/login/')
def index(request):
    
    return render(request, 'app/index.html')

# staff and user login 
def login_view(request):
    if request.user.is_authenticated:
        return redirect('app:index')  
    return render(request, 'app/registration/login.html')


# def admin_login(request):
#     if request.user.is_authenticated:
#         if request.user.is_staff:
#             return redirect('app:uavs-list')  
#         else:
#             return redirect('app:user-rented-uav')
#     return render(request, 'app/registration/admin-login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('app:index')  
    return render(request, 'app/registration/register.html')

@login_required(login_url='/login/')
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('app:login')
    return redirect('app:index')

@staff_member_required(login_url='/login/')
def uav_list_view(request):
    return render(request, 'app/uav-list.html')

@login_required(login_url='/login/')
def rent_uav_view(request):
    return render(request, 'app/uav-rent.html')

@login_required(login_url='/login/')
def uav_rental_list(request):
    return render(request, 'app/uav-rental-list.html')