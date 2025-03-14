from django.urls import path
from . import views

urlpatterns = [
    path('', views.tarkyat_page_view, name='tarkyat_page_view'),
    path('add/', views.add_tarkya, name='add_tarkya'),
    path('edit-promotions/', views.edit_promotions, name='edit_promotions'),




]