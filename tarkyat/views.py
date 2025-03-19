from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Promotion, Employee
from ranks.models import Rank
from .forms import PromotionForm
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

# دالة عرض قائمة الترقيات (موجودة بالفعل)
def promotion_list(request):
    employees = Employee.objects.all().order_by('sort_number')
    selected_employee_id = request.GET.get('employee')
    promotions = Promotion.objects.all()
    form = PromotionForm()  # نموذج فارغ للإضافة
    ranks = Rank.objects.all()  # قائمة الرتب للتعديل

    if selected_employee_id:
        promotions = promotions.filter(employee__id=selected_employee_id)

    return render(request, 'tarkyat/promotion_list.html', {
        'promotions': promotions,
        'employees': employees,
        'selected_employee_id': selected_employee_id,
        'form': form,
        'ranks': ranks,
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Promotion, Employee
from ranks.models import Rank
from .forms import PromotionForm
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

def add_promotion(request):
    if request.method == 'POST':
        logger.info("POST data: %s", request.POST)
        form = PromotionForm(request.POST)
        selected_employee_id = request.POST.get('employee')
        
        try:
            employee = Employee.objects.get(id=selected_employee_id)
        except Employee.DoesNotExist:
            return JsonResponse({'success': False, 'errors': 'الموظف غير موجود.'})

        update_rank = request.POST.get('update_rank')
        promotion_type = request.POST.get('promotion_type') or None

        if form.is_valid():
            promotion = form.save(commit=False)
            promotion.employee = employee
            promotion.promotion_type = promotion_type

            # التحقق من صحة الترقية
            from_rank = promotion.from_rank if promotion.from_rank else employee.rank
            to_rank = promotion.to_rank

            if not to_rank:
                return JsonResponse({'success': False, 'errors': 'الدرجة الجديدة مطلوبة.'})

            if from_rank and to_rank.rank_type in ['police_officer', 'security_assistant']:
                if (from_rank.rank_type == to_rank.rank_type and to_rank.order <= from_rank.order):
                    return JsonResponse({
                        'success': False,
                        'errors': f"لا يمكن الترقية من {from_rank.name} إلى {to_rank.name} لأنها ليست ترقية صالحة في التسلسل."
                    })
                if (from_rank.rank_type == 'primary' and to_rank.rank_type == 'police_officer' and to_rank.order != 1):
                    return JsonResponse({
                        'success': False,
                        'errors': "الانتقال من درجة أولى إلى أمين شرطة يجب أن يكون إلى 'أمين شرطة ثالث' فقط."
                    })

            # تعيين القيم الاختيارية إلى None إذا لم تُدخل
            promotion.training_start_date = promotion.training_start_date or None
            promotion.training_end_date = promotion.training_end_date or None
            promotion.training_course_number = promotion.training_course_number or None
            promotion.training_location = promotion.training_location or None
            promotion.notes = promotion.notes or None

            try:
                promotion.save()
            except Exception as e:
                logger.error("Error saving promotion: %s", str(e))
                return JsonResponse({'success': False, 'errors': f'خطأ أثناء الحفظ: {str(e)}'})

            # تحديث الدرجة إذا اختير "نعم"
            if update_rank == 'yes':
                logger.info("Updating rank for employee %s to %s", employee.id, to_rank.id)
                employee.rank = to_rank
                employee.save(update_fields=['rank'])

            return JsonResponse({'success': True})
        else:
            logger.error("Form errors: %s", form.errors)
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    return JsonResponse({'success': False, 'errors': 'طلب غير صالح'})


# دالة تعديل ترقية عبر AJAX
def edit_promotion(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)
    if request.method == 'POST':
        logger.info("POST data: %s", request.POST)
        form = PromotionForm(request.POST, instance=promotion)
        update_rank = request.POST.get('update_rank')
        promotion_type = request.POST.get('promotion_type') or None

        if form.is_valid():
            promotion_instance = form.save(commit=False)
            promotion_instance.promotion_type = promotion_type

            # التحقق من صحة الترقية
            from_rank = promotion_instance.from_rank if promotion_instance.from_rank else promotion.employee.rank
            to_rank = promotion_instance.to_rank
            if from_rank and to_rank.rank_type in ['police_officer', 'security_assistant']:
                if (from_rank.rank_type == to_rank.rank_type and to_rank.order <= from_rank.order):
                    return JsonResponse({
                        'success': False,
                        'errors': f"لا يمكن الترقية من {from_rank.name} إلى {to_rank.name} لأنها ليست ترقية صالحة في التسلسل."
                    })
                if (from_rank.rank_type == 'primary' and to_rank.rank_type == 'police_officer' and to_rank.order != 1):
                    return JsonResponse({
                        'success': False,
                        'errors': "الانتقال من درجة أولى إلى أمين شرطة يجب أن يكون إلى 'أمين شرطة ثالث' فقط."
                    })

            # حفظ التعديلات
            promotion_instance.save()

            # تحديث الدرجة إذا اختير "نعم" (اختياري: يمكنك تحديد ما إذا كنت تريد هذا في التعديل)
            if update_rank == 'yes':
                logger.info("Updating rank for employee %s to %s", promotion_instance.employee.id, to_rank.id)
                promotion_instance.employee.rank = to_rank
                promotion_instance.employee.save(update_fields=['rank'])

            return JsonResponse({'success': True})
        else:
            logger.error("Form errors: %s", form.errors)
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    return JsonResponse({'success': False, 'errors': 'Invalid request'})

# بقية الدوال (يمكنك الاحتفاظ بها كما هي)
def tarkyat(request):
    return render(request, 'tarkyat/tarkyat.html', {})

def add_tarkya_for_many(request):
    if request.method == 'POST':
        logger.info("POST data: %s", request.POST)
        employee_ids = request.POST.getlist('employee')
        to_rank = Rank.objects.get(id=request.POST['to_rank'])
        from_rank = Rank.objects.get(id=request.POST['from_rank']) if request.POST['from_rank'] else None
        update_rank = request.POST.get('update_rank')
        promotion_type = request.POST.get('promotion_type') or None
        
        for emp_id in employee_ids:
            employee = Employee.objects.get(id=emp_id)
            effective_from_rank = from_rank if from_rank else employee.rank

            if effective_from_rank and to_rank.rank_type in ['police_officer', 'security_assistant']:
                if (effective_from_rank.rank_type == to_rank.rank_type and 
                    to_rank.order <= effective_from_rank.order):
                    raise ValidationError(
                        f"لا يمكن الترقية من {effective_from_rank.name} إلى {to_rank.name} لأنها ليست ترقية صالحة في التسلسل."
                    )
                if (effective_from_rank.rank_type == 'primary' and 
                    to_rank.rank_type == 'police_officer' and 
                    to_rank.order != 1):
                    raise ValidationError(
                        "الانتقال من درجة أولى إلى أمين شرطة يجب أن يكون إلى 'أمين شرطة ثالث' فقط."
                    )

            promotion_data = {
                'employee': employee,
                'from_rank': effective_from_rank,
                'to_rank': to_rank,
                'promotion_date': request.POST['promotion_date'],
                'promotion_course_number': request.POST.get('promotion_course_number') or None,
                'training_start_date': request.POST.get('training_start_date') or None,
                'training_end_date': request.POST.get('training_end_date') or None,
                'training_course_number': request.POST.get('training_course_number') or None,
                'training_location': request.POST.get('training_location') or None,
                'notes': request.POST.get('notes') or None,
                'promotion_type': promotion_type
            }

            promotion = Promotion(**promotion_data)
            promotion.save()

            if update_rank == 'yes':
                logger.info("Updating rank for employee %s to %s", employee.id, to_rank.id)
                employee.rank = to_rank
                employee.save(update_fields=['rank'])

        return redirect('add_tarkya_for_many')

    employees = Employee.objects.all()
    ranks = Rank.objects.all()
    return render(request, 'tarkyat/add_tarkya.html', {'employees': employees, 'ranks': ranks})

def delete_promotion(request, pk):
    promotion = get_object_or_404(Promotion, pk=pk)
    employee_id = promotion.employee.id
    if request.method == 'POST':
        promotion.delete()
        return redirect(f'/tarkyat/promotions/?employee={employee_id}')
    return render(request, 'tarkyat/confirm_delete.html', {'object': promotion})

def ameen_tarkyat(request):
    employees = Employee.objects.filter(rank__rank_type='police_officer').order_by('sort_number').prefetch_related('promotions')
    employee_data = []
    ameen_ranks = {
        5: 'ameen_2', 4: 'ameen_1', 3: 'ameen_mom', 2: 'ameen_mom_2', 1: 'ameen_mom_1'
    }

    for employee in employees:
        promotions_dict = {
            'ameen_2_date': None, 'ameen_2_num': None, 'ameen_1_date': None, 'ameen_1_num': None,
            'ameen_mom_date': None, 'ameen_mom_num': None, 'ameen_mom_2_date': None, 'ameen_mom_2_num': None,
            'ameen_mom_1_date': None, 'ameen_mom_1_num': None,
        }
        for promotion in employee.promotions.all():
            if promotion.to_rank_id in ameen_ranks:
                key = ameen_ranks[promotion.to_rank_id]
                promotions_dict[f'{key}_date'] = promotion.promotion_date
                promotions_dict[f'{key}_num'] = promotion.promotion_course_number
        employee_data.append({'employee': employee, 'promotions': promotions_dict})

    return render(request, 'tarkyat/ameen_tarkyat.html', {'employee_data': employee_data})

def daragaola_tarkya(request):
    employees = Employee.objects.filter(rank__rank_type='primary').order_by('sort_number').prefetch_related('promotions')
    daraga_ranks = {
        21: 'areef', 20: 'raqeeb', 19: 'raqeeb_awwal', 10: 'mosaed_thaleth',
        9: 'mosaed_thani', 8: 'mosaed_awwal', 7: 'mosaed_momtaz'
    }
    employee_data = []
    for employee in employees:
        promotions_dict = {
            'areef_date': None, 'areef_num': None, 'raqeeb_date': None, 'raqeeb_num': None,
            'raqeeb_awwal_date': None, 'raqeeb_awwal_num': None, 'mosaed_thaleth_date': None, 'mosaed_thaleth_num': None,
            'mosaed_thani_date': None, 'mosaed_thani_num': None, 'mosaed_awwal_date': None, 'mosaed_awwal_num': None,
            'mosaed_momtaz_date': None, 'mosaed_momtaz_num': None,
        }
        for promotion in employee.promotions.all():
            if promotion.to_rank_id in daraga_ranks:
                key = daraga_ranks[promotion.to_rank_id]
                promotions_dict[f'{key}_date'] = promotion.promotion_date
                promotions_dict[f'{key}_num'] = promotion.promotion_course_number
        employee_data.append({'employee': employee, 'promotions': promotions_dict})

    return render(request, 'tarkyat/daragaola-tarkya.html', {'employee_data': employee_data})