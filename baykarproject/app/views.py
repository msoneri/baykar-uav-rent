from django.shortcuts import render, redirect

def index(request):
    return render(request, 'app/navbar.html')

def login(request):
    return render(request, 'app/registration/login.html')

def register(request):
    if request.user.is_authenticated:
        return redirect('app:index')  
    return render(request, 'app/registration/register.html')