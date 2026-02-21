from django.shortcuts import render, redirect,get_object_or_404
from AdminApp.models import *
from django.contrib.auth import authenticate,login
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError


# Create your views here.
def admin_loginpage(request):
    return render(request,"Admin_login.html")

def admin_login(request):
    if request.method=="POST":
        uname=request.POST.get("username")
        pswd=request.POST.get("password")

        item=authenticate(request,username=uname,password=pswd)

        if item is not None:
            if item.role == "admin" or item.is_superuser:
                login(request,item)
                return redirect(dashboard)
            else:
                return redirect(admin_loginpage)
        else:
            return redirect(admin_loginpage)

def dashboard(request):
    return render(request,"Dashboard.html")
#---------------------------------------------------------------------------------------------------------------------
def add_category(request):
    return render(request,"Add_Category.html")

def save_category(request):
    if request.method=="POST":
        sport_name=request.POST.get("sport_name")
        sport_description=request.POST.get("sport_description")
        sport_img1=request.FILES["sport_img1"]
        sport_img2=request.FILES["sport_img2"]
        obj1=CategoryDb(Sport_name=sport_name,
                        Sport_description=sport_description,
                        Sport_img1=sport_img1,
                        Sport_img2=sport_img2
                        )
        obj1.save()
        return redirect(add_category)

def category_details(request):
    list=CategoryDb.objects.all()
    return render(request,"Category_Details.html",{"list":list})

def edit_category(request,cat_id):
    arg=CategoryDb.objects.get(id=cat_id)
    return render(request,"Edit_Category.html",{"arg":arg})

def update_category(request,category_id):
    if request.method=="POST":
        sport_name=request.POST.get("sport_name")
        sport_description=request.POST.get("sport_description")
        try:
            sport_img1 = request.FILES["sport_img1"]
            f1=FileSystemStorage()
            file1=f1.save(sport_img1.name,sport_img1)
        except MultiValueDictKeyError:
            file1=CategoryDb.objects.get(id=category_id).Sport_img1

        try:
            sport_img2 = request.FILES["sport_img2"]
            f2 = FileSystemStorage()
            file2 = f2.save(sport_img2.name, sport_img2)
        except MultiValueDictKeyError:
            file2 = CategoryDb.objects.get(id=category_id).Sport_img2


        CategoryDb.objects.filter(id=category_id).update(
            Sport_name=sport_name,
            Sport_description=sport_description,
            Sport_img1=file1,
            Sport_img2=file2
        )
        return redirect(category_details)

def delete_category(request,cat_id):
    obj2=CategoryDb.objects.filter(id=cat_id).delete()
    return redirect(category_details)
#-----------------------------------------------------------------------------------------------------------------------
def user_details(request):
    item = User.objects.filter(role__in=['user', 'owner'])
    return render(request,"User_Details.html",{"item":item})

def edit_user(request,user_id):
    obj=User.objects.get(id=user_id)
    return render(request,"Edit_User.html",{"obj":obj})

def update_user(request,ur_id):
    if request.method == "POST":

        uname = request.POST.get("username")
        role = request.POST.get("role")
        phone = request.POST.get("number")
        password = request.POST.get("password")


        # Check username exists (exclude current user)
        if User.objects.exclude(id=ur_id).filter(username=uname).exists():
            return redirect(edit_user)

        # Check phone exists (exclude current user)
        if User.objects.exclude(id=ur_id).filter(phone_number=phone).exists():
            return redirect(edit_user)

        User.objects.filter(id=ur_id).update(username=uname,role=role,phone_number=phone,password=password)
        return redirect(user_details)
#-----------------------------------------------------------------------------------------------------------------------
def add_city(request):
    return render(request,"Add_City.html")

def save_city(request):
    if request.method=="POST":
        cname=request.POST.get("city_name")
        CityDb(Cityname=cname).save()
        return redirect(add_city)

def city_details(request):
    list=CityDb.objects.all()
    return render(request,"City_Details.html",{"list":list})


def edit_city(request,city_id):
    item=CityDb.objects.get(id=city_id)
    return render(request,"Edit_City.html",{"item":item})

def update_city(request,c_id):
    if request.method == "POST":
        cname = request.POST.get("city_name")
        CityDb.objects.filter(id=c_id).update(Cityname=cname)
        return redirect(city_details)

def city_delete(request,city_id):
    CityDb.objects.filter(id=city_id).delete()
    return redirect(city_details)