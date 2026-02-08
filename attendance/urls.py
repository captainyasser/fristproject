

# attendance/urls.py
from django.urls import path
from . import views
from . import validation_views
from . import musicians_views

urlpatterns = [
    path('3w/', views.attendance_3w, name='attendance_3w'),
    path('validation/', validation_views.attendance_validation_view, name='attendance_validation'),
    path('api/get/', views.get_attendance, name='get_attendance'),
    path('api/update/', views.update_attendance, name='update_attendance'),
    path('api/update-operation/', views.update_operation, name='update_operation'),
    path('api/reset-rahatcounter/', views.reset_rahatcounter, name='reset_rahatcounter'),
    path('api/insert/', views.insert_attendance_for_date, name='insert_attendance_for_date'),
    path('one_employee/', views.one_employee_view, name='one_employee_view'),
    path('api/one_employee/', views.one_employee, name='one_employee'),
    path('api/undo-last-change/', views.undo_last_change, name='undo_last_change'),
    path('api/redo-last-change/', views.redo_last_change, name='redo_last_change'),
    path('api/adjust_rahatcounter/', views.adjust_rahatcounter, name='adjust_rahatcounter'),
    path('api/foodlist/', views.FoodListAPIView.as_view(), name='foodlist-api'),
    path('foodlist/', views.foodlist_page, name='foodlist_page'),
    path('api/amtmam/', views.AmtmamAPIView.as_view(), name='amtmam-api'),
    path('amtmam/', views.amtmam_page, name='amtmam_page'),
    path('api/numreport/', views.NumReportAPIView.as_view(), name='numreport-api'),
    path('numreport/', views.numreport_page, name='numreport_page'),
    path('api/kashftmam/', views.KashftmamAPIView.as_view(), name='kashftmam-api'),
    path('kashftmam/', views.kashftmam_page, name='kashftmam_page'),
    path('api/bus/', views.BusAPIView.as_view(), name='bus-api'),
    path('bus/', views.bus, name='bus'),
    path('api/monthly-discount/', views.MonthlyDiscountAPIView.as_view(), name='monthly-discount-api'),
    path('monthly-discount/', views.monthlydiscount_page, name='monthlydiscount_page'),
    path('employeestates/', views.employeestates_page, name='employeestates_page'),
    path('outs/', views.outs_report, name='outs_report'),
    path('api/bulk-attendance/', views.BulkAttendanceView.as_view(), name='bulk-attendance'),
    path('musicians/', musicians_views.musicians_page, name='musicians_page'),
    path('api/filter-musicians/', musicians_views.filter_musicians, name='filter_musicians'),
    path('api/bulk-update-musicians/', musicians_views.bulk_update_musicians, name='bulk_update_musicians'),
    path('api/calculate-rahat-period/', musicians_views.calculate_rahat_period, name='calculate_rahat_period'),
    path('api/namesreport/', views.NamesReportAPIView.as_view(), name='namesreport-api'),
    path('namesreport/', views.namesreport_page, name='namesreport_page'),
    path('weekly-food-average/', views.weekly_food_average, name='weekly_food_average'),
    path('names-index/', views.names_index_view, name='names_index'),
    
    ]













    
    # path('update_attendance/', views.update_attendance, name='update_attendance'),
    # path('reset_rahatcounter/', views.reset_rahatcounter, name='reset_rahatcounter'),
    # path('insert_attendance_for_date/', views.insert_attendance_for_date, name='insert_attendance_for_date'),
    # path('update_operation/', views.update_operation, name='update_operation'),
    # path('update_attendance/', views.update_attendance, name='update_attendance'),
    # path('bus/', views.bus_view, name='bus_view'),
    # path('kashftmam/', views.kashftmam, name='kashftmam'),
    # path('attendance/3w/', views.attendance_3w, name='attendance_3w'),
    # path('attendance/simple/', views.simple_attendance, name='simple_attendance'),
    # path('attendance/update/', views.update_attendance, name='update_attendance'),
    # path('attendance/reset-rahatcounter/', views.reset_rahatcounter, name='reset_rahatcounter'),
    # path('attendance/get-attendance-data/', views.get_attendance, name='get_attendance'),
    # path('attendance/get-attendance-data2/', views.simple_get_att, name='simple_get_att'),
    # path('attendance/insert-for-date/', views.insert_attendance_for_date, name='insert_attendance_for_date'),
    # path('one-employee/', views.one_employee, name='one_employee'),
    # path('foodlist/', views.foodlist, name='foodlist'),
    # path('amtmam/',  views.amtmam_view, name='amtmam'),
    # path('numreport/', views.numreport, name='numreport'),
    # path('outs/', views.outs, name='outs'),
    # path('insertmany/', views.insert_many_attendance, name='insert_many_attendance'),
    # path('monthly_discount/', views.monthly_discount, name='monthly_discount'),




    
    





    # path('one_employee/', views.one_employee, name='one_employee'),
    # path('get_employee_data/', views.get_employee_data, name='get_employee_data'),
    # path('get_attendance_data/', views.get_attendance_data, name='get_attendance_data'),  # لـ attendance_3w
    # path('get_single_employee_attendance_data/', views.get_single_employee_attendance_data, name='get_single_employee_attendance_data'),  # لـ one_employee
    # path('update_attendance/', views.update_attendance, name='update_attendance'),
    # path('manage_single_employee/', views.manage_single_employee, name='manage_single_employee'),
    # path('get-employee-data2/', views.get_employee_data2, name='get_employee_data2'),
    # path('get-single-employee-attendance-data2/', views.get_single_employee_attendance_data2, name='get_single_employee_attendance_data2'),
    # path('update-attendance2/', views.update_attendance2, name='update_attendance2'),