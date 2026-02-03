from django.contrib import admin
from .models import Education

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'employee_rank_id', 'qualification_type', 'level', 'grade', 'obtained_date')
    search_fields = ('employee__name', 'university_name', 'qualification_type', 'decision_number')
    list_filter = ('level', 'qualification_type', 'grade')

    def employee_rank_id(self, obj):
        return getattr(obj.employee.rank, 'id', None)
    employee_rank_id.short_description = 'rank.id'
