from django.shortcuts import render,redirect,get_object_or_404
from UserApp.models import *
from AdminApp.models import *
from Owner_App.views import *
from datetime import date, timedelta
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
import razorpay
from django.conf import settings
import json
from django.http import JsonResponse
from django.urls import reverse


# Create your views here.
def home(request):
    cat=CategoryDb.objects.all()
    city=CityDb.objects.all()
    turfs = TurfDb.objects.all()

    selected_city = request.session.get('selected_city')
    if selected_city:
        turfs = turfs.filter(City=selected_city)
    return render(request,"Home.html",{"cat":cat,"city":city,"turfs":turfs})
#-----------------------------------------------------------------------------------------------------------------------
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
                password=make_password(password),
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
#-----------------------------------------------------------------------------------------------------------------------
def all_turf(request):
    city = CityDb.objects.all()
    item=TurfDb.objects.all()
    category = CategoryDb.objects.all()

    selected_city = request.session.get('selected_city')
    if selected_city:
        item = item.filter(City=selected_city)

    return render(request,"All_Turf.html",{"city":city,"item":item,"category":category})

def category_filter(request,cat_name):
    city = CityDb.objects.all()
    item=TurfDb.objects.filter(Sport=cat_name)

    selected_city = request.session.get('selected_city')
    if selected_city:
        item = item.filter(City=selected_city)

    category=CategoryDb.objects.all()
    return render(request,"Category_Filter.html",{
        "item":item,
        "city":city,
        "selected_city":selected_city,
        "category":category,
    })

def single_turf(request,turf_id):
    city = CityDb.objects.all()
    data=TurfDb.objects.get(id=turf_id)

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
            turf=data,
            booking_date=selected_date
        ).values_list("slot", flat=True)

    return render(request,"Single_Turf.html",{
        "data":data,
        "city":city,
        "dates": dates,
        "slots": slots,
        "booked_slots": booked_slots,
        "selected_date": selected_date
    })

def book_slot(request):

    if request.method == "POST":

        turf_id = request.POST.get("turf_id")
        booking_date = request.POST.get("booking_date")
        slot = request.POST.get("slot")

        if not booking_date or not slot:
            messages.error(request, "Select date and slot")
            return redirect(reverse('single_turf', args=[turf_id]))

        turf = get_object_or_404(TurfDb, id=turf_id)
        user = User.objects.get(username=request.session['username'])

        conv_fee=50

        if BookingDb.objects.filter(turf=turf,booking_date=booking_date,slot=slot).exists():

            messages.error(request, "This slot is already booked!")
            return redirect(f"/single_turf/{turf_id}/?date={booking_date}")

        request.session['booking_data']={
            "turf_name":turf.Turf_name,
            "turf_id": turf_id,
            "booking_date": booking_date,
            "slot": slot,
            "conv_fee":conv_fee,
            "turf_price":turf.Price_per_hour,
            "price": float((turf.Price_per_hour)+conv_fee)
        }
        return redirect(payment_page)
#-----------------------------------------------------------------------------------------------------------------------
def set_city(request):
    if request.method == "POST":
        city_selected = request.POST.get("city")
        request.session['selected_city'] = city_selected
    return redirect(request.META.get('HTTP_REFERER', '/'))
#-----------------------------------------------------------------------------------------------------------------------
def payment_page(request):

    booking_data = request.session.get('booking_data')
    if not booking_data:
        messages.error(request, "No booking data found")
        return redirect('home')

    amount = int(float(booking_data['price']) * 100)

    client = razorpay.Client(auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    ))

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    # Save order_id in session
    request.session['razorpay_order_id'] = order['id']

    return render(request,"Payment_Page.html",{
        "booking":booking_data,
        "amount": amount,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "order_id": order['id'],
    })

def payment_success(request):

    if request.method == "POST":

        data = json.loads(request.body)

        booking_data = request.session.get('booking_data')
        order_id = request.session.get('razorpay_order_id')

        if not booking_data:
            return JsonResponse({"status": "failed"})

        client = razorpay.Client(auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET
        ))

        try:
            # Verify signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            })

            turf = TurfDb.objects.get(id=booking_data['turf_id'])
            user = User.objects.get(username=request.session['username'])

            # Final safety check
            if BookingDb.objects.filter(
                turf=turf,
                booking_date=booking_data['booking_date'],
                slot=booking_data['slot']
            ).exists():
                return JsonResponse({"status": "slot_taken"})

            BookingDb.objects.create(
                turf=turf,
                user=user,
                user_phone=user.phone_number,
                booking_date=booking_data['booking_date'],
                slot=booking_data['slot'],
                total_price=booking_data['price'],
                booking_type="Online"
            )

            # Clear session
            del request.session['booking_data']
            del request.session['razorpay_order_id']

            return JsonResponse({"status": "success"})

        except:
            return JsonResponse({"status": "failed"})
#-----------------------------------------------------------------------------------------------------------------------
def about_page(request):
    return render(request,"About_page.html")

def contact_page(request):
    return render(request,"Contact_page.html")

def save_contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        ContactMessage(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message).save()

        return redirect(contact_page)

def help_page(request):
    return render(request,"Help_page.html")

def save_owner_application(request):
    if request.method == "POST":
        owner_name = request.POST.get('owner_name')
        username = request.POST.get('username')
        owner_email = request.POST.get('owner_email')
        owner_phone = request.POST.get('owner_phone')
        turf_name = request.POST.get('turf_name')
        turf_city = request.POST.get('turf_city')
        turf_message = request.POST.get('turf_message')

        TurfOwnerApplication(
            username=username,
            owner_name=owner_name,
            owner_email=owner_email,
            owner_phone=owner_phone,
            turf_name=turf_name,
            turf_city=turf_city,
            turf_message=turf_message
        ).save()

        return redirect(help_page)

def user_booking(request):
    username=request.session['username']
    user = User.objects.get(username=username)
    item=BookingDb.objects.filter(user=user).order_by('-booking_date')
    return render(request,"Bookings.html",{"item":item})


