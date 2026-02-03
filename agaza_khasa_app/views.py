# agaza_khasa_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from .models import SpecialLeave
from .forms import SpecialLeaveForm, EditSpecialLeaveForm
from em_data.models import Employee
from django.db.models import Count
from django.http import JsonResponse, HttpResponseForbidden

def select_employee_view(request):
    # صفحة اختيار الموظف (عرض افتراضي)
    employees_with_leaves = Employee.objects.filter(special_leaves__isnull=False).distinct()
    return render(request, 'agaza_khasa_app/select_employee.html', {
        'employees': employees_with_leaves
    })

def special_leave_list(request):
    employee_id = request.GET.get('employee_id')
    employee = None
    leaves = SpecialLeave.objects.none()
    if employee_id:
        employee = get_object_or_404(Employee, pk=employee_id)
        leaves = employee.special_leaves.all().order_by('-start_date', '-created_at')
    employees_with_leaves = Employee.objects.filter(special_leaves__isnull=False).distinct()
    return render(request, 'agaza_khasa_app/list.html', {
        'employees': employees_with_leaves,
        'selected_employee': employee,
        'leaves': leaves,
    })

def add_special_leave(request):
    if request.method == 'POST':
        form = SpecialLeaveForm(request.POST)
        if form.is_valid():
            special = form.save(commit=False)
            special.save()
            # عند الإضافة، يجب تغيير field operation للفرد إلى "خاصه"
            emp = special.employee
            emp.operation = 'خاصه'
            emp.save(update_fields=['operation'])
            messages.success(request, 'تم إضافة الإجازة الخاصة بنجاح.')
            return redirect(reverse('agaza_khasa_app:leave_list') + f'?employee_id={emp.id}')
        else:
            messages.error(request, 'هناك أخطاء في الحقول، تأكد من المدخلات.')
    else:
        form = SpecialLeaveForm()
    return render(request, 'agaza_khasa_app/add.html', {'form': form})

def edit_special_leave(request, pk):
    special = get_object_or_404(SpecialLeave, pk=pk)
    if request.method == 'POST':
        form = EditSpecialLeaveForm(request.POST, instance=special)
        if form.is_valid():
            cut = form.cleaned_data.get('cut_checkbox', False)
            old_return = special.return_date
            special = form.save(commit=False)
            # إذا اختار المستخدم قطع الإجازة، أضف ملاحظة تلقائية
            if cut:
                now = timezone.localtime()
                note_line = f"تم قطع الإجازة بتاريخ {now.date().isoformat()}"
                if special.return_date:
                    note_line += f" وتعديل تاريخ العودة إلى {special.return_date.isoformat()}"
                # أدخل مع السجل السابق للملاحظات
                existing = special.notes or ''
                if existing.strip():
                    special.notes = existing + f"\n{note_line}"
                else:
                    special.notes = note_line
            special.save()
            messages.success(request, 'تم تعديل الإجازة الخاصة بنجاح.')
            return redirect(reverse('agaza_khasa_app:leave_list') + f'?employee_id={special.employee.id}')
        else:
            messages.error(request, 'هناك أخطاء في الحقول.')
    else:
        # prefill form; include cut_checkbox unchecked by default
        form = EditSpecialLeaveForm(instance=special)
    return render(request, 'agaza_khasa_app/edit.html', {'form': form, 'special': special})

def delete_special_leave(request, pk):
    if request.method == 'POST':
        special = get_object_or_404(SpecialLeave, pk=pk)
        employee_id = special.employee.id
        special.delete()
        # بحسب المطلوب: عند حذف آخر إجازة خاصة لا تفعل شيء في operation
        messages.success(request, 'تم حذف الإجازة الخاصة.')
        return redirect(reverse('agaza_khasa_app:leave_list') + f'?employee_id={employee_id}')
    else:
        return HttpResponseForbidden("غير مسموح")
