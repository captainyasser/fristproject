from django.contrib import admin
from .models import Rank

@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # عرض الحقول في القائمة
    search_fields = ('name',)  # إضافة مربع بحث بالاسم
    ordering = ('name',)  # ترتيب التصنيفات أبجدياً
