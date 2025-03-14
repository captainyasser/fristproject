from django.urls import path
from . import views

urlpatterns = [
    path('', views.rank_list, name='rank_list'),
    path('add/', views.add_rank, name='add_rank'),
    path('edit/<int:rank_id>/', views.edit_rank, name='edit_rank'),
    path('delete/<int:rank_id>/', views.delete_rank, name='delete_rank'),
]