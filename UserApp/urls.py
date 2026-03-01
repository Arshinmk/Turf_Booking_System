from UserApp import views
from django.urls import path

urlpatterns=[
    path('home/',views.home,name="home"),
    path('signup/',views.user_signup,name="user_signup"),
    path('user_register/',views.user_register,name="user_register"),
    path('user_login/',views.user_login,name="user_login"),
    path('user_logout/',views.user_logout,name="user_logout"),
#-----------------------------------------------------------------------------------------------------------------------
    path('all_turf/',views.all_turf,name="all_turf"),
    path('about/',views.about_page,name="about"),
    path('contact/',views.contact_page,name="contact"),
    path('help',views.help_page,name="help"),
    path('save_owner_application',views.save_owner_application,name="save_owner_application"),
    path('save_contact/',views.save_contact,name="save_contact"),
    path('category_filter/<cat_name>/',views.category_filter,name="category_filter"),
    path('single_turf/<int:turf_id>/',views.single_turf,name="single_turf"),
    path('user_booking/',views.user_booking,name="user_booking"),
#-----------------------------------------------------------------------------------------------------------------------
    path('set_city/',views.set_city,name="set_city"),
    path('book_slot/',views.book_slot,name="book_slot"),
    path('payment_page/',views.payment_page,name="payment_page"),
    path('payment_success/',views.payment_success,name="payment_success"),
]