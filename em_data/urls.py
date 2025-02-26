from django.urls import path
from . import views
from .views import  add_employee, edit_employee


urlpatterns = [
    path('', views.home, name='home'),
    path('add/', add_employee, name='add_employee'),
    path('edit_employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('age-update/', views.age_update, name='age_update'),
    
    
    
    
    
    
    
]
