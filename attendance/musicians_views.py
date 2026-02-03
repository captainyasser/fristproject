from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta
from .models import Attendance
from em_data.models import Employee
import json

@login_required
def musicians_page(request):
    """صفحة إدارة الموسيقيين الذكية"""
    # جلب جميع الموسيقيين (department_id = 14)
    musicians = Employee.objects.filter(department_id=14, mainornot=1).order_by('dep_sort')
    
    # خيارات التشغيل
    operation_choices = Employee.OPERATION_CHOICES
    
    # حالات الحضور
    attendance_states = [
        ('_', '-'),
        ('نوبتجي', 'نوبتجي'),
        ('يومي', 'يومي'),
        ('راحة', 'راحة'),
        ('ر بديلة', 'ر بديلة'),
        ('8 صباحاً', '8 صباحاً'),
        ('منحة', 'منحة'),
        ('عطلة', 'عطلة'),
        ('دورية', 'دورية'),
        ('طارئة', 'طارئة'),
        ('مأمورية', 'مأمورية'),
        ('مأمورية خ', 'مأمورية خ'),
        ('فرقة', 'فرقة'),
        ('انتداب', 'انتداب'),
        ('مرضي', 'مرضي'),
        ('ج وضع', 'ج وضع'),
        ('خاصه', 'خاصه'),
        ('ت دوري', 'ت دوري'),
        ('ت تكراري', 'ت تكراري'),
        ('غياب', 'غياب'),
        ('قرار66', 'قرار66'),
    ]
    
    context = {
        'musicians': musicians,
        'operation_choices': operation_choices,
        'attendance_states': attendance_states,
        'today': datetime.today().date(),
    }
    
    return render(request, 'attendance/musicians.html', context)


