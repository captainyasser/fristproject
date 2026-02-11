# em_data/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmployeeViewSet, home, FilterDataAPIView, filterdata_view, edit_multi_view,
    EmployeeStatementAPIView, employee_statement_html, idcard_data_view,
    idcard_filter_view, IDCardFilterAPIView,
    department_operation_report_view, DepartmentOperationReportAPIView,
    professional_profile
)

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('home/', home, name='home'),
    path('professional-profile/', professional_profile, name='professional_profile'),
    path('filterdata/', FilterDataAPIView.as_view(), name='filterdata_api'),
    path('filter/', filterdata_view, name='filterdata'),
    path('edit-multi/', edit_multi_view, name='edit_multi'),
    path('api/employee-statement/', EmployeeStatementAPIView.as_view(), name='employee-statement-api'),
    path('employee-statement/', employee_statement_html, name='employee-statement-html'),
    path('idcard-data/', idcard_data_view, name='idcard_data'),
    path('idcard-filter/', idcard_filter_view, name='idcard_filter'),
    path('api/idcard-filter/', IDCardFilterAPIView.as_view(), name='idcard_filter_api'),
    path('department-operation-report/', department_operation_report_view, name='department_operation_report'),
    path('api/department-operation-report/', DepartmentOperationReportAPIView.as_view(), name='department_operation_report_api'),
]

# from django.urls import path
# from . import views
# from .views import  add_employee


# urlpatterns = [
#     path('', views.home, name='home'),
#     path('add/', add_employee, name='add_employee'),
#     path('edit_employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),
#     path('employee_statement/', views.employee_statement, name='employee_statement'),    
#     path('filterdata/', views.filterdata, name='filterdata'),    
#     path('edit_multi/', views.edit_multi, name='edit_multi'),
#     path('employee/<int:employee_id>/delete/', views.delete_employee, name='delete_employee'),
    
    
    
    
# ]
