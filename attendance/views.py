from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Attendance
from em_data.models import Employee
from departments.models import Department
from datetime import datetime, timedelta, date
import json
import logging

@login_required(login_url='/')
def attendance_3w(request):
    today = date.today()
    start_date = request.GET.get('start_date')
    num_days = request.GET.get('num_days', '27')
    try:
        num_days = int(num_days)
        num_days = max(1, min(40, num_days))
    except ValueError:
        num_days = 27

    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = start_date + timedelta(days=num_days)
        except ValueError:
            messages.error(request, "Please enter a valid date.")
            return redirect(request.path)
    else:
        days_to_saturday = (today.weekday() - 5) % 7
        start_date = today - timedelta(days=days_to_saturday + 14)
        end_date = start_date + timedelta(days=num_days)

    week_days = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    employees = Employee.objects.all()

    department_filter = request.GET.get('departments')
    if department_filter:
        employees = employees.filter(department=department_filter)

    sort_by = request.GET.get('sort_by', 'dep_sort')
    valid_sort_fields = ['sort_number', 'dep_sort', 'operation', 'department']
    if sort_by in valid_sort_fields:
        employees = employees.order_by(sort_by)

    paginator = Paginator(employees, 200)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

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
        return redirect(request.path_info + '?' + request.GET.urlencode())

    return render(
        request,
        'attendance/attendance_3w.html',
        {
            'page_obj': page_obj,
            'week_days': week_days,
            'sort_by': sort_by,
            'start_date': start_date,
            'end_date': end_date,
            'today': today,
            'department_choices': Department.objects.values_list('id', 'name').distinct(),
            'num_days': num_days,
        }
    )

@login_required(login_url='/')
def update_attendance(request):
    if request.method == 'POST':
        response_data = {'success': True, 'updates': {}}

        for key in request.POST:
            if key.startswith('changes['):
                parts = key.split('[')[1].split(']')[0]
                field = key.split(']')[1][1:]
                employee_id, date_str = parts.split('_')

                try:
                    employee = Employee.objects.get(id=employee_id)
                    date_obj = datetime.strptime(date_str, '%Y%m%d').date()

                    attendance, created = Attendance.objects.get_or_create(
                        employee=employee,
                        date=date_obj,
                        defaults={'state': '_', 'food': False, 'comfort_adjustment': 0, 'in_or_out': 'out'}
                    )

                    old_comfort = attendance.comfort_adjustment
                    old_state = attendance.state

                    selected_value = request.POST.get(f'changes[{parts}][selected_value]')
                    comfort_adjustment = request.POST.get(f'changes[{parts}][comfort_adjustment]')
                    food = request.POST.get(f'changes[{parts}][food]')
                    source = request.POST.get(f'changes[{parts}][source]')

                    if selected_value:
                        attendance.state = selected_value

                    if source == 'select':
                        if selected_value == 'نوبتجي':
                            attendance.food = True
                            if old_comfort == -1:
                                employee.rahatcounter += 2
                            elif old_comfort == 0:
                                employee.rahatcounter += 1
                            attendance.comfort_adjustment = 1
                            attendance.in_or_out = 'in'
                        elif selected_value == 'يومي':
                            attendance.food = False
                            if old_comfort == 1:
                                employee.rahatcounter -= 1
                            elif old_comfort == -1:
                                employee.rahatcounter += 1
                            attendance.comfort_adjustment = 0
                            attendance.in_or_out = 'going'
                        elif selected_value in ['راحة', 'ر بديلة', '8 صباحاً']:
                            attendance.food = False
                            if old_comfort == 0:
                                employee.rahatcounter -= 1
                            elif old_comfort == 1:
                                employee.rahatcounter -= 2
                            attendance.comfort_adjustment = -1
                            attendance.in_or_out = 'out'
                        else:
                            attendance.food = False
                            if old_comfort == 1:
                                employee.rahatcounter -= 1
                            elif old_comfort == -1:
                                employee.rahatcounter += 1
                            attendance.comfort_adjustment = 0
                            attendance.in_or_out = 'out'

                    if source == 'checkbox':
                        if food is not None:
                            attendance.food = (food == '1')
                        if comfort_adjustment is not None:
                            new_comfort = int(comfort_adjustment)
                            if old_comfort != new_comfort:
                                if old_comfort == 0 and new_comfort == 1:
                                    employee.rahatcounter += 1
                                elif old_comfort == 1 and new_comfort == 0:
                                    employee.rahatcounter -= 1
                            attendance.comfort_adjustment = new_comfort

                    attendance.save()
                    employee.save()

                    response_data['updates'][parts] = {
                        'rahatcounter': employee.rahatcounter,
                        'state': attendance.state,
                        'food': attendance.food,
                        'comfort_adjustment': attendance.comfort_adjustment
                    }

                except Employee.DoesNotExist:
                    response_data['success'] = False
                    response_data['error'] = f'Employee {employee_id} not found'
                    break
                except Exception as e:
                    response_data['success'] = False
                    response_data['error'] = str(e)
                    break

        return JsonResponse(response_data)
    return JsonResponse({'success': False, 'error': 'Invalid request'})

