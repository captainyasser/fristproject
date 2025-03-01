from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Attendance
from em_data.models import Employee
from datetime import datetime, timedelta
from departments.models import Department



@login_required
def attendance_record(request):
    employees = Employee.objects.all().order_by('sort_number')
    start_date = request.GET.get('start_date', datetime.today().date().strftime('%Y-%m-%d'))
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    days = [start_date + timedelta(days=i) for i in range(21)]
    
    # جمع بيانات الحضور
    attendance_data = {}
    for employee in employees:
        attendance_data[employee.id] = {}
        for day in days:
            attendance, created = Attendance.objects.get_or_create(
                employee=employee,
                date=day,
                defaults={'state': '_', 'food': False, 'comfort_adjustment': 0}
            )
            # إذا كان السجل جديدًا و"نوبتجي"، نضبط القيم الافتراضية
            if created and attendance.state == 'نوبتجي':
                attendance.comfort_adjustment = 1
                attendance.food = True
                attendance.save()
            attendance_data[employee.id][day] = {
                'state': attendance.state,
                'food': attendance.food,
                'comfort_adjustment': attendance.comfort_adjustment
            }

    if request.method == 'POST':
        for employee in employees:
            for day in days:
                state_key = f'state_{employee.id}_{day.strftime("%Y%m%d")}'
                food_key = f'food_{employee.id}_{day.strftime("%Y%m%d")}'
                comfort_key = f'comfort_{employee.id}_{day.strftime("%Y%m%d")}'
                
                state = request.POST.get(state_key, '_')
                food = request.POST.get(food_key) == 'on'
                comfort_adjustment = int(request.POST.get(comfort_key, '0'))
                
                # تحديث السجل
                attendance, created = Attendance.objects.get_or_create(
                    employee=employee,
                    date=day,
                    defaults={'state': state, 'food': food, 'comfort_adjustment': comfort_adjustment}
                )
                if not created:
                    old_comfort = attendance.comfort_adjustment
                    attendance.state = state
                    # لا نفرض food أو comfort_adjustment لـ "نوبتجي"، نتركها للإدخال اليدوي
                    attendance.food = food
                    attendance.comfort_adjustment = comfort_adjustment
                    
                    # تحديث rahatcounter
                    if state == 'راحة' and attendance.state != 'راحة':  # إذا تغيرت إلى "راحة"
                        employee.rahatcounter -= 1
                    elif state != 'راحة' and attendance.state == 'راحة':  # إذا تغيرت من "راحة"
                        employee.rahatcounter += 1
                    
                    if old_comfort != comfort_adjustment:
                        if old_comfort == 1 and comfort_adjustment != 1:
                            employee.rahatcounter -= 1
                        elif old_comfort != 1 and comfort_adjustment == 1:
                            employee.rahatcounter += 1
                    attendance.save()
                    employee.save()

        return redirect('attendance_record')

    return render(request, 'attendance/attendance_record.html', {
        'employees': employees,
        'days': days,
        'attendance_data': attendance_data,
        'start_date': start_date,
    })
    
    
    
    from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Attendance
from em_data.models import Employee
from datetime import date, datetime, timedelta
import json

@login_required(login_url='/')
def attendance_3w(request):
    employees = Employee.objects.all()
    today = date.today()

    # Handle start_date from request or default to the previous Saturday
    start_date = request.GET.get('start_date')
    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = start_date + timedelta(days=20)
        except ValueError:
            messages.error(request, "Please enter a valid date.")
            return redirect(request.path)
    else:
        days_to_saturday = (today.weekday() - 5) % 7
        start_date = today - timedelta(days=days_to_saturday + 7)
        end_date = start_date + timedelta(days=20)

    week_days = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

    # Filter employees by department if provided
    department_filter = request.GET.get('departments')
    if department_filter:
        employees = employees.filter(department=department_filter)

    # Sort employees
    sort_by = request.GET.get('sort_by', 'dep_sort')
    valid_sort_fields = ['sort_number', 'dep_sort', 'operation', 'department']
    if sort_by in valid_sort_fields:
        employees = employees.order_by(sort_by)

    # Paginate employees
    paginator = Paginator(employees, 200)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Fetch attendance data
    attendance_data = {}
    for employee in page_obj.object_list.prefetch_related('attendances'):
        attendance_data[employee.id] = {}
        for day in week_days:
            try:
                attendance = employee.attendances.get(date=day)
                attendance_data[employee.id][day] = {
                    'state': attendance.state,
                    'food': attendance.food,
                    'comfort_adjustment': attendance.comfort_adjustment
                }
            except Attendance.DoesNotExist:
                attendance_data[employee.id][day] = {
                    'state': '_',
                    'food': False,
                    'comfort_adjustment': 0
                }

    if request.method == 'POST':
        for employee in page_obj.object_list:
            for day in week_days:
                state = request.POST.get(f'attendance_state_{employee.id}_{day.strftime("%Y%m%d")}')
                if state:
                    food = request.POST.get(f'food_{employee.id}_{day.strftime("%Y%m%d")}')
                    comfort_adjustment = request.POST.get(f'comfort_{employee.id}_{day.strftime("%Y%m%d")}')
                    
                    food_value = '1' if food == '1' else ('0' if state == 'نوبتجي' else '0')
                    comfort_value = int(comfort_adjustment) if comfort_adjustment else (1 if state == 'نوبتجي' else 0)

                    attendance, created = Attendance.objects.update_or_create(
                        employee=employee,
                        date=day,
                        defaults={
                            'state': state,
                            'food': food_value == '1',
                            'comfort_adjustment': comfort_value,
                            'in_or_out': '1' if state == 'نوبتجي' else ('2' if state == 'يومي' else '3')
                        }
                    )
                    if state == 'راحة' and not created and attendance.state != 'راحة':
                        employee.rahatcounter -= 1
                    elif state != 'راحة' and not created and attendance.state == 'راحة':
                        employee.rahatcounter += 1
                    
                    old_comfort = attendance.comfort_adjustment if not created else 0
                    if old_comfort != comfort_value:
                        if old_comfort == 1 and comfort_value != 1:
                            employee.rahatcounter -= 1
                        elif old_comfort != 1 and comfort_value == 1:
                            employee.rahatcounter += 1
                    employee.save()
        return HttpResponseRedirect(request.path)

    return render(
        request,
        'attendance/attendance_3w.html',
        {
            'page_obj': page_obj,
            'week_days': week_days,
            'attendance_data': attendance_data,
            'sort_by': sort_by,
            'start_date': start_date,
            'end_date': end_date,
            'today': today,
            'department_choices': Department.objects.values_list('id', 'name').distinct(),  # تعديل هنا
        }
    )





