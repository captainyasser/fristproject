from django.urls import path
from . import views

app_name = 'secret_reports'

urlpatterns = [
    path('', views.index, name='index'),
    path('edit-by-employee/', views.edit_by_employee, name='edit_by_employee'),
    path('view-by-employee/', views.view_by_employee, name='view_by_employee'),
    path('edit-by-year/', views.edit_by_year, name='edit_by_year'),
    path('check-password/', views.check_password_ajax, name='check_password_ajax'),
    path('secrets-dfter/', views.secrets_dfter, name='secrets_dfter'),
]
