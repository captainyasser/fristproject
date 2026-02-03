# E:\yasser\emapi2025\myproject\periodic_allowances\views.py
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib import messages
from decimal import Decimal
from datetime import datetime, timedelta, date
from em_data.models import Employee
from .models import PeriodicAllowance
import json


class AllowanceComparisonView(ListView):
    model = Employee
    template_name = 'periodic_allowances/allowance_comparison.html'
    context_object_name = 'employees'
    paginate_by = None
    
    def post(self, request, *args, **kwargs):
        employee_id = request.POST.get('employee_id')
        year = int(request.POST.get('year', datetime.now().year))
        target_date_str = request.POST.get('target_date', None)
        action = request.POST.get('action', '')  # 'save_calculated' أو 'update_stored' أو 'update_single_year' أو 'save_all_calculated'
        
        if not employee_id and action != 'save_all_calculated':
            messages.error(request, 'يرجى اختيار فرد أولاً.')
            return redirect(request.get_full_path())
        
        try:
            if action == 'save_all_calculated':
                # حفظ جماعي للجميع في جميع الأعوام المؤهلة (حتى العام الحالي)
                current_year = date.today().year
                eligible_employees = Employee.objects.filter(
                    date_of_appointment__isnull=False,
                    rank__isnull=False,
                    date_of_birth__isnull=False
                ).select_related('rank').order_by('sort_number')
                
                updated_count = 0
                for emp in eligible_employees:
                    appointment_year = emp.date_of_appointment.year + 1
                    retirement_date = emp.date_of_birth + timedelta(days=60 * 365.25)
                    retirement_year = retirement_date.year
                    
                    years_list = list(range(appointment_year, current_year + 1))  # حتى العام الحالي
                    
                    for yr in years_list:
                        allowance_date = PeriodicAllowance.get_allowance_date(yr)
                        
                        dummy = PeriodicAllowance(employee=emp, allowance_year=yr, stored_value=Decimal('0.00'))
                        if not dummy.is_eligible(allowance_date):
                            continue
                        
                        calculated_value = PeriodicAllowance.get_calculated_value(emp, allowance_date)
                        
                        obj, created = PeriodicAllowance.objects.update_or_create(
                            employee=emp,
                            allowance_year=yr,
                            defaults={'stored_value': calculated_value}
                        )
                        updated_count += 1
                
                if updated_count > 0:
                    messages.success(request, f'تم حفظ/تحديث {updated_count} علاوة محسوبة للأفراد في جميع الأعوام بنجاح.')
                else:
                    messages.warning(request, 'لا توجد علاوات مؤهلة للحفظ.')
                return redirect(request.get_full_path())
            
            selected_employee = Employee.objects.get(id=employee_id)
            appointment_year = selected_employee.date_of_appointment.year + 1
            retirement_date = selected_employee.date_of_birth + timedelta(days=60 * 365.25)
            retirement_year = retirement_date.year
            
            years_list = list(range(appointment_year, retirement_year + 1))
            updated_count = 0
            
            if action == 'save_calculated':
                # الحفظ التلقائي للقيم المحسوبة (مع الدرجة الصحيحة لكل عام)
                for yr in years_list:
                    allowance_date = PeriodicAllowance.get_allowance_date(yr)
                    
                    dummy = PeriodicAllowance(employee=selected_employee, allowance_year=yr, stored_value=Decimal('0.00'))
                    if not dummy.is_eligible(allowance_date):
                        continue
                    
                    calculated_value = PeriodicAllowance.get_calculated_value(selected_employee, allowance_date)
                    
                    obj, created = PeriodicAllowance.objects.update_or_create(
                        employee=selected_employee,
                        allowance_year=yr,
                        defaults={'stored_value': calculated_value}
                    )
                    updated_count += 1  # عد حتى لو حدث
                
                if updated_count > 0:
                    messages.success(request, f'تم حفظ/تحديث {updated_count} علاوة محسوبة للفرد {selected_employee.name} بنجاح.')
                else:
                    messages.warning(request, 'لا توجد علاوات مؤهلة للحفظ.')
            
            elif action == 'update_stored':
                # التحديث اليدوي للقيم المخزنة من الإدخالات (فقط للأعوام الماضية/الحالية) - للحالات الشاذة
                current_year = date.today().year
                for yr in years_list:
                    if yr > current_year:
                        continue  # تخطي المستقبلية
                    stored_input = request.POST.get(f'stored_{yr}')
                    if stored_input is not None:  # إذا POSTed
                        try:
                            if stored_input.strip() == '':  # إذا فارغ، set NULL
                                new_value = None
                            else:
                                new_value = Decimal(stored_input)
                            obj, created = PeriodicAllowance.objects.update_or_create(
                                employee=selected_employee,
                                allowance_year=yr,
                                defaults={'stored_value': new_value}
                            )
                            updated_count += 1  # عد حتى لو NULL أو نفس القيمة، طالما أدخلت
                        except ValueError:
                            messages.error(request, f'قيمة غير صالحة للعام {yr}: {stored_input}')
                
                if updated_count > 0:
                    messages.success(request, f'تم تحديث {updated_count} قيمة مخزنة للفرد {selected_employee.name} بنجاح (بما في ذلك NULL للفارغ).')
                else:
                    messages.warning(request, 'لا توجد تغييرات للتحديث. تأكد من إدخال قيم في الأعوام الماضية/الحالية.')
            
            elif action == 'update_single_year':
                # تحديث عام واحد فقط
                single_year = int(request.POST.get('single_year', 0))
                stored_input = request.POST.get('stored_single')
                if single_year and single_year in years_list:
                    if single_year > date.today().year:
                        messages.warning(request, f'لا يمكن تحديث عام مستقبلي: {single_year}')
                    else:
                        try:
                            if stored_input is None or (stored_input and stored_input.strip() == ''):  # إصلاح: التحقق من None قبل strip
                                new_value = None
                            else:
                                new_value = Decimal(stored_input)
                            obj, created = PeriodicAllowance.objects.update_or_create(
                                employee=selected_employee,
                                allowance_year=single_year,
                                defaults={'stored_value': new_value}
                            )
                            updated_count = 1
                            messages.success(request, f'تم تحديث قيمة العام {single_year} للفرد {selected_employee.name} بنجاح.')
                        except ValueError:
                            messages.error(request, f'قيمة غير صالحة للعام {single_year}: {stored_input}')
                else:
                    messages.error(request, 'عام غير صالح.')
            
        except Employee.DoesNotExist:
            messages.error(request, 'الفرد غير موجود.')
        except Exception as e:
            messages.error(request, f'حدث خطأ: {str(e)}')
        
        # إعادة التوجيه مع المعاملات الكاملة
        redirect_url = f"{request.path}?employee_id={employee_id}&year={year}"
        if target_date_str:
            redirect_url += f"&target_date={target_date_str}"
        return redirect(redirect_url)
    
    def get_queryset(self):
        # العام الحالي افتراضيًا
        year = int(self.request.GET.get('year', datetime.now().year))
        target_date = self.request.GET.get('target_date', None)
        employee_id = self.request.GET.get('employee_id', None)
        
        if target_date:
            target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
        else:
            target_date = PeriodicAllowance.get_allowance_date(year)
        
        queryset = Employee.objects.filter(
            date_of_appointment__isnull=False,
            rank__isnull=False,
            date_of_birth__isnull=False  # للتقاعد
        ).select_related('rank').order_by('sort_number')  # ترتيب بـ sort_number
        
        # فلترة المؤهلين فقط بناءً على target_date
        eligible_ids = []
        for employee in queryset:
            dummy_allowance = PeriodicAllowance(
                employee=employee, 
                allowance_year=year, 
                stored_value=Decimal('0.00')
            )
            if dummy_allowance.is_eligible(target_date):
                eligible_ids.append(employee.id)
        
        filtered_queryset = queryset.filter(id__in=eligible_ids)
        
        # إذا محدد employee_id، فلتر للفرد الواحد
        if employee_id:
            filtered_queryset = filtered_queryset.filter(id=employee_id)
        
        return filtered_queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = int(self.request.GET.get('year', datetime.now().year))
        target_date_str = self.request.GET.get('target_date', None)
        employee_id = self.request.GET.get('employee_id', None)
        
        if target_date_str:
            target_date = datetime.strptime(target_date_str, '%Y-%m-%d').date()
        else:
            target_date = PeriodicAllowance.get_allowance_date(year)
            target_date_str = target_date.strftime('%Y-%m-%d')
        
        context['year'] = year
        context['target_date'] = target_date_str
        context['employee_id'] = employee_id
        
        # قائمة الموظفين للـ dropdown (جميع المؤهلين مرتبين بـ sort_number)
        all_eligible_employees = Employee.objects.filter(
            date_of_appointment__isnull=False,
            rank__isnull=False,
            date_of_birth__isnull=False
        ).select_related('rank').order_by('sort_number')
        
        eligible_ids_for_dropdown = []
        current_year_target = PeriodicAllowance.get_allowance_date(datetime.now().year)
        for emp in all_eligible_employees:
            dummy = PeriodicAllowance(employee=emp, allowance_year=datetime.now().year, stored_value=Decimal('0.00'))
            if dummy.is_eligible(current_year_target):
                eligible_ids_for_dropdown.append(emp.id)
        
        context['employees_list'] = all_eligible_employees.filter(id__in=eligible_ids_for_dropdown)
        
        # حساب عدد الفروق غير المتطابقة لكل الأعوام وكل الأفراد
        total_non_matching_count = 0
        total_non_matching_details = []
        current_year = date.today().year
        for emp in all_eligible_employees:
            appointment_year = emp.date_of_appointment.year + 1
            retirement_date = emp.date_of_birth + timedelta(days=60 * 365.25)
            retirement_year = retirement_date.year
            years_list = list(range(appointment_year, current_year + 1))
            for yr in years_list:
                allowance_date = PeriodicAllowance.get_allowance_date(yr)
                dummy = PeriodicAllowance(employee=emp, allowance_year=yr, stored_value=Decimal('0.00'))
                if not dummy.is_eligible(allowance_date):
                    continue
                stored = PeriodicAllowance.objects.filter(
                    employee=emp,
                    allowance_year=yr
                ).first()
                stored_value = stored.stored_value if stored else None
                calculated_value = PeriodicAllowance.get_calculated_value(emp, allowance_date)
                has_diff = calculated_value != stored_value if stored_value is not None else True
                if has_diff:
                    total_non_matching_count += 1
                    total_non_matching_details.append({
                        'employee': emp.name,
                        'year': yr,
                        'difference': calculated_value - (stored_value if stored_value is not None else Decimal('0.00'))
                    })
        context['total_non_matching_count'] = total_non_matching_count
        context['total_non_matching_details'] = total_non_matching_details
        
        if employee_id:
            # للفرد المحدد: احسب جميع الأعوام من التعيين +1 إلى التقاعد
            selected_employee = context['object_list'].first()  # الموظف الواحد
            if selected_employee:
                appointment_year = selected_employee.date_of_appointment.year + 1
                # تاريخ التقاعد التقريبي
                retirement_date = selected_employee.date_of_birth + timedelta(days=60 * 365.25)
                retirement_year = retirement_date.year
                
                years_list = list(range(appointment_year, retirement_year + 1))
                allowances_data = []
                employee_non_matching_details = []
                
                current_year = date.today().year  # التاريخ الحالي: 2025
                
                for yr in years_list:
                    # تاريخ العلاوة لهذا العام
                    allowance_date = PeriodicAllowance.get_allowance_date(yr)
                    
                    dummy = PeriodicAllowance(employee=selected_employee, allowance_year=yr, stored_value=Decimal('0.00'))
                    if not dummy.is_eligible(allowance_date) or yr > current_year:
                        continue  # تخطي غير المؤهل أو المستقبلي
                    
                    # القيمة المخزنة
                    stored = PeriodicAllowance.objects.filter(
                        employee=selected_employee,
                        allowance_year=yr
                    ).first()
                    stored_value = stored.stored_value if stored else None
                    
                    # الحساب الديناميكي (مع الدرجة الصحيحة في هذا التاريخ)
                    calculated_value = PeriodicAllowance.get_calculated_value(selected_employee, allowance_date)
                    
                    has_diff = calculated_value != stored_value if stored_value is not None else True
                    
                    # تحديد إذا كان العام ماضيًا/حاليًا (للتحكم في الإدخال)
                    is_past_year = yr <= current_year
                    
                    # تحويل القيمة المخزنة إلى string للعرض الآمن في input value
                    stored_str = str(stored_value) if stored_value is not None else ''
                    
                    # حساب الدرجة الفعالة في هذا العام
                    rank_name = PeriodicAllowance.get_rank_at_date(selected_employee, allowance_date)
                    
                    allowances_data.append({
                        'year': yr,
                        'allowance_date': allowance_date,
                        'calculated': calculated_value,
                        'stored': stored_value,
                        'stored_str': stored_str,  # string للـ input value
                        'rank_name': rank_name,  # اسم الدرجة في هذا العام
                        'has_diff': has_diff,
                        'difference': calculated_value - stored_value if stored_value is not None else Decimal('0.00'),
                        'is_past_year': is_past_year
                    })
                    
                    if has_diff:
                        employee_non_matching_details.append({
                            'year': yr,
                            'difference': calculated_value - stored_value if stored_value is not None else Decimal('0.00')
                        })
                
                context['allowances_data'] = allowances_data
                context['non_matching_count'] = sum(1 for item in allowances_data if item['has_diff'])
                context['employee_non_matching_details'] = employee_non_matching_details
                context['selected_employee'] = selected_employee
        else:
            # الجدول العام (للعام المحدد فقط، مع إضافة allowances_data للعرض مع inputs)
            context['allowances_data'] = []
            current_year = date.today().year
            year_non_matching_details = []
            for employee in context['object_list']:
                # للعام المحدد فقط
                yr = year
                if yr > current_year:
                    continue  # تخطي المستقبلي
                
                allowance_date = target_date  # نفس التاريخ
                
                dummy = PeriodicAllowance(employee=employee, allowance_year=yr, stored_value=Decimal('0.00'))
                if not dummy.is_eligible(allowance_date):
                    continue  # رغم الفلترة في queryset، للأمان
                
                # القيمة المخزنة
                stored = PeriodicAllowance.objects.filter(
                    employee=employee,
                    allowance_year=yr
                ).first()
                stored_value = stored.stored_value if stored else None
                
                # الحساب الديناميكي
                calculated_value = PeriodicAllowance.get_calculated_value(employee, allowance_date)
                
                has_diff = calculated_value != stored_value if stored_value is not None else True
                
                # تحديد إذا كان العام ماضيًا/حاليًا
                is_past_year = yr <= current_year
                
                # تحويل القيمة المخزنة إلى string
                stored_str = str(stored_value) if stored_value is not None else ''
                
                # حساب الدرجة الفعالة
                rank_name = PeriodicAllowance.get_rank_at_date(employee, allowance_date)
                
                context['allowances_data'].append({
                    'employee': employee,
                    'year': yr,
                    'allowance_date': allowance_date,
                    'calculated': calculated_value,
                    'stored': stored_value,
                    'stored_str': stored_str,
                    'rank_name': rank_name,
                    'has_diff': has_diff,
                    'difference': calculated_value - stored_value if stored_value is not None else Decimal('0.00'),
                    'is_past_year': is_past_year,
                    'sort_number': employee.sort_number
                })
                
                if has_diff:
                    year_non_matching_details.append({
                        'employee': employee.name,
                        'difference': calculated_value - stored_value if stored_value is not None else Decimal('0.00')
                    })
            
            context['non_matching_count'] = sum(1 for item in context['allowances_data'] if item['has_diff'])
            context['year_non_matching_details'] = year_non_matching_details
        
        return context
    
    
    
    
    
    
    
    
