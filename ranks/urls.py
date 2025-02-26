from django.urls import path
from .views import rank_list, add_rank, edit_rank, delete_rank

urlpatterns = [
    path('', rank_list, name='rank_list'),  # عرض جميع الدرجات
    path('add/', add_rank, name='add_rank'),  # إضافة درجة جديدة
    path('edit/<int:rank_id>/', edit_rank, name='edit_rank'),  # تعديل درجة
    path('delete/<int:rank_id>/', delete_rank, name='delete_rank'),  # حذف درجة
]
