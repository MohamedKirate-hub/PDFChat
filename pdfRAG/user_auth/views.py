from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from user_auth.forms import RegisterForm

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return redirect('home')

def login_view(request):
    form = AuthenticationForm(request)
    page = 'login'
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')

    context = {'page': page, 'form': form}
    return render(request, 'login_register.html', context)

def register_view(request):
    form = RegisterForm()
    page = 'register'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    context = {'page': page, 'form': form}
    return render(request, 'login_register.html', context)
