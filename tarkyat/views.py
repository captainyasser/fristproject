from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Promotion, Employee
from ranks.models import Rank
from .forms import PromotionForm
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import logging

logger = logging.getLogger(__name__)

def next_tarkya(request):
    # Fetch all employees with their promotions
    employees = Employee.objects.all().prefetch_related('promotions').order_by('sort_number')
    
    # Get today's date
    today = datetime.today().date()
    
    employee_data = []
    for employee in employees:
        # Get the latest promotion
        latest_promotion = employee.promotions.order_by('-promotion_date').first()
        
        if latest_promotion:
            to_rank_id = latest_promotion.to_rank_id
            promotion_date = latest_promotion.promotion_date
            current_rank = latest_promotion.to_rank
        else:
            to_rank_id = employee.rank.id if employee.rank else None
            promotion_date = None
            current_rank = employee.rank
        
        next_promotion_date = None
        next_promotion_color = 'black'
        
        # Calculate next promotion date based on to_rank or employee rank
        if to_rank_id in [2, 3, 4, 5, 6]:
            next_promotion_date = promotion_date + relativedelta(years=6) if promotion_date else None
        elif to_rank_id == 1:
            next_promotion_date = None  # No next promotion
            next_promotion_color = 'green'
        elif to_rank_id == 10:
            next_promotion_date = promotion_date + relativedelta(years=4) if promotion_date else None
        elif to_rank_id in [8, 9]:
            next_promotion_date = promotion_date + relativedelta(years=5) if promotion_date else None
        elif to_rank_id == 7:
            next_promotion_date = None  # No next promotion
            next_promotion_color = 'green'
        elif to_rank_id in [19, 20, 21, 22]:
            next_promotion_date = promotion_date + relativedelta(years=4) if promotion_date else None
        elif to_rank_id in [24, 25, 26, 27, 28]:
            next_promotion_date = promotion_date + relativedelta(years=6) if promotion_date else None
        elif to_rank_id == 23:
            next_promotion_date = None  # No next promotion
            next_promotion_color = 'green'
        else:
            next_promotion_date = None  # No next promotion for unknown ranks
            next_promotion_color = 'green'
        
        # Adjust next_promotion_date to be either June 1 or December 1 (next closest date)
        if next_promotion_date:
            year = next_promotion_date.year
            month = next_promotion_date.month
            day = next_promotion_date.day
            
            # Define the two possible promotion dates in the same year
            june_1 = date(year, 6, 1)
            december_1 = date(year, 12, 1)
            
            # If the calculated date is not June 1 or December 1, find the next closest
            if not (month == 6 and day == 1) and not (month == 12 and day == 1):
                # Check which is closer: June 1 or December 1 of the same year
                if next_promotion_date < june_1:
                    next_promotion_date = june_1
                elif june_1 <= next_promotion_date < december_1:
                    next_promotion_date = december_1
                else:
                    # If after December 1, move to June 1 of the next year
                    next_promotion_date = date(year + 1, 6, 1)
        
        # Determine color for next promotion date
        if next_promotion_date:
            three_months_from_now = today + relativedelta(months=6)
            if next_promotion_date < today:
                next_promotion_color = 'red'
            elif next_promotion_date <= three_months_from_now:
                next_promotion_color = 'blue'
        
        employee_data.append({
            'employee': employee,
            'latest_promotion': latest_promotion,
            'current_rank': current_rank,
            'promotion_date': promotion_date,
            'next_promotion_date': next_promotion_date,
            'next_promotion_color': next_promotion_color
        })
    
    return render(request, 'tarkyat/next_tarkya.html', {
        'employee_data': employee_data
    })