logger = logging.getLogger(__name__)

@login_required(login_url='/')
def reset_rahatcounter(request):
    if request.method == 'POST':
        try:
            logger.info(f"Received request body: {request.body}")
            data = json.loads(request.body)
            employee_id = data.get('employee_id')
            
            if not employee_id:
                logger.error("No employee_id provided in request")
                return JsonResponse({'success': False, 'error': 'Employee ID is required'})

            try:
                employee_id = int(employee_id)
            except ValueError:
                logger.error(f"Invalid employee_id format: {employee_id}")
                return JsonResponse({'success': False, 'error': 'Invalid employee ID format'})

            logger.info(f"Attempting to reset rahatcounter for employee_id: {employee_id}")
            employee = Employee.objects.get(id=employee_id)
            employee.rahatcounter = 0
            employee.save()
            
            logger.info(f"Successfully reset rahatcounter for employee_id: {employee_id}")
            return JsonResponse({'success': True})
        except Employee.DoesNotExist:
            logger.error(f"Employee not found: {employee_id}")
            return JsonResponse({'success': False, 'error': 'Employee not found'})
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return JsonResponse({'success': False, 'error': f'Internal server error: {str(e)}'})
    logger.warning("Invalid request method")
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required(login_url='/login/')
def insert_attendance_for_date(request):
    if request.method == "POST":
        selected_date_input = request.POST.get("selected_date")
        
        try:
            today = datetime.strptime(selected_date_input, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            today = date.today()

        day_of_week = today.weekday()

        for employee in Employee.objects.all():
            operation = employee.operation
            state_value = "_"
            in_or_out_value = '3'
            food_value = '0'

            if operation == 'السبت':
                if day_of_week in [5, 6, 0]:
                    state_value = "نوبتجي"
                elif day_of_week == 1:
                    state_value = "يومي"
                elif day_of_week in [2, 3, 4]:
                    state_value = "راحة"
            elif operation == 'الأحد':
                if day_of_week in [6, 0, 1]:
                    state_value = "نوبتجي"
                elif day_of_week == 2:
                    state_value = "يومي"
                elif day_of_week in [3, 4, 5]:
                    state_value = "راحة"
            elif operation == 'الاثنين':
                if day_of_week in [0, 1, 2]:
                    state_value = "نوبتجي"
                elif day_of_week == 3:
                    state_value = "يومي"
                elif day_of_week in [4, 5, 6]:
                    state_value = "راحة"
            elif operation == 'الثلاثاء':
                if day_of_week in [1, 2, 3]:
                    state_value = "نوبتجي"
                elif day_of_week == 4:
                    state_value = "يومي"
                elif day_of_week in [5, 6, 0]:
                    state_value = "راحة"
            elif operation == 'الأربعاء':
                if day_of_week in [2, 3, 4]:
                    state_value = "نوبتجي"
                elif day_of_week == 5:
                    state_value = "يومي"
                elif day_of_week in [6, 0, 1]:
                    state_value = "راحة"
            elif operation == 'الخميس':
                if day_of_week in [3, 4, 5]:
                    state_value = "نوبتجي"
                elif day_of_week == 6:
                    state_value = "يومي"
                elif day_of_week in [0, 1, 2]:
                    state_value = "راحة"
            elif operation == 'الجمعة':
                if day_of_week in [4, 5, 6]:
                    state_value = "نوبتجي"
                elif day_of_week == 0:
                    state_value = "يومي"
                elif day_of_week in [1, 2, 3]:
                    state_value = "راحة"
            elif operation == 'انتداب':
                state_value = "انتداب"
            elif operation == 'عمل يومي':
                if day_of_week in [0, 1, 2, 3, 5, 6]:
                    state_value = "يومي"
                elif day_of_week == 4:
                    state_value = "راحة"

            in_or_out_value = '1' if state_value == 'نوبتجي' else ('2' if state_value == 'يومي' else '3')
            food_value = '1' if state_value == 'نوبتجي' else '0'

            if state_value == 'نوبتجي':
                employee.rahatcounter += 1
            elif state_value in ['8 صباحاً', 'ر بديلة', 'راحة']:
                employee.rahatcounter -= 1

            employee.save()

            if not Attendance.objects.filter(employee=employee, date=today).exists():
                Attendance.objects.create(
                    employee=employee,
                    date=today,
                    state=state_value,
                    food=food_value == '1',
                    in_or_out=in_or_out_value,
                    comfort_adjustment=1 if state_value == 'نوبتجي' else (0 if state_value == 'يومي' else -1 if state_value in ['راحة', 'ر بديلة', '8 صباحاً'] else 0)
                )

        return redirect('attendance_3w')

    return render(request, 'insertdayforall.html')

@login_required(login_url='/')
def get_attendance_data(request):
    start_date_str = request.GET.get('start_date')
    page = request.GET.get('page', '1')
    num_days = request.GET.get('num_days', '27')

    if not start_date_str:
        return JsonResponse({'success': False, 'error': 'Start date is required'})

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        num_days = int(num_days)
        num_days = max(1, min(40, num_days))
        week_days = [start_date + timedelta(days=i) for i in range(num_days)]

        employees = Employee.objects.all()
        paginator = Paginator(employees, 50)  # تقليل إلى 50 موظفًا لكل صفحة
        page_obj = paginator.get_page(page)

        attendance_data = {}
        for employee in page_obj:
            attendance_records = Attendance.objects.filter(
                employee=employee,
                date__range=(start_date, week_days[-1])
            ).values('date', 'state', 'comfort_adjustment', 'food')

            attendance_dict = {rec['date'].strftime('%Y%m%d'): {
                'state': rec['state'],
                'comfort_adjustment': rec['comfort_adjustment'],
                'food': rec['food']
            } for rec in attendance_records}

            attendance_data[employee.id] = {}
            for day in week_days:
                date_str = day.strftime('%Y%m%d')
                attendance_data[employee.id][date_str] = attendance_dict.get(date_str, {
                    'state': '_',
                    'comfort_adjustment': 0,
                    'food': False
                })

        return JsonResponse({'success': True, 'attendance_data': attendance_data})
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Invalid date format'})






from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Attendance
from em_data.models import Employee
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

@login_required(login_url='/')
def one_employee(request):
    today = date.today()
    employees = Employee.objects.all()

    selected_employee = request.GET.get('employee')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    employee = None
    start_date = today
    end_date = (today + relativedelta(months=1)).replace(day=1) + relativedelta(days=-1, months=1)
    week_days = []
    week_days_chunked = []

    if selected_employee:
        try:
            employee = Employee.objects.get(id=selected_employee)

            operation_day_map = {
                'السبت': 5, 'الأحد': 6, 'الاثنين': 0, 'الثلاثاء': 1,
                'الأربعاء': 2, 'الخميس': 3, 'الجمعة': 4
            }
            default_start_date = today
            if employee.operation in operation_day_map:
                target_weekday = operation_day_map[employee.operation]
                days_to_target = (today.weekday() - target_weekday) % 7
                default_start_date = today - timedelta(days=days_to_target + 35)

            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else default_start_date
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else end_date

            if end_date < start_date:
                messages.error(request, "تاريخ النهاية يجب أن يكون بعد تاريخ البداية.")
                return redirect(request.path)

            week_days = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
            week_days_chunked = [week_days[i:i + 7] for i in range(0, len(week_days), 7)]

        except Employee.DoesNotExist:
            messages.error(request, "الفرد المحدد غير موجود.")
            return redirect(request.path)
        except ValueError:
            messages.error(request, "يرجى إدخال تواريخ صالحة.")
            return redirect(request.path)

    return render(request, 'attendance/one_employee.html', {
        'employees': employees,
        'selected_employee': selected_employee,
        'employee': employee,
        'week_days': week_days,
        'week_days_chunked': week_days_chunked,
        'start_date': start_date,
        'end_date': end_date,
        'today': today,
    })









@login_required(login_url='/')
def get_attendance(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    employee_id = request.GET.get('employee_id')

    if not start_date_str or (employee_id and not end_date_str):
        return JsonResponse({'success': False, 'error': 'Start date and employee ID are required'})

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            week_days = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
        else:
            week_days = [start_date + timedelta(days=i) for i in range(28)]

        if employee_id:
            employees = Employee.objects.filter(id=employee_id)
        else:
            employees = Employee.objects.all()[:200]

        attendance_data = {}
        for employee in employees:
            attendance_data[employee.id] = {}
            for day in week_days:
                attendance = Attendance.objects.filter(employee=employee, date=day).first()
                attendance_data[employee.id][day.strftime('%Y%m%d')] = {
                    'state': attendance.state if attendance else '_',
                    'comfort_adjustment': attendance.comfort_adjustment if attendance else 0,
                    'food': attendance.food if attendance else False
                }

        return JsonResponse({'success': True, 'attendance_data': attendance_data})
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Invalid date format'})





# @login_required(login_url='/')
# def update_operation(request):
#     if request.method == 'POST':
#         employee_id = request.POST.get('employee_id')
#         operation_value = request.POST.get('operation')

#         try:
#             employee = Employee.objects.get(id=employee_id)
#             employee.operation = operation_value
#             employee.save()

#             print(f"Updated operation: employee={employee_id}, operation={operation_value}")
#             return JsonResponse({'success': True, 'operation': employee.operation})
#         except Employee.DoesNotExist:
#             return JsonResponse({'success': False, 'error': 'Employee not found'})
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})
#     return JsonResponse({'success': False, 'error': 'Invalid request'})


























