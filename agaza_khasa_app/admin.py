# agaza_khasa_app/admin.py
from django.contrib import admin
from .models import SpecialLeave

@admin.register(SpecialLeave)
class SpecialLeaveAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'leave_reason', 'start_date', 'return_date', 'year')
    list_filter = ('leave_reason', 'year')
    search_fields = ('employee__name', 'employee__id_number', 'decision_number')
