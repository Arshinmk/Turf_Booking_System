from django.shortcuts import render,redirect,get_object_or_404
from Owner_App.models import *
from AdminApp.models import *
from UserApp.views import *
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from UserApp.models import *
from datetime import date, timedelta
from Owner_App.decorators import owner_required

# Create your views here.
@owner_required
def owner_dash(request):
    return render(request,"Owner_Dash.html")

@owner_required
def add_turf(request):
    item=CategoryDb.objects.all()
    data=CityDb.objects.all()
    return render(request,"Add_Turf.html",{"item":item,"data":data})

@owner_required
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

@owner_required
def turf_details(request):
    item=TurfDb.objects.filter(Owner=request.session['username'])
    return render(request,"Turf_Details.html",{"item":item})

@owner_required
def edit_turf(request,turf_id):
    item = CategoryDb.objects.all()
    data = CityDb.objects.all()
    turf=TurfDb.objects.get(id=turf_id)
    return render(request,"Edit_Turf.html",{
                                            "item":item,
                                            "data":data,
                                            "turf":turf,
                                            })

@owner_required
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
            file1=TurfDb.objects.get(id=t_id).Turf_image1

        try:
            turf_img2 = request.FILES["Turf_image2"]
            f2=FileSystemStorage()
            file2=f2.save(turf_img2.name,turf_img2)
        except MultiValueDictKeyError:
            file2=TurfDb.objects.get(id=t_id).Turf_image2

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

@owner_required
def delete_turf(request,turf_id):
    TurfDb.objects.filter(id=turf_id).delete()
    return redirect(turf_details)

@owner_required
def offline_booking(request,book_id):
    turf = get_object_or_404(TurfDb, id=book_id)

    today = date.today()
    dates = [today + timedelta(days=i) for i in range(30)]

    slots =  [
            "12:00 AM - 1:00 AM",
            "1:00 AM - 2:00 AM",
            "2:00 AM - 3:00 AM",
            "3:00 AM - 4:00 AM",
            "4:00 AM - 5:00 AM",
            "5:00 AM - 6:00 AM",
            "6:00 AM - 7:00 AM",
            "7:00 AM - 8:00 AM",
            "8:00 AM - 9:00 AM",
            "9:00 AM - 10:00 AM",
            "10:00 AM - 11:00 AM",
            "11:00 AM - 12:00 PM",
            "12:00 PM - 1:00 PM",
            "1:00 PM - 2:00 PM",
            "2:00 PM - 3:00 PM",
            "3:00 PM - 4:00 PM",
            "4:00 PM - 5:00 PM",
            "5:00 PM - 6:00 PM",
            "6:00 PM - 7:00 PM",
            "7:00 PM - 8:00 PM",
            "8:00 PM - 9:00 PM",
            "9:00 PM - 10:00 PM",
            "10:00 PM - 11:00 PM",
            "11:00 PM - 12:00 AM"
        ]

    selected_date = request.GET.get("date")
    booked_slots = []

    if selected_date:
        booked_slots = BookingDb.objects.filter(
            turf=turf,
            booking_date=selected_date
        ).values_list("slot", flat=True)

    return render(request,"Offline_Booking.html",{
        "turf":turf,
        "dates": dates,
        "slots": slots,
        "booked_slots": booked_slots,
        "selected_date": selected_date
    })

@owner_required
def save_offline_booking(request):
    if request.method=="POST":
        turf_id=request.POST.get("turf_id")
        booking_date=request.POST.get("booking_date")
        slot=request.POST.get("slot")
        customer_name=request.POST.get("customer_name")

        turf=get_object_or_404(TurfDb,id=turf_id)

        owner=User.objects.get(username=request.session['username'])

        if BookingDb.objects.filter(
            turf=turf,
            booking_date=booking_date,
            slot=slot
        ).exists():
            messages.error(request, "Slot already booked!")
            return redirect(f"/Owner_App/offline_booking/{turf_id}/?date={booking_date}")

        BookingDb.objects.create(
            turf=turf,
            user=owner,
            booking_date=booking_date,
            slot=slot,
            total_price=turf.Price_per_hour,
            booking_type="Offline",
            customer_name=customer_name
        )

        messages.success(request, "Offline Booking Saved!")
        return redirect("owner_dash")
#-----------------------------------------------------------------------------------------------------------------------
@owner_required
def booked_details(request):
    owner=request.session['username']
    book=BookingDb.objects.filter(turf__Owner=owner).order_by("-created_at")
    return render(request,"Booked_Details.html",{"book":book})

@owner_required
def delete_bookings(request,bk_id):
    BookingDb.objects.filter(id=bk_id).delete()
    return redirect(booked_details)