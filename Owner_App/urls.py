from Owner_App import views
from django.urls import path

urlpatterns=[
    path('owner_dash/',views.owner_dash,name="owner_dash"),
#-----------------------------------------------------------------------------------------------------------------------
    path('add_turf/',views.add_turf,name="add_turf"),
    path('save_turf/',views.save_turf,name="save_turf"),
    path('turf_details/',views.turf_details,name="turf_details"),
    path('edit_turf/<int:turf_id>/',views.edit_turf,name="edit_turf"),
    path('delete_turf/<int:turf_id>/',views.delete_turf,name="delete_turf"),
    path('update_turf/<int:t_id>/',views.update_turf,name="update_turf"),
#-----------------------------------------------------------------------------------------------------------------------
    path('offline_booking/<int:book_id>/',views.offline_booking,name="offline_booking"),
    path('save_offline_booking/',views.save_offline_booking,name="save_offline_booking"),
    path('booked_details/',views.booked_details,name="booked_details"),
    path('delete_bookings/<int:bk_id>/',views.delete_bookings,name="delete_bookings"),
]