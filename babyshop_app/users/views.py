from django.shortcuts import redirect, render
from . forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

def user_register(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your account has been created, you can now log in')
            return redirect('login')
    else:
        form=RegisterForm()

    return render(request,'register.html',{'form':form})
def user_login(request):
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user= authenticate(request,username=username,password=password)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return redirect('/')
                else:
                    messages.info(request,'This account is not active')
            else:
                messages.info(request,'Please check your username and password')

    else:
        form=LoginForm()
    return render(request,'login.html',{'form':form})

def user_logout(request):
    logout(request)
    return redirect('/')
