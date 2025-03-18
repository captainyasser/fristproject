from django.urls import path
from . import views

urlpatterns = [
    path('promotions/', views.promotion_list, name='promotion_list'),
    path('promotions/edit/<int:pk>/', views.edit_promotion, name='edit_promotion'),
    path('promotions/delete/<int:pk>/', views.delete_promotion, name='delete_promotion'),
    path('promotions/add/', views.edit_promotion, name='add_promotion'),
    path('tarkyat/', views.tarkyat, name='tarkyat'),  # المسار الرئيسي لصفحة الترقيات
    path('ameen-tarkyat/', views.ameen_tarkyat, name='ameen_tarkyat'),
    path('daragaola-tarkya/', views.daragaola_tarkya, name='daragaola_tarkya'),
]