@login_required(login_url='/')
def update_attendance(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        selected_date = request.POST.get('selected_date')
        selected_value = request.POST.get('selected_value')
        comfort_adjustment = request.POST.get('comfort_adjustment')
        food = request.POST.get('food')

        try:
            employee = Employee.objects.get(id=employee_id)
            date_obj = datetime.strptime(selected_date, '%Y%m%d').date()

            attendance, created = Attendance.objects.get_or_create(
                employee=employee,
                date=date_obj,
                defaults={'state': '_', 'food': False, 'comfort_adjustment': 0}
            )

            old_comfort = attendance.comfort_adjustment
            old_state = attendance.state

            if selected_value:
                attendance.state = selected_value

            # التعامل مع "نوبتجي"
            if selected_value == 'نوبتجي':
                attendance.food = True  # دائمًا True عند اختيار "نوبتجي"
                if old_state != 'راحة':
                    if old_comfort == 0:
                        employee.rahatcounter += 1  # زيادة بمقدار 1
                        attendance.comfort_adjustment = 1  # تعيين إلى 1
                    # إذا كان old_comfort = 1، لا تغيير
            # التعامل مع "راحة"
            elif selected_value == 'راحة' and old_state != 'راحة':
                if old_comfort == 0:
                    employee.rahatcounter -= 1  # تقليل بمقدار 1
                elif old_comfort == 1:
                    employee.rahatcounter -= 2  # تقليل بمقدار 2
                    attendance.comfort_adjustment = 0  # تعيين إلى 0
                attendance.food = False  # دائمًا False عند "راحة"
            # التعامل مع التبديل من "نوبتجي" إلى حالة غير "راحة"
            elif old_state == 'نوبتجي' and selected_value != 'راحة':
                if old_comfort == 1:
                    employee.rahatcounter -= 1  # تقليل بمقدار 1
                    attendance.comfort_adjustment = 0  # تعيين إلى 0
                # إذا كان old_comfort = 0، لا تغيير
            else:
                if food is not None:
                    attendance.food = (food == '1')
                if comfort_adjustment is not None:
                    new_comfort = int(comfort_adjustment)
                    if old_comfort != new_comfort and selected_value != 'راحة':
                        if old_comfort == 1 and new_comfort == 0:
                            employee.rahatcounter -= 1
                        elif old_comfort == 0 and new_comfort == 1:
                            employee.rahatcounter += 1
                    attendance.comfort_adjustment = new_comfort

            if selected_value != 'راحة' and old_state == 'راحة':
                employee.rahatcounter += 1  # زيادة عند الخروج من "راحة"

            attendance.save()
            employee.save()

            print(f"Updated: state={attendance.state}, food={attendance.food}, comfort={attendance.comfort_adjustment}, rahatcounter={employee.rahatcounter}")
            return JsonResponse({'success': True, 'rahatcounter': employee.rahatcounter})
        except Employee.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Employee not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})








@login_required(login_url='/')
def reset_rahatcounter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        employee_id = data.get('employee_id')
        try:
            employee = Employee.objects.get(id=employee_id)
            employee.rahatcounter = 0
            employee.save()
            return JsonResponse({'success': True})
        except Employee.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Employee not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required(login_url='/')
def insert_attendance_for_date(request):
    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')
        try:
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
            employees = Employee.objects.all()
            for employee in employees:
                Attendance.objects.get_or_create(
                    employee=employee,
                    date=date_obj,
                    defaults={'state': '_', 'food': False, 'comfort_adjustment': 0}
                )
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/attendance/attendance_3w/'))
        except ValueError:
            messages.error(request, "Invalid date format.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/attendance/attendance_3w/'))

@login_required(login_url='/')
def get_rahatcounter(request):
    employee_id = request.GET.get('employee_id')
    try:
        employee = Employee.objects.get(id=employee_id)
        return JsonResponse({'success': True, 'rahatcounter': employee.rahatcounter})
    except Employee.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Employee not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})