# E:\yasser\emapi2025\myproject\periodic_allowances\views.py
# Updated AllowancesDftrView to include rank for each year and convert value to Arabic digits

from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib import messages
from decimal import Decimal
from datetime import datetime, timedelta, date
from em_data.models import Employee
from .models import PeriodicAllowance
import json


def to_arabic_digits(s):
    """Convert English digits to Arabic digits in a string."""
    if not s:
        return ''
    arabic_map = str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')
    return s.translate(arabic_map)


class AllowancesDftrView(ListView):
    model = Employee
    template_name = 'periodic_allowances/allowances_dftr.html'
    
    def get_queryset(self):
        return self.model.objects.none()  # Empty queryset since we're using custom data_list
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        eligible_employees = Employee.objects.filter(
            date_of_appointment__isnull=False,
            rank__isnull=False,
            date_of_birth__isnull=False
        ).select_related('rank').order_by('sort_number')
        
        current_year = date.today().year
        max_pairs = 0
        
        # First pass: calculate max_pairs including all service years up to retirement
        for emp in eligible_employees:
            appointment_year = emp.date_of_appointment.year + 1
            retirement_date = emp.date_of_birth + timedelta(days=60 * 365.25)
            retirement_year = retirement_date.year
            
            years_list = list(range(appointment_year, retirement_year + 1))
            
            eligible_count = 0
            for yr in years_list:
                allowance_date = PeriodicAllowance.get_allowance_date(yr)
                dummy = PeriodicAllowance(employee=emp, allowance_year=yr, stored_value=Decimal('0.00'))
                if dummy.is_eligible(allowance_date):
                    eligible_count += 1
            
            if eligible_count > max_pairs:
                max_pairs = eligible_count
        
        # Second pass: build data_list
        data_list = []
        serial = 1
        
        for emp in eligible_employees:
            appointment_year = emp.date_of_appointment.year + 1
            retirement_date = emp.date_of_birth + timedelta(days=60 * 365.25)
            retirement_year = retirement_date.year
            
            years_list = list(range(appointment_year, retirement_year + 1))
            
            pairs = []
            for yr in years_list:
                allowance_date = PeriodicAllowance.get_allowance_date(yr)
                dummy = PeriodicAllowance(employee=emp, allowance_year=yr, stored_value=Decimal('0.00'))
                if not dummy.is_eligible(allowance_date):
                    continue
                
                # Get rank for this year
                rank_name_for_year = PeriodicAllowance.get_rank_at_date(emp, allowance_date)
                
                if yr <= current_year:
                    # Calculated value for past/current years
                    calculated_value = PeriodicAllowance.get_calculated_value(emp, allowance_date)
                    date_str = to_arabic_digits(allowance_date.strftime('%Y/%m/%d'))
                    value_str = to_arabic_digits(str(calculated_value))
                else:
                    # Future years: empty date format and empty value
                    date_str = f"  /  / {to_arabic_digits(str(yr))}"
                    value_str = ''
                
                pairs.append((rank_name_for_year, date_str, value_str))
            
            # Pad to max_pairs
            while len(pairs) < max_pairs:
                pairs.append(('', '', ''))
            
            row = {
                'serial': serial,
                'rank_name': emp.rank.name,
                'police_number': emp.police_number or '',
                'name': emp.name,
                'dob': to_arabic_digits(emp.date_of_birth.strftime('%Y/%m/%d')),
                'appointment': to_arabic_digits(emp.date_of_appointment.strftime('%Y/%m/%d')),
                'year_value_pairs': pairs
            }
            data_list.append(row)
            serial += 1
        
        context['data_list'] = data_list
        context['max_pairs'] = max_pairs
        context['pair_indices'] = list(range(max_pairs))
        return context