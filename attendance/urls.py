from django.urls import path
from . import views

urlpatterns = [
    path('attendance_3w/', views.attendance_3w, name='attendance_3w'),
    path('update_attendance/', views.update_attendance, name='update_attendance'),
    path('reset_rahatcounter/', views.reset_rahatcounter, name='reset_rahatcounter'),
    path('insert_attendance_for_date/', views.insert_attendance_for_date, name='insert_attendance_for_date'),
    # path('get_rahatcounter/', views.get_rahatcounter, name='get_rahatcounter'),
    # path('update_operation/', views.update_operation, name='update_operation'), 
    path('attendance/get-data/', views.get_attendance_data, name='get_attendance_data'),
    
    path('update_attendance/', views.update_attendance, name='update_attendance'),

    path('attendance/3w/', views.attendance_3w, name='attendance_3w'),
    path('attendance/update/', views.update_attendance, name='update_attendance'),
    path('attendance/reset-rahatcounter/', views.reset_rahatcounter, name='reset_rahatcounter'),
    path('attendance/get-attendance-data/', views.get_attendance, name='get_attendance'),
    path('attendance/insert-for-date/', views.insert_attendance_for_date, name='insert_attendance_for_date'),
    # path('attendance/update-operation/', views.update_operation, name='update_operation'),

    
    
    path('one-employee/', views.one_employee, name='one_employee'),
    

    # path('one_employee/', views.one_employee, name='one_employee'),
    # path('get_employee_data/', views.get_employee_data, name='get_employee_data'),
    # path('get_attendance_data/', views.get_attendance_data, name='get_attendance_data'),  # لـ attendance_3w
    # path('get_single_employee_attendance_data/', views.get_single_employee_attendance_data, name='get_single_employee_attendance_data'),  # لـ one_employee
    # path('update_attendance/', views.update_attendance, name='update_attendance'),



    
    
    
    # path('manage_single_employee/', views.manage_single_employee, name='manage_single_employee'),
    # path('get-employee-data2/', views.get_employee_data2, name='get_employee_data2'),
    # path('get-single-employee-attendance-data2/', views.get_single_employee_attendance_data2, name='get_single_employee_attendance_data2'),
    # path('update-attendance2/', views.update_attendance2, name='update_attendance2'),

    
    
]