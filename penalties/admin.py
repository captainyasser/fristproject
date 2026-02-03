# F:\emapi-edit\myproject\penalties\admin.py
from django.contrib import admin
from .models import PenaltyLevel, PenaltyApplied, ViolationCategory, ViolationType, PenaltyRecord, ViolationPreset

@admin.register(PenaltyLevel)
class PenaltyLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)

@admin.register(PenaltyApplied)
class PenaltyAppliedAdmin(admin.ModelAdmin):
    list_display = ('name', 'penalty_level', 'is_active')
    list_filter = ('penalty_level',)
    search_fields = ('name',)

@admin.register(ViolationCategory)
class ViolationCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    search_fields = ('name',)

@admin.register(ViolationType)
class ViolationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_absence', 'is_active')
    list_filter = ('category', 'is_absence')
    search_fields = ('name',)

@admin.register(PenaltyRecord)
class PenaltyRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'penalty_date', 'violation_type', 'penalty_level', 'penalty_applied', 'created_by')
    list_filter = ('penalty_date', 'category', 'penalty_level')
    search_fields = ('employee__name', 'violation_type__name')

@admin.register(ViolationPreset)
class ViolationPresetAdmin(admin.ModelAdmin):
    list_display = ('name', 'violation_type', 'is_active')
    list_filter = ('violation_type',)
    search_fields = ('name', 'text')
