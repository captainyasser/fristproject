from django.urls import path
from . import views

urlpatterns = [
    path('', views.backup_page, name='backup_page'),
    path('backup/', views.backup_database, name='backup_database'),
    path('restore/<str:filename>/', views.restore_database, name='restore_database'),
    path('delete/<str:filename>/', views.delete_backup, name='delete_backup'),
    path('download/<str:filename>/', views.download_backup, name='download_backup'),
    path('upload/', views.upload_backup, name='upload_backup'),
]