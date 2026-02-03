# F:\emapi-edit\myproject\penalties\urls.py
from django.urls import path
from . import views

app_name = 'penalties'

urlpatterns = [
    path('', views.PenaltiesDashboardView.as_view(), name='dashboard'),
    
    # Levels
    path('levels/', views.PenaltyLevelListView.as_view(), name='level_list'),
    path('levels/add/', views.PenaltyLevelCreateView.as_view(), name='level_create'),
    path('levels/<int:pk>/edit/', views.PenaltyLevelUpdateView.as_view(), name='level_update'),
    path('levels/<int:pk>/delete/', views.PenaltyLevelDeleteView.as_view(), name='level_delete'),
    
    # Applied Penalties
    path('applied/', views.PenaltyAppliedListView.as_view(), name='applied_list'),
    path('applied/add/', views.PenaltyAppliedCreateView.as_view(), name='applied_create'),
    path('applied/<int:pk>/edit/', views.PenaltyAppliedUpdateView.as_view(), name='applied_update'),
    path('applied/<int:pk>/delete/', views.PenaltyAppliedDeleteView.as_view(), name='applied_delete'),

    # Categories
    path('categories/', views.ViolationCategoryListView.as_view(), name='category_list'),
    path('categories/add/', views.ViolationCategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', views.ViolationCategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.ViolationCategoryDeleteView.as_view(), name='category_delete'),
    
    # Types
    path('types/', views.ViolationTypeListView.as_view(), name='type_list'),
    path('types/add/', views.ViolationTypeCreateView.as_view(), name='type_create'),
    path('types/<int:pk>/edit/', views.ViolationTypeUpdateView.as_view(), name='type_update'),
    path('types/<int:pk>/delete/', views.ViolationTypeDeleteView.as_view(), name='type_delete'),
    
    # Records
    path('records/', views.PenaltyRecordListView.as_view(), name='record_list'),
    path('records/add/', views.PenaltyRecordCreateView.as_view(), name='record_create'),
    path('records/<int:pk>/edit/', views.PenaltyRecordUpdateView.as_view(), name='record_update'),
    path('records/<int:pk>/delete/', views.PenaltyRecordDeleteView.as_view(), name='record_delete'),
    
    # Presets
    path('presets/', views.ViolationPresetListView.as_view(), name='preset_list'),
    path('presets/add/', views.ViolationPresetCreateView.as_view(), name='preset_create'),
    path('presets/<int:pk>/edit/', views.ViolationPresetUpdateView.as_view(), name='preset_update'),
    path('presets/<int:pk>/delete/', views.ViolationPresetDeleteView.as_view(), name='preset_delete'),


    # =========================
    # Penalty Amount URLs
    # =========================
    path('amounts/', views.PenaltyAmountListView.as_view(), name='amount_list'),
    path('amounts/add/', views.PenaltyAmountCreateView.as_view(), name='amount_create'),
    path('amounts/<int:pk>/edit/', views.PenaltyAmountUpdateView.as_view(), name='amount_update'),
    path('amounts/<int:pk>/delete/', views.PenaltyAmountDeleteView.as_view(), name='amount_delete'),

    # Penalty Extract Report
    path('extract/', views.PenaltyExtractSelectView.as_view(), name='penalty_extract_select'),
    path('extract/<int:employee_id>/', views.PenaltyExtractView.as_view(), name='penalty_extract'),

]