# @login_required
# def attendance_record(request):
#     employees = Employee.objects.all().order_by('sort_number')
#     start_date = request.GET.get('start_date', datetime.today().date().strftime('%Y-%m-%d'))
#     start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
#     days = [start_date + timedelta(days=i) for i in range(21)]
    
#     # جمع بيانات الحضور
#     attendance_data = {}
#     for employee in employees:
#         attendance_data[employee.id] = {}
#         for day in days:
#             attendance, created = Attendance.objects.get_or_create(
#                 employee=employee,
#                 date=day,
#                 defaults={'state': '_', 'food': False, 'comfort_adjustment': 0}
#             )
#             # إذا كان السجل جديدًا و"نوبتجي"، نضبط القيم الافتراضية
#             if created and attendance.state == 'نوبتجي':
#                 attendance.comfort_adjustment = 1
#                 attendance.food = True
#                 attendance.save()
#             attendance_data[employee.id][day] = {
#                 'state': attendance.state,
#                 'food': attendance.food,
#                 'comfort_adjustment': attendance.comfort_adjustment
#             }

#     if request.method == 'POST':
#         for employee in employees:
#             for day in days:
#                 state_key = f'state_{employee.id}_{day.strftime("%Y%m%d")}'
#                 food_key = f'food_{employee.id}_{day.strftime("%Y%m%d")}'
#                 comfort_key = f'comfort_{employee.id}_{day.strftime("%Y%m%d")}'
                
