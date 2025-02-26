from django.urls import path
from .views import departments_list, add_department, edit_department, delete_department

urlpatterns = [
    path('', departments_list, name='departments_list'),
    path('/add/', add_department, name='add_department'),
    path('/edit/<int:department_id>/', edit_department, name='edit_department'),
    path('/delete/<int:department_id>/', delete_department, name='delete_department'),
]