def promotion_list(request):
    employees = Employee.objects.all().order_by('sort_number')
    selected_employee_id = request.GET.get('employee')
    promotions = Promotion.objects.all()
    form = PromotionForm()
    ranks = Rank.objects.all().order_by('id')
    if selected_employee_id:
        promotions = promotions.filter(employee__id=selected_employee_id).order_by('-to_rank_id')
    return render(request, 'tarkyat/promotion_list.html', {
        'promotions': promotions,
        'employees': employees,
        'selected_employee_id': selected_employee_id,
        'form': form,
        'ranks': ranks,
    })

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
            if update_rank == 'yes':
                logger.info("Updating rank for employee %s to %s", employee.id, to_rank.id)
                employee.rank = to_rank
                employee.save(update_fields=['rank'])
            return JsonResponse({'success': True})
        else:
            logger.error("Form errors: %s", form.errors)
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    return JsonResponse({'success': False, 'errors': 'طلب غير صالح'})

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
            promotion_instance.save()
            if update_rank == 'yes':
                logger.info("Updating rank for employee %s to %s", promotion_instance.employee.id, to_rank.id)
                promotion_instance.employee.rank = to_rank
                promotion_instance.employee.save(update_fields=['rank'])
            return JsonResponse({'success': True})
        else:
            logger.error("Form errors: %s", form.errors)
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})
    return JsonResponse({'success': False, 'errors': 'Invalid request'})

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
    ranks = Rank.objects.all().order_by('id')
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

def m3awn_tarkyat(request):
    employees = Employee.objects.filter(rank__rank_type='security_assistant').order_by('sort_number').prefetch_related('promotions')
    employee_data = []
    m3awn_ranks = {
        28: 'm3awn_thaleth', 27: 'm3awn_thani', 26: 'm3awn_awwal',
        25: 'm3awn_momtaz', 24: 'm3awn_momtaz_thani', 23: 'm3awn_momtaz_awwal'
    }
    for employee in employees:
        promotions_dict = {
            'm3awn_thaleth_date': None, 'm3awn_thaleth_num': None,
            'm3awn_thani_date': None, 'm3awn_thani_num': None,
            'm3awn_awwal_date': None, 'm3awn_awwal_num': None,
            'm3awn_momtaz_date': None, 'm3awn_momtaz_num': None,
            'm3awn_momtaz_thani_date': None, 'm3awn_momtaz_thani_num': None,
            'm3awn_momtaz_awwal_date': None, 'm3awn_momtaz_awwal_num': None,
        }
        for promotion in employee.promotions.all():
            if promotion.to_rank_id in m3awn_ranks:
                key = m3awn_ranks[promotion.to_rank_id]
                promotions_dict[f'{key}_date'] = promotion.promotion_date
                promotions_dict[f'{key}_num'] = promotion.promotion_course_number
        employee_data.append({'employee': employee, 'promotions': promotions_dict})
    return render(request, 'tarkyat/m3awn_tarkyat.html', {'employee_data': employee_data})

def tarkyat_training(request):
    sort_by = request.GET.get('sort_by', 'sort_number')
    if sort_by not in ['sort_number', 'name']:
        sort_by = 'sort_number'
    employees = Employee.objects.all().prefetch_related('promotions').order_by(sort_by)
    employee_data = []
    for employee in employees:
        valid_promotions = employee.promotions.filter(
            Q(training_start_date__isnull=False) |
            Q(training_end_date__isnull=False) |
            Q(training_location__isnull=False)
        ).order_by('-to_rank_id')
        valid_count = valid_promotions.count()
        remaining_rows = 15 - valid_count
        employee_data.append({
            'employee': employee,
            'valid_promotions': valid_promotions,
            'valid_count': valid_count,
            'remaining_rows': remaining_rows
        })
    return render(request, 'tarkyat/tarkyat_training.html', {
        'employee_data': employee_data,
        'sort_by': sort_by
    })




# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import JsonResponse
# from .models import Promotion, Employee
# from ranks.models import Rank
# from .forms import PromotionForm
# from django.core.exceptions import ValidationError
# import logging

# logger = logging.getLogger(__name__)




# def next_tarkya(request):
#     # Fetch all employees with their promotions
#     employees = Employee.objects.all().prefetch_related('promotions').order_by('sort_number')
    
