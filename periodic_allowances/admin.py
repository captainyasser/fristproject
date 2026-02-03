from django.contrib import admin
from .models import PeriodicAllowance

@admin.register(PeriodicAllowance)
class PeriodicAllowanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'allowance_year', 'allowance_date', 'stored_value', 'calculated_value', 'has_difference']
    list_filter = ['allowance_year']
    search_fields = ['employee__name']
    
    def allowance_date(self, obj):
        return obj.allowance_date
    allowance_date.short_description = 'تاريخ العلاوة'
    
    def calculated_value(self, obj):
        return obj.get_calculated_value()
    calculated_value.short_description = 'القيمة المحسوبة'
    
    def has_difference(self, obj):
        return obj.has_difference
    has_difference.boolean = True
    has_difference.short_description = 'اختلاف؟'