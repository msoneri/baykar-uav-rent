from django.shortcuts import render

def login(request):
    return render(request, 'app/registration/login.html')

def register(request):
    return render(request, 'app/registration/register.html')