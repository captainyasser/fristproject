from django.urls import path
from .views import add_institute

urlpatterns = [
    path('add_institute/', add_institute, name='add_institute'),
]
