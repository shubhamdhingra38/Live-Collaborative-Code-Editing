from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from . import forms
from django.contrib.auth import authenticate, login as django_login, logout as django_logout




def login(request):
    errors = []
    if request.method == 'POST':
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print('successfully auth')
            django_login(request, user)
            return redirect('/chat')
        else:
            print('unsucessful login')
            errors.append("Invalid login details")
    return render(request, 'login.html', {'errors': errors})

def register(request):
    if request.method == 'POST':
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            print("valid form")
            form.save()
            return redirect('/auth/login')
        else:
            print("invalid form")
    else:
        form = forms.CreateUserForm()
    return render(request, 'register.html', {'form': form})

def logout(request):
    django_logout(request)
    return redirect('/chat', {'success': "Logged out successfully"})