#     # Get today's date
#     today = datetime.today().date()
    
#     employee_data = []
#     for employee in employees:
#         # Get the latest promotion
#         latest_promotion = employee.promotions.order_by('-promotion_date').first()
#         if not latest_promotion:
#             continue  # Skip employees with no promotions
        
#         to_rank_id = latest_promotion.to_rank_id
#         promotion_date = latest_promotion.promotion_date
#         next_promotion_date = None
#         next_promotion_color = 'black'
        
#         # Calculate next promotion date based on to_rank
#         if to_rank_id in [2, 3, 4, 5, 6]:
#             next_promotion_date = promotion_date + relativedelta(years=6)
#         elif to_rank_id == 1:
#             next_promotion_date = None  # No next promotion
#             next_promotion_color = 'green'
#         elif to_rank_id == 10:
#             next_promotion_date = promotion_date + relativedelta(years=4)
#         elif to_rank_id in [8, 9]:
#             next_promotion_date = promotion_date + relativedelta(years=5)
#         elif to_rank_id == 7:
#             next_promotion_date = None  # No next promotion
#             next_promotion_color = 'green'
#         elif to_rank_id in [19, 20, 21, 22]:
#             next_promotion_date = promotion_date + relativedelta(years=4)
#         elif to_rank_id in [24, 25, 26, 27, 28]:
#             next_promotion_date = promotion_date + relativedelta(years=6)
#         elif to_rank_id == 23:
#             next_promotion_date = None  # No next promotion
#             next_promotion_color = 'green'
        
#         # Determine color for next promotion date
#         if next_promotion_date:
#             three_months_from_now = today + relativedelta(months=3)
#             if next_promotion_date < today:
#                 next_promotion_color = 'red'
#             elif next_promotion_date <= three_months_from_now:
#                 next_promotion_color = 'yellow'
        
#         employee_data.append({
#             'employee': employee,
#             'latest_promotion': latest_promotion,
#             'next_promotion_date': next_promotion_date,
#             'next_promotion_color': next_promotion_color
#         })
    
#     return render(request, 'tarkyat/next_tarkya.html', {
#         'employee_data': employee_data
#     })




# # دالة عرض قائمة الترقيات (موجودة بالفعل)
# def promotion_list(request):
#     employees = Employee.objects.all().order_by('sort_number')
#     selected_employee_id = request.GET.get('employee')
#     promotions = Promotion.objects.all()
#     form = PromotionForm()  # Empty form for adding promotions
#     ranks = Rank.objects.all().order_by('id')  # Sort ranks by id

#     if selected_employee_id:
#         promotions = promotions.filter(employee__id=selected_employee_id).order_by('-to_rank_id')

#     return render(request, 'tarkyat/promotion_list.html', {
#         'promotions': promotions,
#         'employees': employees,
#         'selected_employee_id': selected_employee_id,
#         'form': form,
#         'ranks': ranks,
#     })

# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import JsonResponse
# from .models import Promotion, Employee
# from ranks.models import Rank
# from .forms import PromotionForm
# from django.core.exceptions import ValidationError
# import logging

# logger = logging.getLogger(__name__)

# def add_promotion(request):
#     if request.method == 'POST':
#         logger.info("POST data: %s", request.POST)
#         form = PromotionForm(request.POST)
#         selected_employee_id = request.POST.get('employee')
        
#         try:
#             employee = Employee.objects.get(id=selected_employee_id)
#         except Employee.DoesNotExist:
#             return JsonResponse({'success': False, 'errors': 'الموظف غير موجود.'})

#         update_rank = request.POST.get('update_rank')
#         promotion_type = request.POST.get('promotion_type') or None

#         if form.is_valid():
#             promotion = form.save(commit=False)
#             promotion.employee = employee
#             promotion.promotion_type = promotion_type

#             # التحقق من صحة الترقية
#             from_rank = promotion.from_rank if promotion.from_rank else employee.rank
#             to_rank = promotion.to_rank

