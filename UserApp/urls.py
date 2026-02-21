from UserApp import views
from django.urls import path

urlpatterns=[
    path('home/',views.home,name="home"),
    path('signup/',views.user_signup,name="user_signup"),
    path('user_register/',views.user_register,name="user_register"),
    path('user_login/',views.user_login,name="user_login"),
    path('user_logout/',views.user_logout,name="user_logout"),
    path('all_turf/',views.all_turf,name="all_turf"),
    path('category_filter/',views.category_filter,name="category_filter"),
]