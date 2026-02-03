from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Education, LEVEL_CHOICES, TYPE_CHOICES
from .forms import EducationForm
from em_data.models import Employee

def education_create_or_update(request, pk=None):
    if pk:
        instance = get_object_or_404(Education, pk=pk)
        action = "تحديث"
    else:
        instance = None
        action = "إضافة"

    if request.method == 'POST':
        form = EducationForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            education = form.save()
            if instance:
                messages.success(request, "تم تحديث المؤهل بنجاح")
            else:
                messages.success(request, "تم إضافة المؤهل بنجاح")
            return redirect('education:list')
        else:
            messages.error(request, "هناك أخطاء في الفورم، تأكد من الحقول")
    else:
        # إذا تم تمرير employee_id في GET نعبّئ الاختيار تلقائياً
        initial = {}
        emp_id = request.GET.get('employee')
        if not instance and emp_id:
            try:
                initial['employee'] = Employee.objects.get(pk=emp_id)
            except Employee.DoesNotExist:
                pass
        form = EducationForm(instance=instance, initial=initial)

    return render(request, 'education/education_form.html', {
        'form': form,
        'action': action,
        'instance': instance,
    })


def education_list(request):
    qs = Education.objects.select_related('employee', 'employee__rank').all().order_by('employee__rank__id', 'employee__name')

    # فلترة بمستوى المؤهل وأنواع المؤهل — تسمح بتحديد أكثر من خيار
    levels = request.GET.getlist('level')
    types = request.GET.getlist('type')

    if levels:
        qs = qs.filter(level__in=levels)
    if types:
        qs = qs.filter(qualification_type__in=types)

    # بحث بسيط (اسم الموظف أو نوع المؤهل)
    q = request.GET.get('q')
    if q:
        qs = qs.filter(Q(employee__name__icontains=q) | Q(qualification_type__icontains=q) | Q(university_name__icontains=q))

    context = {
        'educations': qs,
        'levels_choices': LEVEL_CHOICES,
        'type_choices': TYPE_CHOICES,
        'selected_levels': levels,
        'selected_types': types,
        'query': q or '',
    }
    return render(request, 'education/education_list.html', context)


def education_delete(request, pk):
    obj = get_object_or_404(Education, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "تم حذف المؤهل")
        return redirect('education:list')
    return render(request, 'education/confirm_delete.html', {'object': obj})
