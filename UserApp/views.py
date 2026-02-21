from django.shortcuts import render,redirect
from UserApp.models import *
from AdminApp.models import *
from Owner_App.views import *
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


# Create your views here.
def home(request):
    cat=CategoryDb.objects.all()
    return render(request,"Home.html",{"cat":cat})

def user_signup(request):
    return render(request,"User_Signup.html")

def user_register(request):
    if request.method=="POST":
        username=request.POST.get("username")
        phone=request.POST.get("number")
        password=request.POST.get("password")

        if User.objects.filter(username=username).exists():
            # Username already exists
            messages.error(request, "Username already exists")
            return redirect(user_signup)
        elif User.objects.filter(phone_number=phone).exists():
            # Number already exists
            messages.error(request, "Phone number already exists")
            return redirect(user_signup)
        else:
            User.objects.create(
                username=username,
                phone_number=phone,
                password=make_password(password),  #  HASH HERE
                role="user"
            )
            messages.success(request, "Sign in successfully completed..!")
            return redirect(user_signup)


def user_login(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        pswrd = request.POST.get("password")

        try:
            user = User.objects.get(username=uname)

            if check_password(pswrd, user.password):

                request.session['username'] = user.username

                if user.role == "admin":
                    return redirect('admin_dashboard')
                elif user.role == "owner":
                    return redirect(owner_dash)
                else:
                    return redirect(home)

            else:
                messages.error(request, "Incorrect Password")
                return redirect(user_signup)

        except User.DoesNotExist:
            messages.error(request, "User does not exist")
            return redirect(user_signup)

def user_logout(request):
    del request.session['username']
    return redirect(home)

def all_turf(request):
    return render(request,"All_Turf.html")

def category_filter(request):
    return render(request,"Category_Filter.html")