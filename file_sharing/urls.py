# file_sharing/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.file_share, name='file_share'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('delete/<int:file_id>/', views.delete_files, name='delete_files'),
]

