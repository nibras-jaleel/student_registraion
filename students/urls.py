from django.urls import path
from . import views

urlpatterns =[
    path('add/',views.add_student, name='add_student'),
    path('view/',views.view_students, name='view_students'),
    path('update/<int:id>/',views.update_student, name='update_student'),
    path('delete/<int:id>/',views.delete_student, name='delete_student'),

    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    path('api/students/', views.api_get_students),
    path('api/add/', views.api_add_student),
    path('api/update/<int:id>/', views.api_update_student),
    path('api/delete/<int:id>/', views.api_delete_student),


]