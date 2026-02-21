from AdminApp import views
from django.urls import path

urlpatterns=[
    path('login/',views.admin_loginpage,name="login"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('admin_login/',views.admin_login,name="admin_login"),
#-----------------------------------------------------------------------------------------------------------------------
    path('add_category/',views.add_category,name="add_category"),
    path('save_category/',views.save_category,name="save_category"),
    path('category_details/',views.category_details,name="category_details"),
    path('edit_category/<int:cat_id>',views.edit_category,name="edit_category"),
    path('delete_category/<int:cat_id>',views.delete_category,name="delete_category"),
    path('update_category/<int:category_id>',views.update_category,name="update_category"),
#-----------------------------------------------------------------------------------------------------------------------
    path('user_details/',views.user_details,name="user_details"),
    path('edit_user/<int:user_id>/',views.edit_user,name="edit_user"),
    path('update_user/<int:ur_id>/',views.update_user,name="update_user"),
#-----------------------------------------------------------------------------------------------------------------------
    path('add_city/',views.add_city,name="add_city"),
    path('save_city/',views.save_city,name="save_city"),
    path('city_details/',views.city_details,name="city_details"),
    path('edit_city/<int:city_id>/',views.edit_city,name="edit_city"),
    path('update_city/<int:c_id>/',views.update_city,name="update_city"),
    path('city_delete/<int:city_id>/',views.city_delete,name="city_delete"),
]