#             if not to_rank:
#                 return JsonResponse({'success': False, 'errors': 'الدرجة الجديدة مطلوبة.'})

#             if from_rank and to_rank.rank_type in ['police_officer', 'security_assistant']:
#                 if (from_rank.rank_type == to_rank.rank_type and to_rank.order <= from_rank.order):
#                     return JsonResponse({
#                         'success': False,
#                         'errors': f"لا يمكن الترقية من {from_rank.name} إلى {to_rank.name} لأنها ليست ترقية صالحة في التسلسل."
#                     })
#                 if (from_rank.rank_type == 'primary' and to_rank.rank_type == 'police_officer' and to_rank.order != 1):
#                     return JsonResponse({
#                         'success': False,
#                         'errors': "الانتقال من درجة أولى إلى أمين شرطة يجب أن يكون إلى 'أمين شرطة ثالث' فقط."
#                     })

#             # تعيين القيم الاختيارية إلى None إذا لم تُدخل
#             promotion.training_start_date = promotion.training_start_date or None
#             promotion.training_end_date = promotion.training_end_date or None
#             promotion.training_course_number = promotion.training_course_number or None
#             promotion.training_location = promotion.training_location or None
#             promotion.notes = promotion.notes or None

#             try:
#                 promotion.save()
#             except Exception as e:
#                 logger.error("Error saving promotion: %s", str(e))
#                 return JsonResponse({'success': False, 'errors': f'خطأ أثناء الحفظ: {str(e)}'})

#             # تحديث الدرجة إذا اختير "نعم"
#             if update_rank == 'yes':
#                 logger.info("Updating rank for employee %s to %s", employee.id, to_rank.id)
#                 employee.rank = to_rank
#                 employee.save(update_fields=['rank'])

#             return JsonResponse({'success': True})
#         else:
#             logger.error("Form errors: %s", form.errors)
#             return JsonResponse({'success': False, 'errors': form.errors.as_json()})
#     return JsonResponse({'success': False, 'errors': 'طلب غير صالح'})


# # دالة تعديل ترقية عبر AJAX
# def edit_promotion(request, pk):
#     promotion = get_object_or_404(Promotion, pk=pk)
#     if request.method == 'POST':
#         logger.info("POST data: %s", request.POST)
#         form = PromotionForm(request.POST, instance=promotion)
#         update_rank = request.POST.get('update_rank')
#         promotion_type = request.POST.get('promotion_type') or None

#         if form.is_valid():
#             promotion_instance = form.save(commit=False)
#             promotion_instance.promotion_type = promotion_type

#             # التحقق من صحة الترقية
#             from_rank = promotion_instance.from_rank if promotion_instance.from_rank else promotion.employee.rank
#             to_rank = promotion_instance.to_rank
#             if from_rank and to_rank.rank_type in ['police_officer', 'security_assistant']:
#                 if (from_rank.rank_type == to_rank.rank_type and to_rank.order <= from_rank.order):
#                     return JsonResponse({
#                         'success': False,
#                         'errors': f"لا يمكن الترقية من {from_rank.name} إلى {to_rank.name} لأنها ليست ترقية صالحة في التسلسل."
#                     })
#                 if (from_rank.rank_type == 'primary' and to_rank.rank_type == 'police_officer' and to_rank.order != 1):
#                     return JsonResponse({
#                         'success': False,
#                         'errors': "الانتقال من درجة أولى إلى أمين شرطة يجب أن يكون إلى 'أمين شرطة ثالث' فقط."
#                     })

#             # حفظ التعديلات
#             promotion_instance.save()

#             # تحديث الدرجة إذا اختير "نعم" (اختياري: يمكنك تحديد ما إذا كنت تريد هذا في التعديل)
#             if update_rank == 'yes':
#                 logger.info("Updating rank for employee %s to %s", promotion_instance.employee.id, to_rank.id)
#                 promotion_instance.employee.rank = to_rank
#                 promotion_instance.employee.save(update_fields=['rank'])

