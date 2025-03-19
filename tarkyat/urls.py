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
]