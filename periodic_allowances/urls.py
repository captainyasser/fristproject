# E:\yasser\emapi2025\myproject\periodic_allowances\urls.py
# Updated urls.py

from django.urls import path
from . import views

app_name = 'periodic_allowances'

urlpatterns = [
    path('comparison/', views.AllowanceComparisonView.as_view(), name='comparison'),
    path('allowances-dftr/', views.AllowancesDftrView.as_view(), name='allowances_dftr'),
]