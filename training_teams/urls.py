from django.urls import path
from . import views

urlpatterns = [
    # 1. صفحة الفرق التدريبية الرئيسية (training.html)
    path('training-page/', views.training_page_view, name='training_page_view'),
    # 2. الفرق التدريبية حسب الفرد (em_training_teams.html)
    path('em-training-teams/', views.em_training_teams_view, name='em_training_teams'),
    # 3. الفرق التدريبية حسب اسم الفرقة (training_teams.html)
    path('training-teams/', views.training_teams_view, name='training_teams'),
    # 4. فلتر الفرق التدريبية (training-teams-filter.html)
    path('training-teams-filter/', views.training_teams_filter, name='training_teams_filter'),
    # 5. إضافة فرقة تدريبية جديدة (insert_training.html)
    path('insert-training/', views.insert_training, name='insert_training'),
    # 6. تعديل سجل تدريبي (edit_training_record.html)
    path('edit-training-record/', views.edit_training_record, name='edit-training-record'),
    path('get-employee-training-data/<int:employee_id>/', views.get_employee_training_data, name='get_employee_training_data'),
    path('update-training-record/', views.update_training_record, name='update-training-record'),
    # 7. حذف سجل تدريبي
    path('delete-training-record/<int:training_id>/', views.delete_training_record, name='delete-training-record'),
    # 8. صفحة الأماكن
    path("places/", views.places_page, name="places_page"),
    # 9. الفرق التدريبية الحالية
    path("current-teams/", views.current_teams_view, name="current_teams"),
    
    
    
    
    
    
]