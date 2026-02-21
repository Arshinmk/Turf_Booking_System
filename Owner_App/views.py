from django.shortcuts import render,redirect
from Owner_App.models import *
from AdminApp.models import *
from UserApp.views import *
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
def owner_dash(request):
    return render(request,"Owner_Dash.html")

def add_turf(request):
    item=CategoryDb.objects.all()
    data=CityDb.objects.all()
    return render(request,"Add_Turf.html",{"item":item,"data":data})

def save_turf(request):
    if request.method == "POST":

        turf_name = request.POST.get("Turf_name")
        sport = request.POST.get("Sport")
        owner = request.POST.get("Owner")
        city = request.POST.get("City")
        location = request.POST.get("Location")
        price = request.POST.get("Price_per_hour")
        description = request.POST.get("Description")
        size = request.POST.get("Size")

        turf_img1 = request.FILES["Turf_image1"]
        turf_img2 = request.FILES["Turf_image2"]

        obj = TurfDb(
            Turf_name=turf_name,
            Sport=sport,
            Owner=owner,
            City=city,
            Location=location,
            Price_per_hour=price,
            Description=description,
            Size=size,
            Turf_image1=turf_img1,
            Turf_image2=turf_img2
        )

        obj.save()

        return redirect(add_turf)

def turf_details(request):
    item=TurfDb.objects.filter(Owner=request.session['username'])
    return render(request,"Turf_Details.html",{"item":item})

def edit_turf(request,turf_id):
    item = CategoryDb.objects.all()
    data = CityDb.objects.all()
    turf=TurfDb.objects.get(id=turf_id)
    return render(request,"Edit_Turf.html",{
                                            "item":item,
                                            "data":data,
                                            "turf":turf,
                                            })

def update_turf(request,t_id):
    if request.method == "POST":

        turf_name = request.POST.get("Turf_name")
        sport = request.POST.get("Sport")
        owner = request.POST.get("Owner")
        city = request.POST.get("City")
        location = request.POST.get("Location")
        price = request.POST.get("Price_per_hour")
        description = request.POST.get("Description")
        size = request.POST.get("Size")

        try:
            turf_img1 = request.FILES["Turf_image1"]
            f1=FileSystemStorage()
            file1=f1.save(turf_img1.name,turf_img1)
        except MultiValueDictKeyError:
            file1=TurfDb.objects.filter(id=t_id).Turf_image1

        try:
            turf_img2 = request.FILES["Turf_image2"]
            f2=FileSystemStorage()
            file2=f2.save(turf_img2.name,turf_img2)
        except MultiValueDictKeyError:
            file2=TurfDb.objects.filter(id=t_id).Turf_image2

        TurfDb.objects.filter(id=t_id).update(
            Turf_name=turf_name,
            Sport=sport,
            Owner=owner,
            City=city,
            Location=location,
            Price_per_hour=price,
            Description=description,
            Size=size,
            Turf_image1=file1,
            Turf_image2=file2
        )
        return redirect(turf_details)

def delete_turf(request,turf_id):
    TurfDb.objects.filter(id=turf_id).delete()
    return redirect(turf_details)