from django.urls import path
from . import views

app_name = 'education'

urlpatterns = [
    path('', views.education_list, name='list'),
    path('add/', views.education_create_or_update, name='add'),
    path('edit/<int:pk>/', views.education_create_or_update, name='edit'),
    path('delete/<int:pk>/', views.education_delete, name='delete'),
]
