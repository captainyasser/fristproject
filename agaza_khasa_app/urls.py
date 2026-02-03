# agaza_khasa_app/urls.py
from django.urls import path
from . import views

app_name = 'agaza_khasa_app'

urlpatterns = [
    path('', views.select_employee_view, name='select_employee'),
    path('list/', views.special_leave_list, name='leave_list'),  # expects ?employee_id=
    path('add/', views.add_special_leave, name='add_leave'),
    path('edit/<int:pk>/', views.edit_special_leave, name='edit_leave'),
    path('delete/<int:pk>/', views.delete_special_leave, name='delete_leave'),
]
