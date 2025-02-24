from django.urls import path
from . import views
from .views import  add_employee, edit_employee


urlpatterns = [
    path('', views.home, name='home'),
    path('add/', add_employee, name='add_employee'),
    path('edit/<int:employee_id>/', edit_employee, name='edit_employee'),  # Correct URL pattern
    # path('/delete/<int:id>/', delete_employee, name='delete_employee'),
]
