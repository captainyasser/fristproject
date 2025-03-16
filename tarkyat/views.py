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
    
    
    



def ameen_tarkyat(request):
    # تصفية الموظفين الذين لهم درجة من نوع 'police_officer' وفرزهم حسب sort_number
    employees = Employee.objects.filter(rank__rank_type='police_officer').order_by('sort_number').prefetch_related('promotions')
    
    # إعداد البيانات لكل موظف
    employee_data = []
    ameen_ranks = {
        5: 'ameen_2',  # أمين شرطة ثان
        4: 'ameen_1',  # أمين شرطة أول
        3: 'ameen_mom',  # أمين شرطة ممتاز
        2: 'ameen_mom_2',  # أمين شرطة ممتاز ثان
        1: 'ameen_mom_1',  # أمين شرطة ممتاز أول
    }

    for employee in employees:
        promotions_dict = {
            'ameen_2_date': None, 'ameen_2_num': None,
            'ameen_1_date': None, 'ameen_1_num': None,
            'ameen_mom_date': None, 'ameen_mom_num': None,
            'ameen_mom_2_date': None, 'ameen_mom_2_num': None,
            'ameen_mom_1_date': None, 'ameen_mom_1_num': None,
        }
        
        # جلب الترقيات للموظف
        for promotion in employee.promotions.all():
            if promotion.to_rank_id in ameen_ranks:
                key = ameen_ranks[promotion.to_rank_id]
                promotions_dict[f'{key}_date'] = promotion.promotion_date
                promotions_dict[f'{key}_num'] = promotion.promotion_course_number

        employee_data.append({
            'employee': employee,
            'promotions': promotions_dict
        })

    return render(request, 'tarkyat/ameen_tarkyat.html', {'employee_data': employee_data})





from django.shortcuts import render
from .models import Employee, Promotion, Rank

def daragaola_tarkya(request):
    # تصفية الموظفين الذين لهم درجة من نوع 'primary' وفرزهم حسب sort_number
    employees = Employee.objects.filter(rank__rank_type='primary').order_by('sort_number').prefetch_related('promotions')
    
    # إعداد قاموس الرتب بناءً على معرفات الرتب (يجب تعديل المعرفات حسب قاعدة البيانات الخاصة بك)
    daraga_ranks = {
        8: 'areef',         # عريف
        9: 'raqeeb',        # رقيب
        10: 'raqeeb_awwal',  # رقيب أول
        19: 'mosaed_thaleth',# مساعد ثالث
        20: 'mosaed_thani',  # مساعد ثان
        21: 'mosaed_awwal',  # مساعد أول
        22: 'mosaed_momtaz', # مساعد ممتاز
    }

    # إعداد البيانات لكل موظف
    employee_data = []
    for employee in employees:
        promotions_dict = {
            'areef_date': None, 'areef_num': None,
            'raqeeb_date': None, 'raqeeb_num': None,
            'raqeeb_awwal_date': None, 'raqeeb_awwal_num': None,
            'mosaed_thaleth_date': None, 'mosaed_thaleth_num': None,
            'mosaed_thani_date': None, 'mosaed_thani_num': None,
            'mosaed_awwal_date': None, 'mosaed_awwal_num': None,
            'mosaed_momtaz_date': None, 'mosaed_momtaz_num': None,
        }
        
        # جلب الترقيات للموظف
        for promotion in employee.promotions.all():
            if promotion.to_rank_id in daraga_ranks:
                key = daraga_ranks[promotion.to_rank_id]
                promotions_dict[f'{key}_date'] = promotion.promotion_date
                promotions_dict[f'{key}_num'] = promotion.promotion_course_number

        employee_data.append({
            'employee': employee,
            'promotions': promotions_dict
        })

    context = {'employee_data': employee_data}
    return render(request, 'tarkyat/daragaola-tarkya.html', context)