from django.urls import path
from .views import hasr_select_employee_view, hasr_sheet_view

app_name = 'hasr_app'

urlpatterns = [
    path('', hasr_select_employee_view, name='hasr'),  # صفحة اختيار الموظف
    path('<int:employee_id>/', hasr_sheet_view, name='hasr_sheet'),  # صفحة الحصر
]
