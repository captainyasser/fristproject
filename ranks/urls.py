
# project/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RankViewSet

router = DefaultRouter()
router.register(r'', RankViewSet, basename='rank')

urlpatterns = [
    path('', include(router.urls)),
]


# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.rank_list, name='rank_list'),
#     path('add/', views.add_rank, name='add_rank'),
#     path('edit/<int:rank_id>/', views.edit_rank, name='edit_rank'),
#     path('delete/<int:rank_id>/', views.delete_rank, name='delete_rank'),
# ]