#                 state = request.POST.get(state_key, '_')
#                 food = request.POST.get(food_key) == 'on'
#                 comfort_adjustment = int(request.POST.get(comfort_key, '0'))
                
#                 # تحديث السجل
#                 attendance, created = Attendance.objects.get_or_create(
#                     employee=employee,
#                     date=day,
#                     defaults={'state': state, 'food': food, 'comfort_adjustment': comfort_adjustment}
#                 )
#                 if not created:
#                     old_comfort = attendance.comfort_adjustment
#                     attendance.state = state
#                     # لا نفرض food أو comfort_adjustment لـ "نوبتجي"، نتركها للإدخال اليدوي
#                     attendance.food = food
#                     attendance.comfort_adjustment = comfort_adjustment
                    
#                     # تحديث rahatcounter
#                     if state == 'راحة' and attendance.state != 'راحة':  # إذا تغيرت إلى "راحة"
#                         employee.rahatcounter -= 1
#                     elif state != 'راحة' and attendance.state == 'راحة':  # إذا تغيرت من "راحة"
#                         employee.rahatcounter += 1
                    
#                     if old_comfort != comfort_adjustment:
#                         if old_comfort == 1 and comfort_adjustment != 1:
#                             employee.rahatcounter -= 1
#                         elif old_comfort != 1 and comfort_adjustment == 1:
#                             employee.rahatcounter += 1
#                     attendance.save()
#                     employee.save()

