from django.shortcuts import render, redirect
from django.http import HttpResponse
from core.models import User, DataBase
from core.forms import LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


# Create your views here.


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():             
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            try:
                user = User.objects.get(email=email)
            except:
                return HttpResponse("User doesn't exist") 
            if user.password != password:
                return HttpResponse("Incorrect password") 
            user.is_active=True
            user.save()                 
            login(request, user)                                             
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def home(request):    
    dbs = request.user.dbs.all()
    return render(request, 'home.html',{'dbs':dbs, 'user':request.user})