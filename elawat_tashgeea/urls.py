from django.urls import path
from . import views

app_name = 'elawat_tashgeea'

urlpatterns = [
    path('', views.index, name='index'),

    # إضافة علاوة لمجموعة موظفين
    path('batch-create/', views.batch_create, name='batch_create'),

    # اختيار الموظف وعرض العلاوات
    path('employee/select/', views.employee_elawat, name='employee_elawat_select'),

    # تعديل العلاوة
    path('edit-elawa/<int:pk>/', views.edit_elawa, name='edit_elawa'),

    # حذف العلاوة

    path('delete-elawa/<int:pk>/', views.delete_elawa, name='delete_elawa'),

    # عرض العلاوات حسب السنة
    path('year-filter/', views.elawat_by_year, name='elawat_by_year'),
    
    # elawat_tashgeea/urls.py
    path('add-multiple/', views.add_multiple_elawat, name='add_multiple_elawat'),

    # Nomination candidate list
    path('nominate/', views.nominate_employees, name='nominate_employees'),

    # Final Nomination List (Detailed)
    path('final-nomination/', views.final_nomination_list, name='final_nomination_list'),
]
