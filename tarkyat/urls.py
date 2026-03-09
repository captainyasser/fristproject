# from django.urls import path
# from . import views

# urlpatterns = [
#     path('tarkyat/', views.tarkyat, name='tarkyat'),
#     path('add-many/', views.add_tarkya_for_many, name='add_tarkya_for_many'),
#     path('promotions/', views.promotion_list, name='promotion_list'),
#     path('promotions/edit/<int:pk>/', views.edit_promotion, name='edit_promotion'),
#     path('promotions/delete/<int:pk>/', views.delete_promotion, name='delete_promotion'),
#     path('promotions/add/', views.edit_promotion, name='add_promotion'),
#     path('ameen-tarkyat/', views.ameen_tarkyat, name='ameen_tarkyat'),
#     path('daragaola-tarkya/', views.daragaola_tarkya, name='daragaola_tarkya'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.tarkyat, name='tarkyat'),
    path('promotions/', views.promotion_list, name='promotion_list'),
    path('promotions/add/', views.add_promotion, name='add_promotion'),  # للإضافة
    path('promotions/edit/<int:pk>/', views.edit_promotion, name='edit_promotion'),  # للتعديل
    path('promotions/delete/<int:pk>/', views.delete_promotion, name='delete_promotion'),
    path('add_tarkya_for_many/', views.add_tarkya_for_many, name='add_tarkya_for_many'),
    path('ameen_tarkyat/', views.ameen_tarkyat, name='ameen_tarkyat'),
    path('daragaola_tarkya/', views.daragaola_tarkya, name='daragaola_tarkya'),
    path('training/', views.tarkyat_training, name='tarkyat_training'),
    path('training/add/', views.add_training_qualification, name='add_training_qualification'),
    path('next_tarkya/', views.next_tarkya, name='next_tarkya'),
    path('m3awn_tarkyat/', views.m3awn_tarkyat, name='m3awn_tarkyat'),

]