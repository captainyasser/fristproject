from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('detail/<int:task_id>/', views.task_detail, name='task_detail'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('api/notifications/', views.get_notifications, name='get_notifications'),
    path('api/mute/<int:task_id>/', views.mute_notification, name='mute_notification'),
]