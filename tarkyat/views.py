from django.shortcuts import render, redirect
from .models import Promotion
from em_data.models import Employee
from ranks.models import Rank
from django.core.exceptions import ValidationError


def tarkyat(request):
    """
    دالة لعرض صفحة الترقيات الرئيسية التي تحتوي على أزرار التنقل.
    """
    return render(request, 'tarkyat/tarkyat.html', {})

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





from django.shortcuts import render, redirect, get_object_or_404
from .models import Promotion, Employee
from .forms import PromotionForm

def promotion_list(request):
    employees = Employee.objects.all().order_by('sort_number')
    selected_employee_id = request.GET.get('employee')
    promotions = Promotion.objects.all()
    promotion_forms = []

    if selected_employee_id:
        promotions = promotions.filter(employee__id=selected_employee_id)

        if request.method == 'POST':
            print("POST data:", request.POST)  # لتصحيح الأخطاء

            any_form_valid = False
            for promotion in promotions:
                prefix = f"promotion-{promotion.id}"
                form = PromotionForm(request.POST, instance=promotion, prefix=prefix)

                if form.is_valid():
                    promotion_instance = form.save(commit=False)
                    
                    # التأكد من تعيين `employee` يدويًا إذا لم يتم تمريره
                    if not promotion_instance.employee:
                        promotion_instance.employee = promotion.employee  # تعيين الموظف من السجل الأصلي
                    
                    promotion_instance.save()
                    any_form_valid = True
                else:
                    print(f"Form errors for promotion {promotion.id}: {form.errors}")

            if any_form_valid:
                return redirect(request.path + f'?employee={selected_employee_id}')

            # إعادة عرض النماذج بأخطاء الإدخال
            promotion_forms = [PromotionForm(request.POST, instance=p, prefix=f"promotion-{p.id}") for p in promotions]
        else:
            promotion_forms = [PromotionForm(instance=p, prefix=f"promotion-{p.id}") for p in promotions]

    return render(request, 'tarkyat/promotion_list.html', {
        'promotions': promotions,
        'employees': employees,
        'selected_employee_id': selected_employee_id,
        'promotion_forms': promotion_forms,
    })


from django.shortcuts import render, redirect, get_object_or_404
from .models import Promotion, Employee
from .forms import PromotionForm
import logging
from django.shortcuts import render, redirect, get_object_or_404
from .models import Promotion, Employee
from .forms import PromotionForm
import logging

logger = logging.getLogger(__name__)

def edit_promotion(request, pk=None):
    promotion = get_object_or_404(Promotion, pk=pk) if pk else None
    selected_employee_id = request.GET.get('employee')

    if request.method == 'POST':
        logger.info("POST data: %s", request.POST)
        form = PromotionForm(request.POST, instance=promotion, selected_employee_id=selected_employee_id)
        update_rank = request.POST.get('update_rank')
        logger.info("update_rank: %s", update_rank)

        if form.is_valid():
            promotion_instance = form.save(commit=False)

            if not promotion_instance.employee and selected_employee_id:
                try:
                    promotion_instance.employee = Employee.objects.get(id=selected_employee_id)
                except Employee.DoesNotExist:
                    pass

            # حفظ الترقية بدون تمرير update_rank
            promotion_instance.save()

            # تحديث rank مباشرة إذا اختير "نعم"
            if update_rank == 'yes' and not promotion:  # تحديث فقط عند الإضافة (لا التحرير)
                logger.info("Updating rank for employee %s to %s", promotion_instance.employee.id, promotion_instance.to_rank.id)
                promotion_instance.employee.rank = promotion_instance.to_rank
                promotion_instance.employee.save(update_fields=['rank'])

            employee_id = promotion_instance.employee.id
            return redirect(f'/tarkyat/promotions/?employee={employee_id}')
        else:
            logger.error("Form errors: %s", form.errors)
    else:
        form = PromotionForm(instance=promotion, selected_employee_id=selected_employee_id)

    return render(request, 'tarkyat/edit_promotions.html', {
        'form': form,
        'selected_employee_id': selected_employee_id,
    })


def delete_promotion(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)
    employee_id = promotion.employee.id
    if request.method == 'POST':
        promotion.delete()
        return redirect(f'/tarkyat/promotions/?employee={employee_id}')
    return render(request, 'tarkyat/confirm_delete.html', {'object': promotion})




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





def daragaola_tarkya(request):
    employees = Employee.objects.filter(rank__rank_type='primary').order_by('sort_number').prefetch_related('promotions')
    
    daraga_ranks = {
        21: 'areef',         # عريف
        20: 'raqeeb',        # رقيب
        19: 'raqeeb_awwal', # رقيب أول
        10: 'mosaed_thaleth', # مساعد ثالث
        9: 'mosaed_thani',  # مساعد ثان
        8: 'mosaed_awwal',  # مساعد أول
        7: 'mosaed_momtaz', # مساعد ممتاز
    }

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


