from django.urls import path
from .views import DepartmentList, DepartmentDetail, DepartmentsPage

urlpatterns = [
    path('', DepartmentsPage.as_view(), name='departments_list'),
    path('api/departments/', DepartmentList.as_view(), name='department-list'),
    path('api/departments/<int:id>/', DepartmentDetail.as_view(), name='department-detail'),
]