#             return JsonResponse({'success': True})
#         else:
#             logger.error("Form errors: %s", form.errors)
#             return JsonResponse({'success': False, 'errors': form.errors.as_json()})
#     return JsonResponse({'success': False, 'errors': 'Invalid request'})

# # بقية الدوال (يمكنك الاحتفاظ بها كما هي)
# def tarkyat(request):
#     return render(request, 'tarkyat/tarkyat.html', {})

# def add_tarkya_for_many(request):
#     if request.method == 'POST':
#         logger.info("POST data: %s", request.POST)
#         employee_ids = request.POST.getlist('employee')
#         to_rank = Rank.objects.get(id=request.POST['to_rank'])
#         from_rank = Rank.objects.get(id=request.POST['from_rank']) if request.POST['from_rank'] else None
#         update_rank = request.POST.get('update_rank')
#         promotion_type = request.POST.get('promotion_type') or None
        
#         for emp_id in employee_ids:
#             employee = Employee.objects.get(id=emp_id)
#             effective_from_rank = from_rank if from_rank else employee.rank

#             if effective_from_rank and to_rank.rank_type in ['police_officer', 'security_assistant']:
#                 if (effective_from_rank.rank_type == to_rank.rank_type and 
#                     to_rank.order <= effective_from_rank.order):
#                     raise ValidationError(
#                         f"لا يمكن الترقية من {effective_from_rank.name} إلى {to_rank.name} لأنها ليست ترقية صالحة في التسلسل."
#                     )
#                 if (effective_from_rank.rank_type == 'primary' and 
#                     to_rank.rank_type == 'police_officer' and 
#                     to_rank.order != 1):
#                     raise ValidationError(
#                         "الانتقال من درجة أولى إلى أمين شرطة يجب أن يكون إلى 'أمين شرطة ثالث' فقط."
#                     )

#             promotion_data = {
#                 'employee': employee,
#                 'from_rank': effective_from_rank,
#                 'to_rank': to_rank,
#                 'promotion_date': request.POST['promotion_date'],
#                 'promotion_course_number': request.POST.get('promotion_course_number') or None,
#                 'training_start_date': request.POST.get('training_start_date') or None,
#                 'training_end_date': request.POST.get('training_end_date') or None,
#                 'training_course_number': request.POST.get('training_course_number') or None,
#                 'training_location': request.POST.get('training_location') or None,
#                 'notes': request.POST.get('notes') or None,
#                 'promotion_type': promotion_type
#             }

#             promotion = Promotion(**promotion_data)
#             promotion.save()

#             if update_rank == 'yes':
#                 logger.info("Updating rank for employee %s to %s", employee.id, to_rank.id)
#                 employee.rank = to_rank
#                 employee.save(update_fields=['rank'])

#         return redirect('add_tarkya_for_many')

#     employees = Employee.objects.all()
#     ranks = Rank.objects.all().order_by('id')
#     return render(request, 'tarkyat/add_tarkya.html', {'employees': employees, 'ranks': ranks})

# def delete_promotion(request, pk):
#     promotion = get_object_or_404(Promotion, pk=pk)
#     employee_id = promotion.employee.id
#     if request.method == 'POST':
#         promotion.delete()
#         return redirect(f'/tarkyat/promotions/?employee={employee_id}')
#     return render(request, 'tarkyat/confirm_delete.html', {'object': promotion})

# def ameen_tarkyat(request):
#     employees = Employee.objects.filter(rank__rank_type='police_officer').order_by('sort_number').prefetch_related('promotions')
#     employee_data = []
#     ameen_ranks = {
#         5: 'ameen_2', 4: 'ameen_1', 3: 'ameen_mom', 2: 'ameen_mom_2', 1: 'ameen_mom_1'
#     }

