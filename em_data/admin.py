from django.contrib import admin
from .models import Employee, TransferRecord, TransferLocation, MusicalInstrument

@admin.register(MusicalInstrument)
class MusicalInstrumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name',)
    list_filter = ('category',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'police_number', 'department', 'primary_instrument')
    search_fields = ('name', 'police_number', 'id_number')
    list_filter = ('department', 'rank', 'primary_instrument')

@admin.register(TransferRecord)
class TransferRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'transfer_type', 'year')
    search_fields = ('name',)

@admin.register(TransferLocation)
class TransferLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_type')
