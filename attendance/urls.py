# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.attendance_record, name='attendance_record'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('attendance_3w/', views.attendance_3w, name='attendance_3w'),
    path('update_attendance/', views.update_attendance, name='update_attendance'),
    path('reset_rahatcounter/', views.reset_rahatcounter, name='reset_rahatcounter'),
    path('insert_attendance_for_date/', views.insert_attendance_for_date, name='insert_attendance_for_date'),
    path('get_rahatcounter/', views.get_rahatcounter, name='get_rahatcounter'),
]