#     for employee in employees:
#         promotions_dict = {
#             'ameen_2_date': None, 'ameen_2_num': None, 'ameen_1_date': None, 'ameen_1_num': None,
#             'ameen_mom_date': None, 'ameen_mom_num': None, 'ameen_mom_2_date': None, 'ameen_mom_2_num': None,
#             'ameen_mom_1_date': None, 'ameen_mom_1_num': None,
#         }
#         for promotion in employee.promotions.all():
#             if promotion.to_rank_id in ameen_ranks:
#                 key = ameen_ranks[promotion.to_rank_id]
#                 promotions_dict[f'{key}_date'] = promotion.promotion_date
#                 promotions_dict[f'{key}_num'] = promotion.promotion_course_number
#         employee_data.append({'employee': employee, 'promotions': promotions_dict})

#     return render(request, 'tarkyat/ameen_tarkyat.html', {'employee_data': employee_data})

# def daragaola_tarkya(request):
#     employees = Employee.objects.filter(rank__rank_type='primary').order_by('sort_number').prefetch_related('promotions')
#     daraga_ranks = {
#         21: 'areef', 20: 'raqeeb', 19: 'raqeeb_awwal', 10: 'mosaed_thaleth',
#         9: 'mosaed_thani', 8: 'mosaed_awwal', 7: 'mosaed_momtaz'
#     }
#     employee_data = []
#     for employee in employees:
#         promotions_dict = {
#             'areef_date': None, 'areef_num': None, 'raqeeb_date': None, 'raqeeb_num': None,
#             'raqeeb_awwal_date': None, 'raqeeb_awwal_num': None, 'mosaed_thaleth_date': None, 'mosaed_thaleth_num': None,
#             'mosaed_thani_date': None, 'mosaed_thani_num': None, 'mosaed_awwal_date': None, 'mosaed_awwal_num': None,
#             'mosaed_momtaz_date': None, 'mosaed_momtaz_num': None,
#         }
#         for promotion in employee.promotions.all():
#             if promotion.to_rank_id in daraga_ranks:
#                 key = daraga_ranks[promotion.to_rank_id]
#                 promotions_dict[f'{key}_date'] = promotion.promotion_date
#                 promotions_dict[f'{key}_num'] = promotion.promotion_course_number
#         employee_data.append({'employee': employee, 'promotions': promotions_dict})

#     return render(request, 'tarkyat/daragaola-tarkya.html', {'employee_data': employee_data})

# # tarkyat/views.py (إضافة دالة العرض)
# # tarkyat/views.py (تعديل دالة العرض)
# from django.shortcuts import render
# from em_data.models import Employee
# from .models import Promotion
# from django.db.models import Q

# def tarkyat_training(request):
#     # Get sort_by parameter from the request, default to 'sort_number'
#     sort_by = request.GET.get('sort_by', 'sort_number')
    
#     # Validate sort_by to prevent injection; allow only 'sort_number' or 'name'
#     if sort_by not in ['sort_number', 'name']:
#         sort_by = 'sort_number'
    
#     # Fetch all employees with their promotions, ordered by the chosen field
#     employees = Employee.objects.all().prefetch_related('promotions').order_by(sort_by)
    
#     # Create a list to store employee data with filtered promotions
#     employee_data = []
#     for employee in employees:
#         # Filter promotions related to training
#         valid_promotions = employee.promotions.filter(
#             Q(training_start_date__isnull=False) |
#             Q(training_end_date__isnull=False) |
#             Q(training_location__isnull=False)
#         ).order_by('-to_rank_id')
#         valid_count = valid_promotions.count()
#         remaining_rows = 15 - valid_count  # Calculate remaining rows in Python
#         employee_data.append({
#             'employee': employee,
#             'valid_promotions': valid_promotions,
#             'valid_count': valid_count,
#             'remaining_rows': remaining_rows
#         })
    
#     return render(request, 'tarkyat/tarkyat_training.html', {
#         'employee_data': employee_data,
#         'sort_by': sort_by  # Pass current sort_by to template
#     })