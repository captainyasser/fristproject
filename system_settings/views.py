from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SystemSetting
from .forms import SystemSettingForm

def settings_view(request):
    # Get the singleton instance or create it
    setting, created = SystemSetting.objects.get_or_create(pk=1)
    
    if request.method == 'POST':
        form = SystemSettingForm(request.POST, instance=setting)
        if form.is_valid():
            form.save()
            messages.success(request, 'تم حفظ الإعدادات بنجاح.')
            return redirect('system_settings:settings_home')
    else:
        form = SystemSettingForm(instance=setting)
    
    return render(request, 'system_settings/settings_form.html', {'form': form})