@api_view(['POST'])
@login_required
@csrf_exempt
def filter_musicians(request):
    """فلترة الموسيقيين حسب معايير متعددة"""
    try:
        data = request.data
        
        # البداية بجميع الموسيقيين
        musicians = Employee.objects.filter(department_id=14, mainornot=1)
        
        # فلترة حسب التشغيل
        operation_filter = data.get('operation_filter')
        if operation_filter and operation_filter != 'all':
            musicians = musicians.filter(operation=operation_filter)
        
        # فلترة حسب الأسماء المحددة
        selected_names = data.get('selected_names', [])
        if selected_names:
            musicians = musicians.filter(id__in=selected_names)
        
        # الترتيب
        sort_by = data.get('sort_by', 'dep_sort')
        if sort_by in ['dep_sort', 'sort_number', 'operation', 'rahatcounter']:
            musicians = musicians.order_by(sort_by)
        
        # فلترة حسب حالة معينة في تاريخ معين
        state_date_filters = data.get('state_date_filters', [])
        if state_date_filters:
            for filter_item in state_date_filters:
                date = filter_item.get('date')
                states = filter_item.get('states', [])
                if date and states:
                    # جلب الموظفين الذين لديهم إحدى الحالات المحددة في التاريخ المحدد
                    matching_ids = Attendance.objects.filter(
                        employee__in=musicians,
                        date=date,
                        state__in=states
                    ).values_list('employee_id', flat=True)
                    musicians = musicians.filter(id__in=matching_ids)
        
        # فلترة بشرطين (يومين مختلفين)
        dual_filter = data.get('dual_filter')
        if dual_filter:
            date1 = dual_filter.get('date1')
            states1 = dual_filter.get('states1', [])
            date2 = dual_filter.get('date2')
            states2 = dual_filter.get('states2', [])
            
            if date1 and states1 and date2 and states2:
                # الموظفين الذين يحققون الشرط الأول
                ids1 = set(Attendance.objects.filter(
                    employee__in=musicians,
                    date=date1,
                    state__in=states1
                ).values_list('employee_id', flat=True))
                
                # الموظفين الذين يحققون الشرط الثاني
                ids2 = set(Attendance.objects.filter(
                    employee__in=musicians,
                    date=date2,
                    state__in=states2
                ).values_list('employee_id', flat=True))
                
                # التقاطع (AND)
                matching_ids = ids1 & ids2
                musicians = musicians.filter(id__in=matching_ids)
        
        # إعداد البيانات للإرجاع
        result = []
        for musician in musicians:
            result.append({
                'id': musician.id,
                'name': musician.name,
                'nickname': musician.nickname,
                'operation': musician.operation,
                'rahatcounter': musician.rahatcounter,
                'dep_sort': musician.dep_sort,
                'sort_number': musician.sort_number,
            })
        
        return Response({
            'success': True,
            'musicians': result,
            'count': len(result)
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=500)


@api_view(['POST'])
@login_required
@csrf_exempt
def bulk_update_musicians(request):
    """تحديث جماعي لحالات الموسيقيين"""
    try:
        data = request.data
        
        # الموظفين المستهدفين
        target_employees = data.get('target_employees', [])
        if not target_employees:
            return Response({
                'success': False,
                'error': 'No employees selected'
            }, status=400)
        
        # التحديثات المطلوبة
        updates = data.get('updates', [])
        if not updates:
            return Response({
                'success': False,
                'error': 'No updates provided'
            }, status=400)
        
        # تنفيذ التحديثات
        updated_count = 0
        for employee_id in target_employees:
            try:
                employee = Employee.objects.get(id=employee_id, department_id=14)
                
                for update in updates:
                    date = update.get('date')
                    state = update.get('state')
                    
                    if not date or not state:
                        continue
                    
                    # تحديد القيم بناءً على الحالة
                    comfort_adjustment = 0
                    food = False
                    in_or_out = 'out'
                    
                    if state == 'نوبتجي':
                        comfort_adjustment = 1
                        food = True
                        in_or_out = 'in'
                    elif state in ['راحة', 'ر بديلة', '8 صباحاً']:
                        comfort_adjustment = -1
                        in_or_out = 'out'
                    elif state == 'يومي':
                        comfort_adjustment = 0
                        in_or_out = 'going'
                    
                    # جلب أو إنشاء السجل
                    attendance, created = Attendance.objects.get_or_create(
                        employee=employee,
                        date=date,
                        defaults={
                            'state': state,
                            'comfort_adjustment': comfort_adjustment,
                            'food': food,
                            'in_or_out': in_or_out
                        }
                    )
                    
                    if not created:
                        # حساب الفرق في comfort_adjustment
                        old_comfort = attendance.comfort_adjustment
                        delta = comfort_adjustment - old_comfort
                        
                        # تحديث السجل
                        attendance.state = state
                        attendance.comfort_adjustment = comfort_adjustment
                        attendance.food = food
                        attendance.in_or_out = in_or_out
                        attendance.save()
                        
                        # تحديث عداد الراحات
                        employee.rahatcounter += delta
                        employee.save()
                    else:
                        # سجل جديد - تحديث العداد مباشرة
                        employee.rahatcounter += comfort_adjustment
                        employee.save()
                    
                    updated_count += 1
                    
            except Employee.DoesNotExist:
                continue
        
        return Response({
            'success': True,
            'updated_count': updated_count,
            'message': f'تم تحديث {updated_count} سجل بنجاح'
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=500)


@api_view(['POST'])
@login_required
@csrf_exempt
def calculate_rahat_period(request):
    """حساب عداد الراحات في فترة محددة"""
    try:
        data = request.data
        
        employee_ids = data.get('employee_ids', [])
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        reset_date = data.get('reset_date')  # التاريخ الذي يبدأ منه العد
        
        if not employee_ids or not start_date or not end_date:
            return Response({
                'success': False,
                'error': 'Missing required parameters'
            }, status=400)
        
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
        reset_date_obj = datetime.strptime(reset_date, '%Y-%m-%d').date() if reset_date else start_date_obj
        
        results = []
        
        for emp_id in employee_ids:
            try:
                employee = Employee.objects.get(id=emp_id, department_id=14)
                
                # حساب الراحات في الفترة
                attendances = Attendance.objects.filter(
                    employee=employee,
                    date__gte=reset_date_obj,
                    date__lte=end_date_obj
                ).order_by('date')
                
                rahat_count = 0
                for att in attendances:
                    rahat_count += att.comfort_adjustment
                
                results.append({
                    'id': employee.id,
                    'name': employee.name,
                    'nickname': employee.nickname,
                    'operation': employee.operation,
                    'rahat_in_period': rahat_count,
                    'current_rahatcounter': employee.rahatcounter
                })
                
            except Employee.DoesNotExist:
                continue
        
        return Response({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=500)
