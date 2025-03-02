from django.urls import path
from . import views

urlpatterns = [
    path('attendance_3w/', views.attendance_3w, name='attendance_3w'),
    path('update_attendance/', views.update_attendance, name='update_attendance'),
    path('reset_rahatcounter/', views.reset_rahatcounter, name='reset_rahatcounter'),
    path('insert_attendance_for_date/', views.insert_attendance_for_date, name='insert_attendance_for_date'),
    path('get_rahatcounter/', views.get_rahatcounter, name='get_rahatcounter'),
    path('update_operation/', views.update_operation, name='update_operation'), 
    path('attendance/get-data/', views.get_attendance_data, name='get_attendance_data'),
    

    path('attendance/3w/', views.attendance_3w, name='attendance_3w'),
    path('attendance/update/', views.update_attendance, name='update_attendance'),
    path('attendance/reset-rahatcounter/', views.reset_rahatcounter, name='reset_rahatcounter'),
    path('attendance/get-attendance-data/', views.get_attendance_data, name='get_attendance_data'),
    path('attendance/insert-for-date/', views.insert_attendance_for_date, name='insert_attendance_for_date'),
    path('attendance/update-operation/', views.update_operation, name='update_operation'),

    
    
    
    
]