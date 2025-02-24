
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import add_user

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('add/', add_user, name='add_user'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    
    
    
]

