from django.urls import path
from . import views
from .views import  add_employee


urlpatterns = [
    path('', views.home, name='home'),
    path('add/', add_employee, name='add_employee'),
    path('edit_employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
    path('employee_statement/', views.employee_statement, name='employee_statement'),    
    path('filterdata/', views.filterdata, name='filterdata'),    
    path('edit_multi/', views.edit_multi, name='edit_multi'),
    
    
    
    
    
]