#         return redirect('attendance_record')

#     return render(request, 'attendance/attendance_record.html', {
#         'employees': employees,
#         'days': days,
#         'attendance_data': attendance_data,
#         'start_date': start_date,
#     })
    
    




# @login_required(login_url='/')
# def get_rahatcounter(request):
#     employee_id = request.GET.get('employee_id')
#     try:
#         employee = Employee.objects.get(id=employee_id)
#         return JsonResponse({'success': True, 'rahatcounter': employee.rahatcounter})
#     except Employee.DoesNotExist:
#         return JsonResponse({'success': False, 'error': 'Employee not found'})
#     except Exception as e:
#         return JsonResponse({'success': False, 'error': str(e)})
    
    
    


# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from em_data.models import Employee
# from .models import Attendance
# from datetime import datetime
# import json

# from django.shortcuts import render
# from datetime import datetime, timedelta
# from em_data.models import Employee
# from .models import Attendance
# from django.contrib.auth.decorators import login_required

# from django.shortcuts import render
# from datetime import datetime, timedelta
# from em_data.models import Employee
# from .models import Attendance
# from django.contrib.auth.decorators import login_required

# @login_required(login_url='/')
# def manage_single_employee(request):
#     employees = Employee.objects.all().order_by('nickname')
#     employee_id = request.GET.get('employee_id')
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')

#     # Default date range if not provided
#     if not start_date or not end_date:
#         today = datetime.today()
#         if not start_date:
#             start_date = today - timedelta(weeks=5)
#         if not end_date:
#             end_date = today.replace(month=today.month + 2, day=1) - timedelta(days=1)
#     else:
#         start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
#         end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

#     days = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
#     weeks = [days[i:i + 7] for i in range(0, len(days), 7)]

#     attendance_data = {}
#     selected_employee_id = None
#     if employee_id:
#         try:
#             selected_employee = Employee.objects.get(id=employee_id)
#             selected_employee_id = selected_employee.id
#             attendance_records = Attendance.objects.filter(
#                 employee=selected_employee,
#                 date__range=[start_date, end_date]
#             )
#             for record in attendance_records:
#                 date_str = record.date.strftime('%Y%m%d')
#                 attendance_data[selected_employee.id] = attendance_data.get(selected_employee.id, {})
#                 attendance_data[selected_employee.id][date_str] = {
#                     'state': record.state,
#                     'comfort_adjustment': record.comfort_adjustment,
#                     'food': record.food
#                 }
#         except Employee.DoesNotExist:
#             selected_employee_id = None

#     # Get attendance state choices from the model
#     attendance_states = Attendance._meta.get_field('state').choices

