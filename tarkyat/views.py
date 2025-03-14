from django.shortcuts import render, redirect
from .models import Promotion
from em_data.models import Employee
from ranks.models import Rank
from django.core.exceptions import ValidationError
def tarkyat_page_view(request):
    return render(request, 'tarkyat/tarkyat.html')
def add_tarkya(request):
    if request.method == 'POST':
        employee_ids = request.POST.getlist('employee')
        to_rank = Rank.objects.get(id=request.POST['to_rank'])
        from_rank = Rank.objects.get(id=request.POST['from_rank']) if request.POST['from_rank'] else None

        for emp_id in employee_ids:
            employee = Employee.objects.get(id=emp_id)
            effective_from_rank = from_rank if from_rank else employee.rank

            # فرض التسلسل لأمناء الشرطة ومعاوني الأمن فقط
            if effective_from_rank and to_rank.rank_type in ['police_officer', 'security_assistant']:
                # إذا كان from_rank و to_rank من نفس النوع، تحقق من التسلسل
                if (effective_from_rank.rank_type == to_rank.rank_type and 
                    to_rank.order <= effective_from_rank.order):
                    raise ValidationError(
                        f"لا يمكن الترقية من {effective_from_rank.name} إلى {to_rank.name} لأنها ليست ترقية صالحة في التسلسل."
                    )
                # إذا كان الانتقال من درجة أولى إلى أمين شرطة، تحقق أن to_rank هو "أمين شرطة ثالث"
                if (effective_from_rank.rank_type == 'primary' and 
                    to_rank.rank_type == 'police_officer' and 
                    to_rank.order != 1):  # أمين شرطة ثالث = order 1
                    raise ValidationError(
                        "الانتقال من درجة أولى إلى أمين شرطة يجب أن يكون إلى 'أمين شرطة ثالث' فقط."
                    )

            promotion = Promotion(
                employee=employee,
                from_rank=effective_from_rank,
                to_rank=to_rank,
                promotion_date=request.POST['promotion_date'],
                promotion_course_number=request.POST['promotion_course_number'],
                training_start_date=request.POST['training_start_date'],
                training_end_date=request.POST['training_end_date'],
                training_course_number=request.POST['training_course_number'],
                training_location=request.POST['training_location'],
                notes=request.POST['notes']
            )
            promotion.save()
        return redirect('add_tarkya')

    employees = Employee.objects.all()
    ranks = Rank.objects.all()
    return render(request, 'tarkyat/add_tarkya.html', {'employees': employees, 'ranks': ranks})




from django.shortcuts import render, redirect
from .models import Employee, Promotion, Rank

def edit_promotions(request):
    employees = Employee.objects.all()
    selected_employee = None
    promotions = []
    ranks = Rank.objects.all()

    if request.method == 'GET' and 'employee_id' in request.GET:
        employee_id = request.GET.get('employee_id')
        if employee_id:
            selected_employee = Employee.objects.get(id=employee_id)
            promotions = Promotion.objects.filter(employee=selected_employee)

    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        employee = Employee.objects.get(id=employee_id)

        # تحديث الترقيات الحالية
        for promotion in Promotion.objects.filter(employee=employee):
            promotion_date = request.POST.get(f'promotion_date_{promotion.id}')
            from_rank_id = request.POST.get(f'from_rank_id_{promotion.id}')
            to_rank_id = request.POST.get(f'to_rank_id_{promotion.id}')
            promotion_course_number = request.POST.get(f'promotion_course_number_{promotion.id}')
            training_start_date = request.POST.get(f'training_start_date_{promotion.id}')
            training_end_date = request.POST.get(f'training_end_date_{promotion.id}')
            training_course_number = request.POST.get(f'training_course_number_{promotion.id}')
            training_location = request.POST.get(f'training_location_{promotion.id}')
            notes = request.POST.get(f'notes_{promotion.id}')

            if promotion_date and from_rank_id and to_rank_id:
                promotion.promotion_date = promotion_date
                promotion.from_rank_id = from_rank_id
                promotion.to_rank_id = to_rank_id
                promotion.promotion_course_number = promotion_course_number
                promotion.training_start_date = training_start_date or None
                promotion.training_end_date = training_end_date or None
                promotion.training_course_number = training_course_number
                promotion.training_location = training_location
                promotion.notes = notes
                promotion.save()
            else:
                promotion.delete()  # حذف إذا تم إزالته من النموذج

        # إضافة ترقيات جديدة
        new_dates = request.POST.getlist('promotion_date_new[]')
        new_from_ranks = request.POST.getlist('from_rank_id_new[]')
        new_to_ranks = request.POST.getlist('to_rank_id_new[]')
        new_promotion_courses = request.POST.getlist('promotion_course_number_new[]')
        new_training_starts = request.POST.getlist('training_start_date_new[]')
        new_training_ends = request.POST.getlist('training_end_date_new[]')
        new_training_courses = request.POST.getlist('training_course_number_new[]')
        new_training_locations = request.POST.getlist('training_location_new[]')
        new_notes = request.POST.getlist('notes_new[]')

        for date, from_rank, to_rank, prom_course, train_start, train_end, train_course, train_loc, note in zip(
            new_dates, new_from_ranks, new_to_ranks, new_promotion_courses, new_training_starts, 
            new_training_ends, new_training_courses, new_training_locations, new_notes
        ):
            if date and from_rank and to_rank:
                Promotion.objects.create(
                    employee=employee,
                    promotion_date=date,
                    from_rank_id=from_rank,
                    to_rank_id=to_rank,
                    promotion_course_number=prom_course,
                    training_start_date=train_start or None,
                    training_end_date=train_end or None,
                    training_course_number=train_course,
                    training_location=train_loc,
                    notes=note
                )

        return redirect('edit_promotions')  # إعادة تحميل الصفحة بعد الحفظ

    return render(request, 'tarkyat/edit_promotions.html', {
        'employees': employees,
        'selected_employee': selected_employee,
        'promotions': promotions,
        'ranks': ranks,
    })