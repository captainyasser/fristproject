# users/urls.py
from django.urls import path
from .views import add_user, login_view, logout_view

urlpatterns = [
    path('', login_view, name='login'),
    path('add/', add_user, name='add_user'),
    path('logout/', logout_view, name='logout'),
]