#     return render(request, 'attendance/one_employee.html', {
#         'employees': employees,
#         'selected_employee_id': selected_employee_id,
#         'start_date': start_date,
#         'end_date': end_date,
#         'weeks': weeks,
#         'attendance_data': attendance_data,
#         'attendance_states': attendance_states,
#         'stateColors': {
#             '_': 'white',
#             'نوبتجي': '#219C90',
#             'يومي': '#A7D397',
#             'راحة': '#00A9FF',
#             'دورية': '#C70039',
#             'ر بديلة': '#0a2df5',
#             'طارئة': '#FF9130',
#             'مأمورية': '#eb5bad',
#             'مأمورية خ': '#DA0C81',
#             'فرقة': '#BCA37F',
#             'انتداب': '#713ABE',
#             'مرضي': 'yellow',
#             'ج وضع': 'yellow',
#             'خاصه': 'yellow',
#             '8 صباحاً': '#89CFF3',
#             'ت دوري': '#FFF2D8',
#             'ت تكراري': '#EAD7BB',
#             'منحة': '#A0E9FF',
#             'عطلة': '#CDF5FD',
#             'غياب': 'black',
#             'قرار66': 'yellow'
#         }
#     })


# def get_employee_data2(request):
#     """Get basic employee data for the selected employee"""
#     employee_id = request.GET.get('employee_id')
#     if not employee_id:
#         return JsonResponse({'success': False, 'error': 'لم يتم تحديد الموظف'})
    
#     try:
#         employee = Employee.objects.get(id=employee_id)
#         return JsonResponse({
#             'success': True,
#             'employee': {
#                 'id': employee.id,
#                 'operation': employee.operation,
#                 'nickname': employee.nickname
#             }
#         })
#     except Employee.DoesNotExist:
#         return JsonResponse({'success': False, 'error': 'الموظف غير موجود'})
#     except Exception as e:
#         return JsonResponse({'success': False, 'error': str(e)})

# def get_single_employee_attendance_data2(request):
#     """Get attendance data for a specific employee within date range"""
#     employee_id = request.GET.get('employee_id')
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')

#     if not all([employee_id, start_date, end_date]):
#         return JsonResponse({'success': False, 'error': 'البيانات المطلوبة غير كاملة'})

#     try:
#         attendance_records = Attendance.objects.filter(
#             employee_id=employee_id,
#             date__range=[start_date, end_date]
#         ).select_related('employee')

#         # Format attendance data
#         attendance_data = {}
#         for record in attendance_records:
#             date_str = record.date.strftime('%Y%m%d')
#             if employee_id not in attendance_data:
#                 attendance_data[employee_id] = {}
#             attendance_data[employee_id][date_str] = {
#                 'state': record.state,
#                 'comfort_adjustment': record.comfort_adjustment,
#                 'food': record.food
#             }

#         return JsonResponse({
#             'success': True,
#             'attendance_data': attendance_data
#         })
#     except Exception as e:
#         return JsonResponse({'success': False, 'error': str(e)})

# @csrf_exempt
# def update_attendance2(request):
    """Update attendance records"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'})

    try:
        # Get changes from the request
        changes = {}
        for key, value in request.POST.items():
            if key.startswith('changes['):
                parts = key.split('[')
                change_key = parts[1].rstrip(']')
                field = parts[2].rstrip(']')
                if change_key not in changes:
                    changes[change_key] = {}
                changes[change_key][field] = value

        # Process each change
        for change in changes.values():
            employee_id = change.get('employee_id')
            date_str = change.get('selected_date')
            selected_value = change.get('selected_value')
            comfort_adjustment = change.get('comfort_adjustment')
            food = change.get('food')
            source = change.get('source')

            if not all([employee_id, date_str]):
                continue

            # Convert date format
            date = datetime.strptime(date_str, '%Y%m%d').date()

            # Get or create attendance record
            attendance, created = Attendance.objects.get_or_create(
                employee_id=employee_id,
                date=date,
                defaults={
                    'state': '_',
                    'food': False,
                    'comfort_adjustment': 0
                }
            )

            # Update fields if provided
            if selected_value and source == 'select':
                attendance.state = selected_value
            if comfort_adjustment is not None and source == 'checkbox':
                attendance.comfort_adjustment = int(comfort_adjustment)
            if food is not None and source == 'checkbox':
                attendance.food = bool(int(food))

            attendance.save()

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})