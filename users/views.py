from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import authenticate,login
from django.contrib import messages
# Create your views here.


def user_register(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        user_email = request.POST['user_email']
        user_password = request.POST['user_password']
        user_confirm_password = request.POST['user_confirm_password']
        if user_password != user_confirm_password:
            messages.error(request,"Password and Confirm password should be equal")
            return redirect("home")
        elif user_name and user_email and user_password and user_password and user_confirm_password:
            if User.objects.filter(username=user_name).exists():
                messages.error(request,"Username already exists.")
                return redirect("home")
            elif User.objects.filter(email=user_email).exists():
                messages.error(request,"Email already exists.")
                return redirect("home")
            else:
                user = User.objects.create_user(username=user_name,email=user_email,password=user_password)
                user.save()
                messages.success(request,"User successfully created.")
                return redirect('home')
        elif len(user_password) < 8:
            messages.error(request,"Password must be greater than 8 characters")
            return redirect('home')

def user_login(request):
    if request.method == 'POST':
        user_name = request.POST['user_name']
        user_password = request.POST['user_password']
        print(user_name,user_password)
        user = authenticate(username=user_name,password=user_password)
        if user is not None:
            login(request,user)
            
            return redirect('home')
        else:
            messages.error(request,'Invalid Credentials')
            redirect('home')
    return redirect("home")

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Successfully Logged out from the account")
        return redirect("home")






# def object_details(request,id):

# 	obj = get_object_or_404(Post,id=id)
# 	viewed_by_session_count(request,obj)
# 	return redirect('/')


