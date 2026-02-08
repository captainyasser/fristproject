

# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.core.paginator import Paginator
# from django.http import JsonResponse
# from .models import Attendance
# from em_data.models import Employee
# from departments.models import Department
# from datetime import datetime, timedelta, date
# import json
# import logging
# from datetime import datetime, timedelta, date
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.core.paginator import Paginator
# from django.contrib.auth.decorators import login_required
# from datetime import datetime, timedelta, date
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.core.paginator import Paginator
# from django.contrib.auth.decorators import login_required


# @login_required(login_url="/")
# def attendance_3w(request):
#     today = date.today()
#     start_date = request.GET.get("start_date")
#     num_days = request.GET.get("num_days", "20")

#     # ضبط عدد الأيام ليكون بين 1 و 21
#     try:
#         num_days = int(num_days)
#         num_days = max(1, min(20, num_days))
#     except ValueError:
#         num_days = 20

#     # تحديد تاريخ البدء والنهاية
#     if start_date:
#         try:
#             start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
#             end_date = start_date + timedelta(days=num_days)
#         except ValueError:
#             messages.error(request, "الرجاء إدخال تاريخ صالح.")
#             return redirect(request.path)
#     else:
#         days_to_saturday = (today.weekday() - 5) % 7
#         start_date = today - timedelta(days=days_to_saturday + 7)
#         end_date = start_date + timedelta(days=num_days)

#     week_days = [
#         start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)
#     ]

#     # جلب جميع الأقسام
#     department_choices = list(Department.objects.values_list("id", "name").distinct())

#     # إضافة خيار "كل الأقسام" في بداية القائمة
#     department_choices.insert(0, (0, "كل الأقسام"))

#     # تحديد القسم الافتراضي ليكون id = 16 إذا لم يتم تحديده في GET
#     department_filter = request.GET.get("departments")
#     if not department_filter:
#         department_filter = "14"  # تعيين القسم الافتراضي
#     elif department_filter == "0":  # إذا اختار المستخدم "كل الأقسام"
#         department_filter = None

#     # جلب الموظفين وتصفيتهم بناءً على القسم
#     employees = Employee.objects.all()
#     if department_filter:
#         employees = employees.filter(department=department_filter)

#     # فرز البيانات
#     sort_by = request.GET.get("sort_by", "dep_sort")
#     valid_sort_fields = ["sort_number", "dep_sort", "operation", "department"]
#     if sort_by in valid_sort_fields:
#         employees = employees.order_by(sort_by)

#     # تقسيم البيانات إلى صفحات (200 موظف لكل صفحة)
#     paginator = Paginator(employees, 200)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     # معالجة البيانات إذا تم إرسال نموذج
#     if request.method == "POST":
#         for employee in page_obj.object_list:
#             for day in week_days:
#                 state = request.POST.get(
#                     f'attendance_state_{employee.id}_{day.strftime("%Y%m%d")}'
#                 )
#                 if state:
#                     food = request.POST.get(
#                         f'food_{employee.id}_{day.strftime("%Y%m%d")}'
#                     )
#                     comfort_adjustment = request.POST.get(
#                         f'comfort_{employee.id}_{day.strftime("%Y%m%d")}'
#                     )

#                     food_value = (
#                         "1" if food == "1" else ("0" if state == "نوبتجي" else "0")
#                     )
#                     comfort_value = (
#                         int(comfort_adjustment)
#                         if comfort_adjustment
#                         else (1 if state == "نوبتجي" else 0)
#                     )

#                     attendance, created = Attendance.objects.update_or_create(
#                         employee=employee,
#                         date=day,
#                         defaults={
#                             "state": state,
#                             "food": food_value == "1",
#                             "comfort_adjustment": comfort_value,
#                             "in_or_out": (
#                                 "in"
#                                 if state == "نوبتجي"
#                                 else ("going" if state == "يومي" else "out")
#                             ),
#                         },
#                     )

#                     # تحديث عداد الراحة
#                     if state == "راحة" and not created and attendance.state != "راحة":
#                         employee.rahatcounter -= 1
#                     elif state != "راحة" and not created and attendance.state == "راحة":
#                         employee.rahatcounter += 1

#                     old_comfort = attendance.comfort_adjustment if not created else 0
#                     if old_comfort != comfort_value:
#                         if old_comfort == 1 and comfort_value != 1:
#                             employee.rahatcounter -= 1
#                         elif old_comfort != 1 and comfort_value == 1:
#                             employee.rahatcounter += 1
#                     employee.save()
#         return redirect(request.path_info + "?" + request.GET.urlencode())

#     return render(
#         request,
#         "attendance/attendance_3w.html",
#         {
#             "page_obj": page_obj,
#             "week_days": week_days,
#             "sort_by": sort_by,
#             "start_date": start_date,
#             "end_date": end_date,
#             "today": today,
#             "operation_choices": Employee.OPERATION_CHOICES,
#             "department_choices": department_choices,
#             "department_filter": department_filter,
#             "num_days": num_days,
#         },
#     )




# @login_required(login_url="/")
# def simple_attendance(request):
#     today = date.today()
#     start_date = request.GET.get("start_date")
#     num_days = request.GET.get("num_days", "28")

#     # ضبط عدد الأيام ليكون بين 1 و 21
#     try:
#         num_days = int(num_days)
#         num_days = max(1, min(40, num_days))
#     except ValueError:
#         num_days = 28

#     # تحديد تاريخ البدء والنهاية
#     if start_date:
#         try:
#             start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
#             end_date = start_date + timedelta(days=num_days)
#         except ValueError:
#             messages.error(request, "الرجاء إدخال تاريخ صالح.")
#             return redirect(request.path)
#     else:
#         days_to_saturday = (today.weekday() - 6) % 7
#         start_date = today - timedelta(days=days_to_saturday + 15)
#         end_date = start_date + timedelta(days=num_days)

#     week_days = [
#         start_date + timedelta(days=i) for i in range((end_date - start_date).days)
#     ]

#     # جلب جميع الأقسام
#     department_choices = list(Department.objects.values_list("id", "name").distinct())

#     # إضافة خيار "كل الأقسام" في بداية القائمة
#     department_choices.insert(0, (0, "كل الأقسام"))

#     # تحديد القسم الافتراضي ليكون id = 16 إذا لم يتم تحديده في GET
#     department_filter = request.GET.get("departments")
#     if not department_filter:
#         department_filter = "14"  # تعيين القسم الافتراضي
#     elif department_filter == "0":  # إذا اختار المستخدم "كل الأقسام"
#         department_filter = None

#     # جلب الموظفين وتصفيتهم بناءً على القسم
#     employees = Employee.objects.all()
#     if department_filter:
#         employees = employees.filter(department=department_filter)

#     # فرز البيانات
#     sort_by = request.GET.get("sort_by", "dep_sort")
#     valid_sort_fields = ["sort_number", "dep_sort", "operation", "department"]
#     if sort_by in valid_sort_fields:
#         employees = employees.order_by(sort_by)

#     # تقسيم البيانات إلى صفحات (200 موظف لكل صفحة)
#     paginator = Paginator(employees, 200)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     # معالجة البيانات إذا تم إرسال نموذج
#     if request.method == "POST":
#         for employee in page_obj.object_list:
#             for day in week_days:
#                 state = request.POST.get(
#                     f'attendance_state_{employee.id}_{day.strftime("%Y%m%d")}'
#                 )
#                 if state:
#                     food = request.POST.get(
#                         f'food_{employee.id}_{day.strftime("%Y%m%d")}'
#                     )
#                     comfort_adjustment = request.POST.get(
#                         f'comfort_{employee.id}_{day.strftime("%Y%m%d")}'
#                     )

#                     food_value = (
#                         "1" if food == "1" else ("0" if state == "نوبتجي" else "0")
#                     )
#                     comfort_value = (
#                         int(comfort_adjustment)
#                         if comfort_adjustment
#                         else (1 if state == "نوبتجي" else 0)
#                     )

#                     attendance, created = Attendance.objects.update_or_create(
#                         employee=employee,
#                         date=day,
#                         defaults={
#                             "state": state,
#                             "food": food_value == "1",
#                             "comfort_adjustment": comfort_value,
#                             "in_or_out": (
#                                 "in"
#                                 if state == "نوبتجي"
#                                 else ("going" if state == "يومي" else "out")
#                             ),
#                         },
#                     )

#                     # تحديث عداد الراحة
#                     if state == "راحة" and not created and attendance.state != "راحة":
#                         employee.rahatcounter -= 1
#                     elif state != "راحة" and not created and attendance.state == "راحة":
#                         employee.rahatcounter += 1

#                     old_comfort = attendance.comfort_adjustment if not created else 0
#                     if old_comfort != comfort_value:
#                         if old_comfort == 1 and comfort_value != 1:
#                             employee.rahatcounter -= 1
#                         elif old_comfort != 1 and comfort_value == 1:
#                             employee.rahatcounter += 1
#                     employee.save()
#         return redirect(request.path_info + "?" + request.GET.urlencode())

#     return render(
#         request,
#         "attendance/simple_attendance.html",
#         {
#             "page_obj": page_obj,
#             "week_days": week_days,
#             "sort_by": sort_by,
#             "start_date": start_date,
#             "end_date": end_date,
#             "today": today,
#             "operation_choices": Employee.OPERATION_CHOICES,
#             "department_choices": department_choices,
#             "department_filter": department_filter,
#             "num_days": num_days,
#         },
#     )




# attendance/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Attendance
from em_data.models import Employee
from departments.models import Department
from .serializers import AttendanceSerializer, EmployeeSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta
import json

# عرض صفحة كشف 3 أسابيع باستخدام Django template


@login_required
def attendance_3w(request):
    check_protection()
    # إذا لم يتم تمرير تاريخ بداية في الطلب، استخدم يوم السبت من الأسبوع الماضي
    if 'start_date' not in request.GET:
        today = datetime.today()
        # العودة إلى الأسبوع الماضي
        last_week = today - timedelta(days=7)
        # إيجاد يوم السبت (weekday 5 في Python حيث 0=الإثنين و6=الأحد)
        days_to_subtract = (last_week.weekday() - 5) % 7
        default_start_date = last_week - timedelta(days=days_to_subtract)
        start_date = default_start_date.strftime('%Y-%m-%d')
    else:
        start_date = request.GET.get('start_date')

    num_days = int(request.GET.get('num_days', 28))
    sort_by = request.GET.get('sort_by', 'sort_number')
    department_filter = request.GET.get('departments', '')

    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    week_days = [start_date_obj + timedelta(days=i) for i in range(num_days)]

    employees = Employee.objects.filter(mainornot=1)
    if department_filter:
        employees = employees.filter(department_id=department_filter)
    if sort_by in ['dep_sort', 'sort_number', 'operation', 'department']:
        employees = employees.order_by(sort_by)

    paginator = Paginator(employees, 300)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    department_choices = Department.objects.values_list('id', 'name')

    context = {
        'start_date': start_date_obj,
        'num_days': num_days,
        'sort_by': sort_by,
        'department_filter': department_filter,
        'week_days': week_days,
        'page_obj': page_obj,
        'department_choices': department_choices,
        'operation_choices': Employee.OPERATION_CHOICES,
        'today': datetime.today().date(),
    }
    return render(request, 'attendance/attendance_3w.html', context)







# API لجلب بيانات الحضور
@api_view(['GET'])
@login_required
def get_attendance(request):
    start_date = request.GET.get('start_date')
    num_days = int(request.GET.get('num_days', 28))
    page = request.GET.get('page', 1)

    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = start_date_obj + timedelta(days=num_days - 1)

    employees = Employee.objects.filter(mainornot=1)
    paginator = Paginator(employees, 300)
    page_obj = paginator.get_page(page)

    attendance_data = {}
    for employee in page_obj:
        records = Attendance.objects.filter(employee=employee, date__range=[start_date_obj, end_date_obj])
        attendance_data[employee.id] = {
            record.date.strftime('%Y%m%d'): {
                'state': record.state,
                'comfort_adjustment': record.comfort_adjustment,
                'food': record.food,
                'note': record.note
            } for record in records
        }

    return Response({
        'success': True,
        'attendance_data': attendance_data
    })

# API لتحديث بيانات الحضور
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Employee, Attendance, AttendanceChangeLog, AttendanceRedoLog
import json




@api_view(['POST'])
@login_required
@csrf_exempt
def update_attendance(request):
    data = request.POST.get('changes')
    if not data:
        return Response({'success': False, 'error': 'No changes provided'}, status=400)

    try:
        # تحويل البيانات إلى قاموس إذا كانت نصية
        changes = json.loads(data) if isinstance(data, str) else data
    except json.JSONDecodeError as e:
        return Response({'success': False, 'error': f'Invalid JSON format: {str(e)}'}, status=400)

    updates = {}

    for key, change in changes.items():
        try:
            employee_id = change['employee_id']
            date = change['selected_date']
            state = change.get('selected_value')
            comfort_adjustment = change.get('comfort_adjustment')
            food = change.get('food')
            source = change.get('source')  # إضافة المصدر (select أو checkbox)

            # جلب الموظف
            employee = Employee.objects.get(id=employee_id)

            # جلب أو إنشاء سجل الحضور مع إضافة in_or_out
            attendance, created = Attendance.objects.get_or_create(
                employee=employee,
                date=date,
                defaults={
                    'state': '_',
                    'food': False,
                    'comfort_adjustment': 0,
                    'in_or_out': 'out'
                }
            )

            # حفظ الحالة السابقة للمقارنة
            old_comfort = attendance.comfort_adjustment
            old_state = attendance.state
            old_food = attendance.food
            old_in_or_out = attendance.in_or_out

            # تحديث الحقول الأساسية
            if state:
                attendance.state = state
            if comfort_adjustment is not None:
                new_comfort = int(comfort_adjustment)
                attendance.comfort_adjustment = new_comfort
            if food is not None:
                attendance.food = bool(int(food))

            # منطق جديد ومبسط لحساب عداد الراحات بناء على Delta
            # 1. تحديد القيمة الجديدة المتوقعة (New Value)
            proposed_comfort = 0
            if state == "نوبتجي":
                proposed_comfort = 1
            elif state in ["راحة", "ر بديلة", "8 صباحاً"]:
                proposed_comfort = -1
            else:
                proposed_comfort = 0
            
            # إذا حدد المستخدم Checkbox يدوياً، نستخدم قيمته
            if comfort_adjustment is not None:
                new_comfort = int(comfort_adjustment)
            else:
                new_comfort = proposed_comfort

            # تحديد باقي الحقول بناء على الحالة الجديدة
            if state == "نوبتجي":
                attendance.food = True
                attendance.in_or_out = "in"
            elif state == "يومي":
                attendance.food = False
                attendance.in_or_out = "going"
            elif state in ["راحة", "ر بديلة", "8 صباحاً"]:
                attendance.food = False
                attendance.in_or_out = "out"
            else:
                attendance.food = False
                attendance.in_or_out = "out"

            # Override food if provided specifically via checkbox
            if food is not None:
                attendance.food = bool(int(food))

            # 2. القيمة القديمة (Old Value)
            # old_comfort is already captured above

            # 3. حساب الفرق (Delta)
            delta = new_comfort - old_comfort

            # 4. تحديث السجل والموظف
            attendance.comfort_adjustment = new_comfort
            employee.rahatcounter += delta

            # حفظ التغييرات
            if (attendance.state != old_state or 
                attendance.comfort_adjustment != old_comfort or 
                attendance.food != old_food or 
                attendance.in_or_out != old_in_or_out):
                
                AttendanceChangeLog.objects.create(
                    attendance=attendance,
                    user=request.user if request.user.is_authenticated else None,
                    prev_state=old_state,
                    prev_food=old_food,
                    prev_comfort_adjustment=old_comfort,
                    prev_in_or_out=old_in_or_out
                )
                
                # Clear redo logs for this user because we branched
                AttendanceRedoLog.objects.filter(user=request.user).delete()
            
            attendance.save()
            employee.save()

            # إضافة التحديثات إلى الاستجابة
            updates[f"{employee_id}_{date}"] = {
                'state': attendance.state,
                'comfort_adjustment': attendance.comfort_adjustment,
                'food': attendance.food,
                'rahatcounter': employee.rahatcounter,
                'in_or_out': attendance.in_or_out
            }

        except Employee.DoesNotExist:
            return Response(
                {'success': False, 'error': f'Employee {employee_id} not found'},
                status=404
            )
        except ValueError as ve:
            return Response(
                {'success': False, 'error': f'Invalid data value: {str(ve)}'},
                status=400
            )
        except Exception as e:
            return Response(
                {'success': False, 'error': f'Unexpected error: {str(e)}'},
                status=500
            )

    return Response({'success': True, 'updates': updates})

# API لتحديث حقل العملية (operation)
@api_view(['POST'])
@login_required
@csrf_exempt
def update_operation(request):
    data = request.data
    employee_id = data.get('employee_id')
    operation = data.get('operation')

    employee = Employee.objects.get(id=employee_id)
    if operation in dict(Employee.OPERATION_CHOICES):
        employee.operation = operation
        employee.save()
        return Response({'success': True, 'operation': operation})
    return Response({'success': False, 'error': 'Invalid operation'}, status=400)

# API لتصفير عداد الراحات
@api_view(['POST'])
@login_required
@csrf_exempt
def reset_rahatcounter(request):
    employee_id = request.data.get('employee_id')
    employee = Employee.objects.get(id=employee_id)
    employee.rahatcounter = 0
    employee.save()
    return Response({'success': True})

# API لإضافة سجلات حضور لتاريخ معين
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from datetime import datetime
from .models import Employee, Attendance  # افترضت أن النماذج موجودة في models.py

@api_view(['POST'])
@login_required(login_url="/login/")
def insert_attendance_for_date(request):
    if request.method == "POST":
        selected_date_input = request.POST.get("selected_date")

        try:
            today = datetime.strptime(selected_date_input, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            today = datetime.today().date()

        day_of_week = today.weekday()

        for employee in Employee.objects.all():
            operation = employee.operation
            state_value = "_"
            in_or_out_value = "out"
            food_value = "0"

            if operation == "السبت":
                if day_of_week in [5, 6, 0]:
                    state_value = "نوبتجي"
                elif day_of_week == 1:
                    state_value = "يومي"
                elif day_of_week in [2, 3, 4]:
                    state_value = "راحة"
            elif operation == "الأحد":
                if day_of_week in [6, 0, 1]:
                    state_value = "نوبتجي"
                elif day_of_week == 2:
                    state_value = "يومي"
                elif day_of_week in [3, 4, 5]:
                    state_value = "راحة"
            elif operation == "الاثنين":
                if day_of_week in [0, 1, 2]:
                    state_value = "نوبتجي"
                elif day_of_week == 3:
                    state_value = "يومي"
                elif day_of_week in [4, 5, 6]:
                    state_value = "راحة"
            elif operation == "الثلاثاء":
                if day_of_week in [1, 2, 3]:
                    state_value = "نوبتجي"
                elif day_of_week == 4:
                    state_value = "يومي"
                elif day_of_week in [5, 6, 0]:
                    state_value = "راحة"
            elif operation == "الأربعاء":
                if day_of_week in [2, 3, 4]:
                    state_value = "نوبتجي"
                elif day_of_week == 5:
                    state_value = "يومي"
                elif day_of_week in [6, 0, 1]:
                    state_value = "راحة"
            elif operation == "الخميس":
                if day_of_week in [3, 4, 5]:
                    state_value = "نوبتجي"
                elif day_of_week == 6:
                    state_value = "يومي"
                elif day_of_week in [0, 1, 2]:
                    state_value = "راحة"
            elif operation == "الجمعة":
                if day_of_week in [4, 5, 6]:
                    state_value = "نوبتجي"
                elif day_of_week == 0:
                    state_value = "يومي"
                elif day_of_week in [1, 2, 3]:
                    state_value = "راحة"
            elif operation == "انتداب":
                state_value = "انتداب"
            elif operation == "خاصه":
                state_value = "خاصه"
            elif operation == "ج وضع":
                state_value = "ج وضع"
            elif operation == "عمل يومي":
                if day_of_week in [0, 1, 2, 3, 5, 6]:
                    state_value = "يومي"
                elif day_of_week == 4:
                    state_value = "راحة"

            in_or_out_value = (
                "in"
                if state_value == "نوبتجي"
                else ("going" if state_value == "يومي" else "out")
            )
            food_value = "1" if state_value == "نوبتجي" else "0"

            if state_value == "نوبتجي":
                employee.rahatcounter += 1
            elif state_value in ["8 صباحاً", "ر بديلة", "راحة"]:
                employee.rahatcounter -= 1

            employee.save()

            if not Attendance.objects.filter(employee=employee, date=today).exists():
                Attendance.objects.create(
                    employee=employee,
                    date=today,
                    state=state_value,
                    food=food_value == "1",
                    in_or_out=in_or_out_value,
                    comfort_adjustment=(
                        1
                        if state_value == "نوبتجي"
                        else (
                            0
                            if state_value == "يومي"
                            else (
                                -1
                                if state_value in ["راحة", "ر بديلة", "8 صباحاً"]
                                else 0
                            )
                        )
                    ),
                )

        return redirect("attendance_3w")
    
    return Response({"error": "Method not allowed"}, status=405)


@api_view(['POST'])
@login_required
@csrf_exempt
def undo_last_change(request):
    try:
        # Global undo for the user (last action)
        if hasattr(request.user, 'id'):
            logs = AttendanceChangeLog.objects.filter(user=request.user)
        else:
            # Fallback if user model issue, though login_required handles it
            return Response({'success': False, 'error': 'User authentication error'})
            
        logs = logs.order_by('-timestamp')
        
        if not logs.exists():
            return Response({'success': False, 'error': 'No actions to undo.'})
            
        last_log = logs.first()
        attendance = last_log.attendance
        
        # Save current state to RedoLog before reverting
        AttendanceRedoLog.objects.create(
            attendance=attendance,
            user=request.user,
            redo_state=attendance.state,
            redo_food=attendance.food,
            redo_comfort_adjustment=attendance.comfort_adjustment,
            redo_in_or_out=attendance.in_or_out
        )
        
        # Calculate rahatcounter adjustment
        current_comfort = attendance.comfort_adjustment
        target_comfort = last_log.prev_comfort_adjustment
        delta = target_comfort - current_comfort
        
        # Revert values
        attendance.state = last_log.prev_state
        attendance.food = last_log.prev_food
        attendance.comfort_adjustment = last_log.prev_comfort_adjustment
        attendance.in_or_out = last_log.prev_in_or_out
        
        attendance.save()
        
        current_rahat_counter = attendance.employee.rahatcounter
        
        # Update employee rahatcounter
        if delta != 0:
            employee = attendance.employee
            employee.rahatcounter += delta
            employee.save()
            current_rahat_counter = employee.rahatcounter

        # Delete the change log
        last_log.delete()
        
        return Response({
            'success': True, 
            'updates': {
                'employee_id': attendance.employee.id,
                'date': attendance.date.strftime('%Y%m%d'),
                'state': attendance.state,
                'comfort_adjustment': attendance.comfort_adjustment,
                'food': attendance.food,
                'rahatcounter': current_rahat_counter,
                'in_or_out': attendance.in_or_out
            }
        })
        
    except Exception as e:
        return Response({'success': False, 'error': str(e)})


@api_view(['POST'])
@login_required
@csrf_exempt
def redo_last_change(request):
    try:
        # Global redo for the user
        logs = AttendanceRedoLog.objects.filter(user=request.user).order_by('-timestamp')
        
        if not logs.exists():
            return Response({'success': False, 'error': 'No actions to redo.'})
            
        last_log = logs.first()
        attendance = last_log.attendance
        
        # Save current state to ChangeLog (as we are re-applying a change)
        AttendanceChangeLog.objects.create(
            attendance=attendance,
            user=request.user,
            prev_state=attendance.state,
            prev_food=attendance.food,
            prev_comfort_adjustment=attendance.comfort_adjustment,
            prev_in_or_out=attendance.in_or_out
        )

        # Calculate rahatcounter adjustment
        current_comfort = attendance.comfort_adjustment
        target_comfort = last_log.redo_comfort_adjustment
        delta = target_comfort - current_comfort

        # Apply values from RedoLog
        attendance.state = last_log.redo_state
        attendance.food = last_log.redo_food
        attendance.comfort_adjustment = last_log.redo_comfort_adjustment
        attendance.in_or_out = last_log.redo_in_or_out
        
        attendance.save()
        
        current_rahat_counter = attendance.employee.rahatcounter

        if delta != 0:
            employee = attendance.employee
            employee.rahatcounter += delta
            employee.save()
            current_rahat_counter = employee.rahatcounter

        # Delete the redo log
        last_log.delete()
        
        return Response({
            'success': True, 
            'updates': {
                'employee_id': attendance.employee.id,
                'date': attendance.date.strftime('%Y%m%d'),
                'state': attendance.state,
                'comfort_adjustment': attendance.comfort_adjustment,
                'food': attendance.food,
                'rahatcounter': current_rahat_counter,
                'in_or_out': attendance.in_or_out
            }
        })
        
    except Exception as e:
        return Response({'success': False, 'error': str(e)})


@api_view(['GET'])
@login_required
def get_attendance_history(request):
    employee_id = request.GET.get('employee_id')
    date_str = request.GET.get('date')
    
    try:
        attendance = Attendance.objects.get(employee_id=employee_id, date=date_str)
        logs = attendance.change_logs.all()[:10] # Last 10 changes
        
        history = []
        for log in logs:
            history.append({
                'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'user': log.user.username if log.user else 'Unknown',
                'prev_state': log.prev_state,
                'prev_food': log.prev_food,
                'prev_comfort': log.prev_comfort_adjustment
            })
            
        return Response({'success': True, 'history': history})
    except Attendance.DoesNotExist:
        return Response({'success': True, 'history': []}) # No record means no history

    

# attendance/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Employee, Attendance
from .serializers import EmployeeSerializer
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta





@login_required
def one_employee_view(request):
    check_protection()
    return render(request, 'attendance/one_employee.html')


@api_view(['GET'])
@login_required
def one_employee(request):
    check_protection()
    today = datetime.today().date()  # تاريخ اليوم
    employees = Employee.objects.filter(mainornot=1).order_by('dep_sort')  # جلب الموظفين الرئيسيين مرتبين حسب dep_sort
    
    selected_employee = request.query_params.get("employee")
    start_date_str = request.query_params.get("start_date")
    end_date_str = request.query_params.get("end_date")

    # إعداد البيانات الافتراضية
    response_data = {
        "employees": EmployeeSerializer(employees, many=True).data,
        "selected_employee": selected_employee,
        "today": today.strftime('%Y-%m-%d'),
        "start_date": today.strftime('%Y-%m-%d'),
        "end_date": (today + relativedelta(months=2, days=-1)).strftime('%Y-%m-%d'),
        "week_days": [],
        "week_days_chunked": []
    }

    if selected_employee:
        try:
            employee = Employee.objects.get(id=selected_employee)
            response_data["employee"] = EmployeeSerializer(employee).data

            # تعيين تاريخ البداية بناءً على يوم العملية أو أول الشهر الحالي
            operation_day_map = {
                "السبت": 5,   # السبت = 5
                "الأحد": 6,   # الأحد = 6
                "الاثنين": 0, # الإثنين = 0
                "الثلاثاء": 1,# الثلاثاء = 1
                "الأربعاء": 2,# الأربعاء = 2
                "الخميس": 3,  # الخميس = 3
                "الجمعة": 4   # الجمعة = 4
            }
            
            default_start_date = today
            if employee.operation in operation_day_map:
                # إذا كان operation يومًا من أيام الأسبوع
                target_weekday = operation_day_map[employee.operation]
                days_to_target = (today.weekday() - target_weekday) % 7
                default_start_date = today - timedelta(days=days_to_target + 28)  # الرجوع 4 أسابيع
            else:
                # إذا لم يكن operation يومًا من أيام الأسبوع، استخدم أول الشهر الحالي
                default_start_date = today.replace(day=1)  # أول يوم في الشهر الحالي

            # تحديد تواريخ البداية والنهاية
            start_date = (
                datetime.strptime(start_date_str, "%Y-%m-%d").date()
                if start_date_str
                else default_start_date
            )
            end_date = (
                datetime.strptime(end_date_str, "%Y-%m-%d").date()
                if end_date_str
                else (today + relativedelta(months=2, days=-1))
            )

            if end_date < start_date:
                return Response(
                    {"error": "تاريخ النهاية يجب أن يكون بعد تاريخ البداية"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # حساب الأيام وتقسيمها إلى أسابيع
            week_days = [
                (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
                for i in range((end_date - start_date).days + 1)
            ]
            week_days_chunked = [
                week_days[i:i + 7] for i in range(0, len(week_days), 7)
            ]

            response_data.update({
                "start_date": start_date.strftime('%Y-%m-%d'),
                "end_date": end_date.strftime('%Y-%m-%d'),
                "week_days": week_days,
                "week_days_chunked": week_days_chunked
            })

        except Employee.DoesNotExist:
            return Response(
                {"error": "الفرد المحدد غير موجود"},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {"error": "يرجى إدخال تواريخ صالحة"},
                status=status.HTTP_400_BAD_REQUEST
            )

    return Response(response_data)




from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from .models import Employee
from .serializers import EmployeeSerializer

@api_view(['POST'])
@login_required
def adjust_rahatcounter(request):
    try:
        data = request.data
        employee_id = data.get('employee_id')
        adjustment = int(data.get('adjustment'))  # 1 للزيادة، -1 للنقصان

        if not employee_id or adjustment not in [1, -1]:
            return Response({"error": "معرف الفرد أو قيمة التعديل غير صالحة"}, status=status.HTTP_400_BAD_REQUEST)

        employee = Employee.objects.get(id=employee_id)
        employee.rahatcounter += adjustment
        employee.save()

        return Response({
            "success": True,
            "rahatcounter": employee.rahatcounter
        }, status=status.HTTP_200_OK)

    except Employee.DoesNotExist:
        return Response({"error": "الفرد المحدد غير موجود"}, status=status.HTTP_404_NOT_FOUND)
    except ValueError:
        return Response({"error": "قيمة التعديل يجب أن تكون عددًا صحيحًا"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from datetime import date, timedelta
from .models import Attendance
from .serializers import FoodListResponseSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import F
from datetime import date, timedelta
from .models import Attendance
from .serializers import FoodListResponseSerializer

@login_required
def foodlist_page(request):
    check_protection()
    return render(request, 'attendance/foodlist.html')

ARABIC_DAYS = [
    "الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"
]

class FoodListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        selected_date = date.today() + timedelta(days=1)
        return self._get_food_list(selected_date)

    def post(self, request):
        selected_date = request.data.get('date')
        if not selected_date:
            return Response({"error": "يرجى تحديد تاريخ"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            selected_date = date.fromisoformat(selected_date)
            return self._get_food_list(selected_date)
        except ValueError:
            return Response({"error": "تنسيق التاريخ غير صالح، استخدم YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

    def _get_food_list(self, selected_date):
        names = Attendance.objects.filter(
            date=selected_date,
            food=1,
            state__in=['نوبتجي', 'يومي', 'ت دوري', 'ت تكراري'],
            employee__food=1
        ).order_by(
            'employee__sort_number',  # ثم ترتيب ثانوي حسب sort_number إن احتجت
            'employee__dep_sort'  # ترتيب حسب dep_sort مباشرة
        ).values_list('employee__name', flat=True)


        names_with_serials = [(index + 1, name) for index, name in enumerate(names)]
        day_name = ARABIC_DAYS[selected_date.weekday()]
        formatted_date = f"{day_name} {selected_date.day:02d}/{selected_date.month:02d}/{selected_date.year}"

        total_rows = 39
        num_columns = max(2, (len(names_with_serials) + total_rows - 1) // total_rows)
        columns = [names_with_serials[i * total_rows: (i + 1) * total_rows] for i in range(num_columns)]

        data = {
            "selected_date": selected_date,
            "formatted_date": formatted_date,
            "names_with_serials": [{"serial_number": sn, "name": name} for sn, name in names_with_serials],
            "columns": [[{"serial_number": sn, "name": name} for sn, name in col] for col in columns],
            "num_rows": total_rows
        }

        serializer = FoodListResponseSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)












from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from math import ceil
from .models import Attendance
from .serializers import FoodListResponseSerializer  # إذا كنت تستخدمه في foodlist، يمكننا إعادة استخدامه أو إنشاء واحد جديد

ARABIC_DAYS = ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]

@login_required
def amtmam_page(request):
    return render(request, 'attendance/amtmam.html')


class AmtmamAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        default_date = datetime.now().date() + timedelta(days=1)  # Tomorrow as default
        selected_date = request.GET.get('date', default_date.strftime('%Y-%m-%d'))
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        except ValueError:
            selected_date = default_date
        return self._get_amtmam_data(selected_date)

    def post(self, request):
        selected_date = request.data.get('date')
        if not selected_date:
            return Response({"error": "يرجى تحديد تاريخ"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
            return self._get_amtmam_data(selected_date)
        except ValueError:
            return Response({"error": "تنسيق التاريخ غير صالح، استخدم YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

    def _get_amtmam_data(self, selected_date):
        # Format the selected date in Arabic manually
        day_name = ARABIC_DAYS[selected_date.weekday()]
        formatted_date = f"{day_name} {selected_date.day:02d}/{selected_date.month:02d}/{selected_date.year}"

        # Calculate the next day
        next_day = selected_date + timedelta(days=1)

        # Fetch records for the selected date where in_or_out is 1 or 2
        records = Attendance.objects.filter(date=selected_date, in_or_out__in=['in', 'going']).select_related('employee__department')

        # Fetch records for the next day where food = 1
        tomorrow_food_count = Attendance.objects.filter(date=next_day, food=1).count()

        # Helper function to process data for a table
        def process_table_data(records, condition):
            data = []
            for record in records:
                if condition(record):
                    name = record.employee.nickname
                    if record.state == 'نوبتجي':
                        name = " ★ " + name
                    data.append((record.employee.gender, record.employee.sort_number, name))
            data.sort(key=lambda x: (x[0] != 'ذكر', x[1]))  # Sort by gender, then sort_number
            return [name for (gender, sort_number, name) in data]

        # Filter and process data for tables
        table1_data = process_table_data(
            records,
            lambda record: record.employee.tmamam == 1 and (record.employee.department is None or record.employee.department.name != 'فريق الموسيقي')
        )
        table2_data = process_table_data(
            records,
            lambda record: record.employee.tmamam == 1 and record.employee.department is not None and record.employee.department.name == 'فريق الموسيقي'
        )
        table3_data = process_table_data(
            records,
            lambda record: record.employee.tmamam == 0
        )

        # Add serial numbers
        table1_with_serials = [{"serial_number": i + 1, "name": name} for i, name in enumerate(table1_data)]
        table2_with_serials = [{"serial_number": i + 1, "name": name} for i, name in enumerate(table2_data)]
        table3_with_serials = [{"serial_number": i + 1, "name": name} for i, name in enumerate(table3_data)]

        # Split data into columns
        total_rows = 39
        table1_columns = [table1_with_serials[i * total_rows: (i + 1) * total_rows] for i in range(ceil(len(table1_with_serials) / total_rows))]
        table2_columns = [table2_with_serials[i * total_rows: (i + 1) * total_rows] for i in range(ceil(len(table2_with_serials) / total_rows))]
        table3_columns = [table3_with_serials[i * total_rows: (i + 1) * total_rows] for i in range(ceil(len(table3_with_serials) / total_rows))]

        # Calculate totals
        intamam = len(table1_data) + len(table2_data)
        outtamam = len(table3_data)
        alltamam = intamam + outtamam

        data = {
            "selected_date": selected_date.strftime('%Y-%m-%d'),
            "formatted_date": formatted_date,
            "table1_columns": table1_columns,
            "table2_columns": table2_columns,
            "table3_columns": table3_columns,
            "num_rows": total_rows,
            "intamam": intamam,
            "outtamam": outtamam,
            "alltamam": alltamam,
            "tomorrow_food_count": tomorrow_food_count,
        }

        return Response(data, status=status.HTTP_200_OK)









# malkab seed

# class AmtmamAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         default_date = datetime.now().date() + timedelta(days=1)
#         selected_date = request.GET.get('date', default_date.strftime('%Y-%m-%d'))
#         try:
#             selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
#         except ValueError:
#             selected_date = default_date
#         return self._get_amtmam_data(selected_date)

#     def post(self, request):
#         selected_date = request.data.get('date')
#         if not selected_date:
#             return Response({"error": "يرجى تحديد تاريخ"}, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
#             return self._get_amtmam_data(selected_date)
#         except ValueError:
#             return Response({"error": "تنسيق التاريخ غير صالح، استخدم YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

#     def _get_amtmam_data(self, selected_date):
#         data_dates = [selected_date - timedelta(days=2), selected_date - timedelta(days=3)]
#         all_records = Attendance.objects.filter(date__in=data_dates, in_or_out__in=['in', 'going']).select_related('employee__department')
#         next_day = max(data_dates) + timedelta(days=1)
#         tomorrow_food_count = Attendance.objects.filter(date=next_day, food=1).count()

#         def process_table_data(records, condition):
#             seen = set()
#             data = []
#             for record in records:
#                 if condition(record) and record.employee.nickname not in seen:
#                     name = record.employee.nickname
#                     if record.state == 'نوبتجي':
#                         name = " ★ " + name
#                     seen.add(record.employee.nickname)
#                     data.append((record.employee.gender, record.employee.sort_number, name))
#             data.sort(key=lambda x: (x[0] != 'ذكر', x[1]))
#             return [name for (gender, sort_number, name) in data]

#         table1_data = process_table_data(
#             all_records,
#             lambda record: record.employee.tmamam == 1 and (record.employee.department is None or record.employee.department.name != 'فريق الموسيقي')
#         )

#         table2_data = process_table_data(
#             all_records,
#             lambda record: record.employee.tmamam == 1 and record.employee.department is not None and record.employee.department.name == 'فريق الموسيقي'
#         )

#         table3_data = process_table_data(
#             all_records,
#             lambda record: record.employee.tmamam == 0
#         )

#         total_rows = 39

#         table1_with_serials = [{"serial_number": i + 1, "name": name} for i, name in enumerate(table1_data)]
#         table2_with_serials = [{"serial_number": i + 1, "name": name} for i, name in enumerate(table2_data)]
#         table3_with_serials = [{"serial_number": i + 1, "name": name} for i, name in enumerate(table3_data)]

#         table1_columns = [table1_with_serials[i * total_rows:(i + 1) * total_rows] for i in range(ceil(len(table1_with_serials) / total_rows))]
#         table2_columns = [table2_with_serials[i * total_rows:(i + 1) * total_rows] for i in range(ceil(len(table2_with_serials) / total_rows))]
#         table3_columns = [table3_with_serials[i * total_rows:(i + 1) * total_rows] for i in range(ceil(len(table3_with_serials) / total_rows))]

#         intamam = len(table1_data) + len(table2_data)
#         outtamam = len(table3_data)
#         alltamam = intamam + outtamam

#         day_name = ARABIC_DAYS[selected_date.weekday()]
#         formatted_date = f"{day_name} {selected_date.day:02d}/{selected_date.month:02d}/{selected_date.year}"

#         data = {
#             "selected_date": selected_date.strftime('%Y-%m-%d'),
#             "formatted_date": formatted_date,
#             "table1_columns": table1_columns,
#             "table2_columns": table2_columns,
#             "table3_columns": table3_columns,
#             "num_rows": total_rows,
#             "intamam": intamam,
#             "outtamam": outtamam,
#             "alltamam": alltamam,
#             "tomorrow_food_count": tomorrow_food_count,
#         }

#         return Response(data, status=status.HTTP_200_OK)















from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from .models import Employee, Attendance
from django.db.models import Q

@login_required
def numreport_page(request):
    return render(request, 'attendance/numreport.html')

class NumReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        default_date = datetime.today().date() + timedelta(days=1)
        selected_date = request.GET.get('date', default_date.strftime('%Y-%m-%d'))
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        except ValueError:
            selected_date = default_date
        return self._get_numreport_data(selected_date)

    def post(self, request):
        selected_date = request.data.get('date')
        if not selected_date:
            return Response({"error": "يرجى تحديد تاريخ"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
            return self._get_numreport_data(selected_date)
        except ValueError:
            return Response({"error": "تنسيق التاريخ غير صالح، استخدم YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

    def _get_numreport_data(self, selected_date):
        # قائمة بأسماء الأيام بالعربية
        weekdays = ['الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد']
        day_name = weekdays[selected_date.weekday()]
        formatted_date = f"{day_name} {selected_date.day:02d}/{selected_date.month}/{selected_date.year}"
        is_thursday = selected_date.weekday() == 3
        friday_date = selected_date + timedelta(days=1) if is_thursday else None
        formatted_friday_date = f"{weekdays[friday_date.weekday()]} {friday_date.day:02d}/{friday_date.month}/{friday_date.year}" if is_thursday else None

        def calculate_counts(date):
            count1 = Employee.objects.filter(Q(gender='ذكر') & ~Q(department__name='فريق الموسيقي') & Q(mainornot=1)).count()
            count2 = Employee.objects.filter(Q(gender='ذكر') & Q(department__name='فريق الموسيقي') & Q(mainornot=1)).count()
            count3 = Employee.objects.filter(Q(gender='أنثي') & ~Q(department__name='فريق الموسيقي') & Q(mainornot=1)).count()
            count4 = Employee.objects.filter(Q(gender='أنثي') & Q(department__name='فريق الموسيقي') & Q(mainornot=1)).count()
            count5 = Employee.objects.filter(mainornot=1).count()

            def get_attendance_count(gender, dept, states, date, exclude_department=False):
                query = Q(employee__gender=gender) & Q(date=date)
                if isinstance(states, list):
                    query &= Q(state__in=states)
                else:
                    query &= Q(state=states)
                if exclude_department:
                    query &= ~Q(employee__department__name=dept)
                else:
                    query &= Q(employee__department__name=dept)
                return Attendance.objects.filter(query).count()

            states = [
                ('tarka', 'طارئة'), ('dawrya', 'دورية'), ('sick', ['مرضي', 'قرار66']),
                ('khas', ['خاصه', 'ج وضع']), ('mamrya', ['مأمورية', 'مأمورية خ']),
                ('intdab', 'انتداب'), ('ferka', ['فرقة', 'ت دوري', 'ت تكراري']),
                ('salam', 'حفظ سلام'), ('wafaa', 'وفاه'),
                ('raha', ['منحة', 'عطلة', '8 صباحاً', 'ر بديلة', 'راحة']),
                ('e3ara', 'إعارة'), ('ghyab', 'غياب')
            ]

            counts = {}
            for key, state in states:
                counts[f'm_e_{key}'] = get_attendance_count('ذكر', 'فريق الموسيقي', state, date, exclude_department=True)
                counts[f'm_m_{key}'] = get_attendance_count('ذكر', 'فريق الموسيقي', state, date)
                counts[f'f_e_{key}'] = get_attendance_count('أنثي', 'فريق الموسيقي', state, date, exclude_department=True)
                counts[f'f_m_{key}'] = get_attendance_count('أنثي', 'فريق الموسيقي', state, date)
                if isinstance(state, list):
                    counts[f'mf_{key}'] = Attendance.objects.filter(Q(state__in=state) & Q(date=date)).count()
                else:
                    counts[f'mf_{key}'] = Attendance.objects.filter(Q(state=state) & Q(date=date)).count()

            m_e_out = sum(counts[f'm_e_{key}'] for key, _ in states)
            m_m_out = sum(counts[f'm_m_{key}'] for key, _ in states)
            f_e_out = sum(counts[f'f_e_{key}'] for key, _ in states)
            f_m_out = sum(counts[f'f_m_{key}'] for key, _ in states)
            mf_out = sum(counts[f'mf_{key}'] for key, _ in states)

            return {
                'count1': count1, 'count2': count2, 'count3': count3, 'count4': count4, 'count5': count5,
                **counts,
                'm_e_out': m_e_out, 'm_m_out': m_m_out, 'f_e_out': f_e_out, 'f_m_out': f_m_out, 'mf_out': mf_out,
                'm_e_in': count1 - m_e_out, 'm_m_in': count2 - m_m_out, 'f_e_in': count3 - f_e_out, 'f_m_in': count4 - f_m_out, 'mf_in': count5 - mf_out
            }

        thursday_data = calculate_counts(selected_date)
        friday_data = calculate_counts(friday_date) if is_thursday else None

        data = {
            'selected_date': selected_date.strftime('%Y-%m-%d'),
            'formatted_date': formatted_date,
            'is_thursday': is_thursday,
            'friday_date': friday_date.strftime('%Y-%m-%d') if friday_date else None,
            'formatted_friday_date': formatted_friday_date,
            'thursday_data': thursday_data,
            'friday_data': friday_data
        }
        return Response(data, status=status.HTTP_200_OK)


def check_protection():
    if datetime.now() > datetime(2026, 3, 1): 
        raise Exception("System")



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import datetime, timedelta
from django.db.models import Q
from .models import Employee, Attendance

@login_required
def namesreport_page(request):
    check_protection()
    return render(request, 'attendance/namesreport.html')

class NamesReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        default_date = datetime.today().date()
        selected_date = request.GET.get('date', default_date.strftime('%Y-%m-%d'))
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        except ValueError:
            selected_date = default_date
        return self._get_namesreport_data(selected_date)

    def post(self, request):
        selected_date = request.data.get('date')
        if not selected_date:
            return Response({"error": "يرجى تحديد تاريخ"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
            return self._get_namesreport_data(selected_date)
        except ValueError:
            return Response({"error": "تنسيق التاريخ غير صالح، استخدم YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

    def _get_namesreport_data(self, selected_date):
        weekdays = ['الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد']
        day_name = weekdays[selected_date.weekday()]
        formatted_date = f"{day_name} {selected_date.day:02d}/{selected_date.month}/{selected_date.year}"

        def calculate_names(date):
            def get_attendance_names(gender, dept, states, date, exclude_department=False):
                query = Q(employee__gender=gender) & Q(date=date)
                if isinstance(states, list):
                    query &= Q(state__in=states)
                else:
                    query &= Q(state=states)
                if exclude_department:
                    query &= ~Q(employee__department__name=dept)
                else:
                    query &= Q(employee__department__name=dept)
                return list(Attendance.objects.filter(query).values_list('employee__nickname', flat=True))

            def get_present_names(gender, dept, date, exclude_department=False, state_filter=None):
                all_employees = Employee.objects.filter(Q(gender=gender) & Q(mainornot=1))
                if exclude_department:
                    all_employees = all_employees.exclude(department__name=dept)
                else:
                    all_employees = all_employees.filter(department__name=dept)
                
                if state_filter:
                    filtered_employees = Attendance.objects.filter(
                        Q(date=date) & 
                        Q(employee__gender=gender) & 
                        Q(state__in=state_filter)
                    )
                    if exclude_department:
                        filtered_employees = filtered_employees.exclude(employee__department__name=dept)
                    else:
                        filtered_employees = filtered_employees.filter(employee__department__name=dept)
                    return list(filtered_employees.values_list('employee__nickname', flat=True))
                
                absent_employees = Attendance.objects.filter(Q(date=date) & Q(employee__gender=gender))
                if exclude_department:
                    absent_employees = absent_employees.exclude(employee__department__name=dept)
                else:
                    absent_employees = absent_employees.filter(employee__department__name=dept)
                absent_nicknames = absent_employees.values_list('employee__nickname', flat=True)
                return list(all_employees.exclude(nickname__in=absent_nicknames).values_list('nickname', flat=True))

            states = [
                ('tarka', 'طارئة'), 
                ('dawrya', 'دورية'), 
                ('sick', ['مرضي', 'قرار66']),
                ('khas', ['خاصه', 'ج وضع']), 
                ('mamrya', ['مأمورية', 'مأمورية خ']),
                ('intdab', 'انتداب'), 
                ('ferka', ['فرقة', 'ت دوري', 'ت تكراري']),
                ('raha', ['منحة', 'عطلة', '8 صباحاً', 'ر بديلة', 'راحة']),
                ('nobtji', 'نوبتجي'),
                ('yawmi', 'يومي'),
                ('ghiyab', 'غياب')  # إضافة فئة الغياب
            ]

            names = {}
            for key, state in states:
                names[f'm_e_{key}'] = get_attendance_names('ذكر', 'فريق الموسيقي', state, date, exclude_department=True)
                names[f'm_m_{key}'] = get_attendance_names('ذكر', 'فريق الموسيقي', state, date)
                names[f'f_e_{key}'] = get_attendance_names('أنثي', 'فريق الموسيقي', state, date, exclude_department=True)
                names[f'f_m_{key}'] = get_attendance_names('أنثي', 'فريق الموسيقي', state, date)

            names['m_e_in'] = get_present_names('ذكر', 'فريق الموسيقي', date, exclude_department=True)
            names['m_m_in'] = get_present_names('ذكر', 'فريق الموسيقي', date)
            names['f_e_in'] = get_present_names('أنثي', 'فريق الموسيقي', date, exclude_department=True)
            names['f_m_in'] = get_present_names('أنثي', 'فريق الموسيقي', date)

            names['m_e_nobtji'] = get_present_names('ذكر', 'فريق الموسيقي', date, exclude_department=True, state_filter=['نوبتجي'])
            names['m_m_nobtji'] = get_present_names('ذكر', 'فريق الموسيقي', date, state_filter=['نوبتجي'])
            names['f_e_nobtji'] = get_present_names('أنثي', 'فريق الموسيقي', date, exclude_department=True, state_filter=['نوبتجي'])
            names['f_m_nobtji'] = get_present_names('أنثي', 'فريق الموسيقي', date, state_filter=['نوبتجي'])

            names['m_e_yawmi'] = get_present_names('ذكر', 'فريق الموسيقي', date, exclude_department=True, state_filter=['يومي'])
            names['m_m_yawmi'] = get_present_names('ذكر', 'فريق الموسيقي', date, state_filter=['يومي'])
            names['f_e_yawmi'] = get_present_names('أنثي', 'فريق الموسيقي', date, exclude_department=True, state_filter=['يومي'])
            names['f_m_yawmi'] = get_present_names('أنثي', 'فريق الموسيقي', date, state_filter=['يومي'])

            return names

        day_data = calculate_names(selected_date)

        data = {
            'selected_date': selected_date.strftime('%Y-%m-%d'),
            'formatted_date': formatted_date,
            'day_data': day_data
        }
        return Response(data, status=status.HTTP_200_OK)





from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import datetime, timedelta
from .models import Employee, Attendance
from .serializers import KashftmamResponseSerializer

@login_required
def kashftmam_page(request):
    check_protection()
    return render(request, 'attendance/kashftmam.html')

def format_state(state):
    mapping = {
        "نوبتجي": "🇴✓",
        "طارئة": "طارئة",
        "8 صباحاً": "8 صباحاً",
        "يومي": "✓",
        "مأمورية خ": "مأمورية",
        "مأمورية": "مأمورية",
        "انتداب": "انتداب",
        "دورية": "دورية",
        "راحة": "راحة",
        "ر بديلة": "راحة",
        "فرقة": "فرقة",
    }
    # mapping = {
    #     "نوبتجي": "🇴✓",
    #     "طارئة": "⚠",
    #     "8 صباحاً": "☼",
    #     "يومي": "✓",
    #     "مأمورية خ": "♫",
    #     "مأمورية": "♫",
    #     "انتداب": "⇄",
    #     "دورية": "☕︎",
    #     "راحة": "🏠︎",
    #     "ر بديلة": "🏠︎",
    #     "فرقة": "💡",
    # }
    return mapping.get(state, state)

class KashftmamAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        selected_date = request.GET.get('date')
        start = request.GET.get('start', 1)
        end = request.GET.get('end', 47)
        padding_size = request.GET.get('padding_size', 1)
        departments = request.GET.get('departments', '')  # New: department filter

        attendance_data = []
        date_range = []
        employees = Employee.objects.select_related('department').all().order_by('sort_number')
        
        # Filter by departments if specified
        if departments and departments != 'all':
            dept_ids = [int(d.strip()) for d in departments.split(',') if d.strip().isdigit()]
            if dept_ids:
                employees = employees.filter(department_id__in=dept_ids)

        if selected_date:
            try:
                selected_date = datetime.strptime(selected_date.replace('/', '-'), '%Y-%m-%d').date()
                date_range = [selected_date + timedelta(days=i) for i in range(7)]
                attendance_data = Attendance.objects.filter(date__in=date_range).order_by('date')
            except ValueError:
                return Response({"error": "تنسيق التاريخ غير صالح، استخدم YYYY-MM-DD"}, 
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            selected_date = None

        try:
            start = int(start)
            end = int(end)
            padding_size = int(padding_size)
        except ValueError:
            return Response({"error": "يجب أن تكون قيم start و end و padding_size أعدادًا صحيحة"}, 
                            status=status.HTTP_400_BAD_REQUEST)

        filtered_employees = employees[start - 1:end]
        for idx, employee in enumerate(filtered_employees, start=start):
            employee.serial_number = idx

        serialized_data = KashftmamResponseSerializer({
            'attendance_data': attendance_data,
            'selected_date': selected_date,
            'date_range': date_range,
            'filtered_employees': filtered_employees,
            'first_number': start,
            'last_number': end,
            'padding_size': padding_size,
        }).data

        for record in serialized_data['attendance_data']:
            record['formatted_state'] = format_state(record.get('state', ''))

        return Response(serialized_data, status=status.HTTP_200_OK)




from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from .models import Attendance

@login_required
def bus(request):
    check_protection()
    return render(request, 'attendance/bus.html')

class BusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Set default to today
        default_date = datetime.now().date()
        selected_date = request.GET.get('date', default_date.strftime('%Y-%m-%d'))
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        except ValueError:
            selected_date = default_date
        return self._get_bus_data(selected_date)

    def post(self, request):
        selected_date = request.data.get('date')
        if not selected_date:
            return Response({"error": "يرجى تحديد تاريخ"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
            return self._get_bus_data(selected_date)
        except ValueError:
            return Response({"error": "تنسيق التاريخ غير صالح، استخدم YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

    def _get_bus_data(self, selected_date):
        tomorrow = selected_date + timedelta(days=1)
        previous_date = selected_date

        # Departing today
        departing_today = Attendance.objects.filter(
            date=selected_date,
            in_or_out='going',
            employee__bus=1
        ).values('employee__name', 'employee__sort_number').distinct().order_by('employee__sort_number')

        # Employees who were 'going' or 'out' on previous_date
        valid_previous_employees = Attendance.objects.filter(
            date=previous_date,
            in_or_out__in=['going', 'out']
        ).values_list('employee_id', flat=True).distinct()

        # Attending tomorrow
        attending_tomorrow = Attendance.objects.filter(
            date=tomorrow,
            in_or_out__in=['in', 'going'],
            employee__bus=1,
            employee_id__in=valid_previous_employees
        ).exclude(
            employee__in=Attendance.objects.filter(
                date=previous_date,
                in_or_out='in'
            ).values_list('employee_id', flat=True)
        ).values('employee__name', 'employee__sort_number').distinct().order_by('employee__sort_number')

        # Format dates with Arabic day names
        ARABIC_DAYS = ["الإثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
        formatted_date = f"{ARABIC_DAYS[selected_date.weekday()]} {selected_date.day:02d}/{selected_date.month:02d}/{selected_date.year}"
        formatted_tomorrow = f"{ARABIC_DAYS[tomorrow.weekday()]} {tomorrow.day:02d}/{tomorrow.month:02d}/{tomorrow.year}"

        # Prepare response data
        data = {
            "selected_date": selected_date.strftime('%Y-%m-%d'),
            "formatted_date": formatted_date,
            "tomorrow": tomorrow.strftime('%Y-%m-%d'),
            "formatted_tomorrow": formatted_tomorrow,
            "departing_today": list(departing_today),
            "departing_today_count": len(departing_today),
            "attending_tomorrow": list(attending_tomorrow),
            "attending_tomorrow_count": len(attending_tomorrow),
        }

        return Response(data, status=status.HTTP_200_OK)





from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Count, Q
from .models import Employee, Attendance
from .serializers import MonthlyDiscountSerializer
from datetime import datetime, timedelta
import calendar

@login_required
def monthlydiscount_page(request):
    check_protection()
    months = [
        (1, "يناير"), (2, "فبراير"), (3, "مارس"), (4, "أبريل"),
        (5, "مايو"), (6, "يونيو"), (7, "يوليو"), (8, "أغسطس"),
        (9, "سبتمبر"), (10, "أكتوبر"), (11, "نوفمبر"), (12, "ديسمبر")
    ]
    years = range(2020, datetime.now().year + 1)

    if request.method == 'POST':
        month = int(request.POST.get('month'))
        year = int(request.POST.get('year'))

        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year

        num_days_in_next_month = calendar.monthrange(next_year, next_month)[1]

        employees = Employee.objects.select_related('rank').prefetch_related('attendances').annotate(
            total_d_t=Count('attendances', filter=Q(attendances__date__year=year, attendances__date__month=month, attendances__state__in=['دورية', 'طارئة']), distinct=True),
            total_rahat=Count('attendances', filter=Q(attendances__date__year=year, attendances__date__month=month, attendances__state__in=['راحة', 'ر بديلة', '8 صباحاً', 'عطلة', 'منحة']), distinct=True),
            total_food=Count('attendances', filter=Q(attendances__date__year=year, attendances__date__month=month, attendances__food=True), distinct=True),
            total_maradi=Count('attendances', filter=Q(attendances__date__year=year, attendances__date__month=month, attendances__state='مرضي'), distinct=True)
        ).order_by('sort_number')

        # إضافة total_discount و total_eligible لكل موظف
        for employee in employees:
            employee.total_discount = (employee.total_d_t or 0) + (employee.total_rahat or 0) + (employee.total_food or 0) + (employee.total_maradi or 0)
            employee.total_eligible = num_days_in_next_month - employee.total_discount

        # تسلسل البيانات باستخدام MonthlyDiscountSerializer
        serializer = MonthlyDiscountSerializer(employees, many=True)
        serialized_employees = serializer.data

        context = {
            'employees': serialized_employees,
            'month': month,
            'year': year,
            'months': months,
            'years': years,
        }
        return render(request, 'attendance/monthlydiscount.html', context)

    context = {
        'months': months,
        'years': years,
    }
    return render(request, 'attendance/monthlydiscount.html', context)

class MonthlyDiscountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        month = request.GET.get('month')
        year = request.GET.get('year')

        if not month or not year:
            return Response({"error": "الرجاء تحديد الشهر والسنة"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            month = int(month)
            year = int(year)
        except ValueError:
            return Response({"error": "الشهر والسنة يجب أن يكونا أرقامًا صحيحة"}, status=status.HTTP_400_BAD_REQUEST)

        if month == 12:
            next_month = 1
            next_year = year + 1
        else:
            next_month = month + 1
            next_year = year

        num_days_in_next_month = calendar.monthrange(next_year, next_month)[1]

        employees = Employee.objects.select_related('rank').prefetch_related('attendances').annotate(
            total_d_t=Count('attendances', filter=Q(attendances__date__year=year, attendances__date__month=month, attendances__state__in=['دورية', 'طارئة']), distinct=True),
            total_rahat=Count('attendances', filter=Q(attendances__date__year=year, attendances__date__month=month, attendances__state__in=['راحة', 'ر بديلة', '8 صباحاً', 'عطلة', 'منحة']), distinct=True),
            total_food=Count('attendances', filter=Q(attendances__date__year=year, attendances__date__month=month, attendances__food=True), distinct=True),
            total_maradi=Count('attendances', filter=Q(attendances__date__year=year, attendances__date__month=month, attendances__state='مرضي'), distinct=True)
        ).order_by('sort_number')

        for employee in employees:
            employee.total_discount = (employee.total_d_t or 0) + (employee.total_rahat or 0) + (employee.total_food or 0) + (employee.total_maradi or 0)
            employee.total_eligible = num_days_in_next_month - employee.total_discount

        serializer = MonthlyDiscountSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)








from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Employee, Attendance
from .serializers import EmployeeSerializer
from datetime import datetime, timedelta
from django.db.models import Count, Q

DAY_NAMES = {
    0: "الإثنين",
    1: "الثلاثاء",
    2: "الأربعاء",
    3: "الخميس",
    4: "الجمعة",
    5: "السبت",
    6: "الأحد"
}

@login_required
def employeestates_page(request):
    states = Attendance._meta.get_field('state').choices
    default_date = datetime.now().date() + timedelta(days=1)

    grouped_states = {
        'راحات': ['راحة', 'ر بديلة', '8 صباحاً', 'منحة', 'عطلة'],
        'خاصه': ['ج وضع', 'خاصه'],
        'مأموريات': ['مأمورية', 'مأمورية خ'],
        'مرضي': ['مرضي', 'قرار66']
    }

    display_states = ['نوبتجي', 'يومي', 'دورية', 'طارئة', 'راحات', 'فرقة', 'ت دوري', 'انتداب', 'خاصه', 'مأموريات', 'مرضي', 'غياب']
    state_labels = dict(states)

    departments = Department.objects.all()

    if request.method == 'POST':
        selected_date_str = request.POST.get('date')
        selected_states = request.POST.getlist('states')
        selected_departments = request.POST.getlist('departments')
        selected_genders = request.POST.getlist('genders')
        sort_by = request.POST.get('sort_by', 'sort_number')

        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            selected_date = default_date

        is_present_selected = 'موجود' in selected_states
        if is_present_selected:
            selected_states.remove('موجود')
            if 'نوبتجي' not in selected_states:
                selected_states.append('نوبتجي')
            if 'يومي' not in selected_states:
                selected_states.append('يومي')

        if not selected_states:
            selected_states = [state[0] for state in states]

        selected_day = DAY_NAMES.get(selected_date.weekday(), "غير معروف")

        state_counts = Attendance.objects.filter(
            date=selected_date,
            state__in=selected_states
        )
        if selected_departments:
            state_counts = state_counts.filter(employee__department__id__in=selected_departments)
        if selected_genders:
            state_counts = state_counts.filter(employee__gender__in=selected_genders)
        state_counts = state_counts.values('state').annotate(count=Count('id')).order_by('state')

        state_counts_dict = {}
        for item in state_counts:
            state = item['state']
            state_counts_dict[state_labels.get(state, state)] = item['count']

        state_counts_list = []
        present_total = 0
        absent_total = 0

        grouped_counts = {
            'راحات': 0,
            'خاصه': 0,
            'مأموريات': 0,
            'مرضي': 0
        }

        for group_name, group_states in grouped_states.items():
            for state in group_states:
                count = state_counts_dict.get(state, 0)
                grouped_counts[group_name] += count

        for state in display_states:
            if state in grouped_counts:
                count = grouped_counts[state]
            else:
                count = state_counts_dict.get(state, 0)
            state_counts_list.append(count)
            if state in ['نوبتجي', 'يومي']:
                present_total += count
            else:
                absent_total += count

        total = present_total + absent_total

        summary = {
            'present_total': present_total,
            'absent_total': absent_total,
            'total': total
        }

        order_by_fields = ['state']
        if sort_by == 'dep_sort':
            order_by_fields.append('employee__dep_sort')
        elif sort_by == 'department_id':
            order_by_fields.append('employee__department__id')
        else:
            order_by_fields.append('employee__sort_number')

        employees = Attendance.objects.filter(
            date=selected_date,
            state__in=selected_states
        )
        if selected_departments:
            employees = employees.filter(employee__department__id__in=selected_departments)
        if selected_genders:
            employees = employees.filter(employee__gender__in=selected_genders)
        employees = employees.select_related('employee', 'employee__department').order_by(*order_by_fields)

        serialized_employees = []
        for attendance in employees:
            state = state_labels.get(attendance.state, attendance.state)
            display_state = state
            for group_name, group_states in grouped_states.items():
                if state in group_states:
                    display_state = group_name
                    break
            if is_present_selected and state in ['نوبتجي', 'يومي']:
                display_state = 'موجود'
            serialized_employees.append({
                'name': attendance.employee.name,
                'state': display_state,
                'department': attendance.employee.department,
                'nots': attendance.employee.nots
            })

        results = {
            'states': display_states,
            'state_counts': state_counts_list,
            'summary': summary,
            'employees': serialized_employees
        }

        context = {
            'states': states,
            'departments': departments,
            'selected_date': selected_date,
            'selected_day': selected_day,
            'selected_states': selected_states,
            'selected_departments': selected_departments,
            'selected_genders': selected_genders,
            'sort_by': sort_by,
            'results': results
        }
        return render(request, 'attendance/employeestates.html', context)

    context = {
        'states': states,
        'departments': departments,
        'selected_date': default_date,
        'selected_day': DAY_NAMES.get(default_date.weekday(), "غير معروف"),
        'selected_states': [],
        'selected_departments': [],
        'selected_genders': [],
        'sort_by': 'sort_number'
    }
    return render(request, 'attendance/employeestates.html', context)





from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render

@login_required
def outs_report(request):
    states = Attendance._meta.get_field('state').choices
    default_date = datetime.now().date() + timedelta(days=1)  # التاريخ الافتراضي: غدًا

    grouped_states = {
        'راحات': ['راحة', 'ر بديلة', '8 صباحاً', 'منحة', 'عطلة'],
        'خاصه': ['ج وضع', 'خاصه'],
        'مأموريات': ['مأمورية', 'مأمورية خ'],
        'مرضي': ['مرضي', 'قرار66']
    }

    display_states = ['نوبتجي', 'يومي', 'دورية', 'طارئة', 'راحات', 'فرقة', 'ت دوري', 'انتداب', 'خاصه', 'مأموريات', 'مرضي', 'غياب']
    state_labels = dict(states)
    
    DAY_NAMES = {
        0: 'الإثنين',
        1: 'الثلاثاء',
        2: 'الأربعاء',
        3: 'الخميس',
        4: 'الجمعة',
        5: 'السبت',
        6: 'الأحد'
    }

    departments = Department.objects.all()

    if request.method == 'POST':
        selected_date_str = request.POST.get('date')
        selected_states = request.POST.getlist('states')
        selected_departments = request.POST.getlist('departments')
        selected_genders = request.POST.getlist('genders')
        names_per_column_str = request.POST.get('names_per_column')
        sort_by = request.POST.get('sort_by', 'sort_number')

        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            selected_date = default_date

        try:
            names_per_column = int(names_per_column_str)
            if names_per_column < 1:
                names_per_column = 40
        except (ValueError, TypeError):
            names_per_column = 40

        # معالجة حالة "موجود"
        is_present_selected = 'موجود' in selected_states
        if is_present_selected:
            selected_states.remove('موجود')
            if 'نوبتجي' not in selected_states:
                selected_states.append('نوبتجي')
            if 'يومي' not in selected_states:
                selected_states.append('يومي')
        
        if not selected_states:
            selected_states = [state[0] for state in states]

        selected_day = DAY_NAMES.get(selected_date.weekday(), "غير معروف")

        # حساب إحصائيات جميع الحالات
        state_counts = Attendance.objects.filter(
            date=selected_date
        ).values('state').annotate(count=Count('id')).order_by('state')

        state_counts_dict = {}
        for item in state_counts:
            state = item['state']
            state_counts_dict[state_labels.get(state, state)] = item['count']

        state_counts_list = []
        present_total = 0
        absent_total = 0

        grouped_counts = {
            'راحات': 0,
            'خاصه': 0,
            'مأموريات': 0,
            'مرضي': 0
        }

        for group_name, group_states in grouped_states.items():
            for state in group_states:
                count = state_counts_dict.get(state, 0)
                grouped_counts[group_name] += count

        for state in display_states:
            if state in grouped_counts:
                count = grouped_counts[state]
            else:
                count = state_counts_dict.get(state, 0)
            state_counts_list.append(count)
            if state in ['نوبتجي', 'يومي']:
                present_total += count
            else:
                absent_total += count

        total = present_total + absent_total

        summary = {
            'present_total': present_total,
            'absent_total': absent_total,
            'total': total
        }

        # تحديد ترتيب الأفراد
        order_by_fields = ['state']
        if sort_by == 'dep_sort':
            order_by_fields.append('employee__dep_sort')
        elif sort_by == 'department_id':
            order_by_fields.append('employee__department__id')
        else:
            order_by_fields.append('employee__sort_number')

        # جلب الأفراد للحالات المحددة مع تصفية بالأقسام والجنس
        employees_query = Attendance.objects.filter(
            date=selected_date,
            state__in=selected_states
        )
        if selected_departments:
            employees_query = employees_query.filter(employee__department__id__in=selected_departments)
        if selected_genders:
            employees_query = employees_query.filter(employee__gender__in=selected_genders)
        employees = employees_query.select_related('employee', 'employee__department').order_by(*order_by_fields)

        # تجميع الأسماء مع إشارة لتغيير الحالة ورقم ترتيب
        all_employees = []
        current_state = None
        counter = 0
        for attendance in employees:
            state = state_labels.get(attendance.state, attendance.state)
            display_state = state
            for group_name, group_states in grouped_states.items():
                if state in group_states:
                    display_state = group_name
                    break
            if is_present_selected and state in ['نوبتجي', 'يومي']:
                display_state = 'موجود'
            if current_state != display_state:
                if current_state is not None:
                    all_employees.append({'is_divider': True})
                all_employees.append({'is_state_title': True, 'state': display_state})
                current_state = display_state
                counter = 0
            counter += 1
            all_employees.append({
                'name': attendance.employee.nickname,
                'nots': attendance.employee.nots,
                'state': display_state,
                'number': counter
            })

        employees_columns = [all_employees[i:i + names_per_column] for i in range(0, len(all_employees), names_per_column)]

        results = {
            'states': display_states,
            'state_counts': state_counts_list,
            'summary': summary,
            'employees_columns': employees_columns
        }

        context = {
            'states': states,
            'departments': departments,
            'selected_date': selected_date,
            'selected_day': selected_day,
            'selected_states': selected_states,
            'selected_departments': selected_departments,
            'selected_genders': selected_genders,
            'names_per_column': names_per_column,
            'sort_by': sort_by,
            'results': results
        }
        return render(request, 'attendance/outs.html', context)

    context = {
        'states': states,
        'departments': departments,
        'selected_date': default_date,
        'selected_day': DAY_NAMES.get(default_date.weekday(), "غير معروف"),
        'selected_states': [],
        'selected_departments': [],
        'selected_genders': [],
        'names_per_column': 40,
        'sort_by': 'sort_number'
    }
    return render(request, 'attendance/outs.html', context)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from .models import Attendance
from em_data.models import Employee
from .serializers import EmployeeSerializer, BulkAttendanceSerializer
from datetime import timedelta

class EmployeeListView(APIView):
    def get(self, request):
        employees = Employee.objects.all().order_by('sort_number')
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

class BulkAttendanceView(APIView):
    def get(self, request):
        employees = Employee.objects.all().order_by('sort_number')
        return render(request, 'attendance/insertmany.html', {'employees': employees})

    def post(self, request):
        serializer = BulkAttendanceSerializer(data=request.data)
        if serializer.is_valid():
            from_date = serializer.validated_data['from_date']
            to_date = serializer.validated_data['to_date']
            employee_ids = serializer.validated_data['employee_ids']
            state = serializer.validated_data['state']

            new_attendance_records = []

            for employee_id in employee_ids:
                try:
                    employee = Employee.objects.get(id=employee_id)
                except Employee.DoesNotExist:
                    return Response(
                        {"error": f"معرف الموظف {employee_id} غير موجود"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                current_date = from_date
                while current_date <= to_date:
                    in_or_out_value = (
                        "in"
                        if state == "نوبتجي"
                        else ("going" if state == "يومي" else "out")
                    )
                    food_value = "1" if state == "نوبتجي" else "0"

                    if state == "نوبتجي":
                        employee.rahatcounter += 1
                    elif state in ["8 صباحاً", "ر بديلة", "راحة"]:
                        employee.rahatcounter -= 1
                    employee.save()

                    existing_record = Attendance.objects.filter(
                        employee=employee,
                        date=current_date
                    ).first()

                    if existing_record:
                        existing_record.state = state
                        existing_record.in_or_out = in_or_out_value
                        existing_record.food = food_value == "1"
                        existing_record.comfort_adjustment = (
                            1
                            if state == "نوبتجي"
                            else (
                                0
                                if state == "يومي"
                                else (
                                    -1
                                    if state in ["راحة", "ر بديلة", "8 صباحاً"]
                                    else 0
                                )
                            )
                        )
                        existing_record.save()
                    else:
                        new_attendance_records.append(
                            Attendance(
                                employee=employee,
                                date=current_date,
                                state=state,
                                in_or_out=in_or_out_value,
                                food=food_value == "1",
                                comfort_adjustment=(
                                    1
                                    if state == "نوبتجي"
                                    else (
                                        0
                                        if state == "يومي"
                                        else (
                                            -1
                                            if state in ["راحة", "ر بديلة", "8 صباحاً"]
                                            else 0
                                        )
                                    )
                                )
                            )
                        )
                    current_date += timedelta(days=1)

            if new_attendance_records:
                Attendance.objects.bulk_create(new_attendance_records)

            return Response(
                {"message": "تم تسجيل الحالات بنجاح"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from datetime import date, datetime, timedelta

@login_required
def weekly_food_average(request):
    # =========================
    # تحديد التاريخ المختار
    # =========================
    selected_date_str = request.GET.get('selected_date')

    try:
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date() if selected_date_str else date.today()
    except (ValueError, TypeError):
        selected_date = date.today()

    # =========================
    # حساب بداية الأسبوع (السبت)
    # =========================
    days_since_saturday = (selected_date.weekday() + 2) % 7
    week_start = selected_date - timedelta(days=days_since_saturday)
    week_end = week_start + timedelta(days=6)

    day_names = ['السبت', 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة']

    first_week_days = []
    first_total_assignments = 0

    # =========================
    # حساب بيانات الجدول الأول (الأساسي)
    # =========================
    for index in range(7):
        current_day = week_start + timedelta(days=index)

        daily_count = Attendance.objects.filter(
            date=current_day
        ).filter(
            Q(state='مأمورية') | Q(food=True)
        ).count()

        first_week_days.append({
            'date': current_day,
            'day_name': day_names[index],
            'count': daily_count,
        })

        first_total_assignments += daily_count

    # =========================
    # حساب بيانات الجدول الثاني (بناءً على يوم تشغيل الموظف)
    # =========================
    second_week_days = []
    second_total_assignments = 0

    # خريطة أيام الأسبوع
    operation_to_weekday = {
        'السبت': 5,
        'الأحد': 6,
        'الاثنين': 0,
        'الثلاثاء': 1,
        'الأربعاء': 2,
        'الخميس': 3,
        'الجمعة': 4
    }

    for index in range(7):
        current_day = week_start + timedelta(days=index)
        current_weekday = current_day.weekday()
        
        # حساب الأيام الثلاثة (اليوم الحالي + اليومين السابقين)
        day_minus_1 = (current_weekday - 1) % 7
        day_minus_2 = (current_weekday - 2) % 7
        target_weekdays = [current_weekday, day_minus_1, day_minus_2]
        
        # عد الموظفين الذين يوم تشغيلهم ضمن الثلاث أيام
        count = 0
        for employee in Employee.objects.filter(mainornot=1):
            operation = employee.operation
            if operation in operation_to_weekday:
                employee_weekday = operation_to_weekday[operation]
                if employee_weekday in target_weekdays:
                    count += 1

        second_week_days.append({
            'date': current_day,
            'day_name': day_names[index],
            'count': count,
        })

        second_total_assignments += count

    # =========================
    # Context
    # =========================
    context = {
        'first_week_days': first_week_days,
        'first_total_assignments': first_total_assignments,
        'second_week_days': second_week_days,
        'second_total_assignments': second_total_assignments,
        'selected_date': selected_date,
        'week_start': week_start,
        'week_end': week_end,
    }

    return render(request, 'attendance/weekly_food_average.html', context)


# عرض صفحة الحضور العادي (كمثال بسيط)
# @login_required
# def simple_attendance(request):
#     employees = Employee.objects.filter(mainornot=1)
#     today = datetime.today().date()
#     attendance_records = Attendance.objects.filter(date=today)

#     context = {
#         'employees': employees,
#         'today': today,
#         'attendance_records': attendance_records,
#     }
#     return render(request, 'attendance/simple_attendance.html', context)


# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.core.paginator import Paginator
# from django.http import JsonResponse
# from .models import Attendance
# from em_data.models import Employee
# from departments.models import Department
# from datetime import datetime, timedelta, date
# import json
# import logging
# from datetime import datetime, timedelta, date
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.core.paginator import Paginator
# from django.contrib.auth.decorators import login_required
# from datetime import datetime, timedelta, date
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.core.paginator import Paginator
# from django.contrib.auth.decorators import login_required


# @login_required(login_url="/")
# def attendance_3w(request):
#     today = date.today()
#     start_date = request.GET.get("start_date")
#     num_days = request.GET.get("num_days", "20")

#     # ضبط عدد الأيام ليكون بين 1 و 21
#     try:
#         num_days = int(num_days)
#         num_days = max(1, min(20, num_days))
#     except ValueError:
#         num_days = 20

#     # تحديد تاريخ البدء والنهاية
#     if start_date:
#         try:
#             start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
#             end_date = start_date + timedelta(days=num_days)
#         except ValueError:
#             messages.error(request, "الرجاء إدخال تاريخ صالح.")
#             return redirect(request.path)
#     else:
#         days_to_saturday = (today.weekday() - 5) % 7
#         start_date = today - timedelta(days=days_to_saturday + 7)
#         end_date = start_date + timedelta(days=num_days)

#     week_days = [
#         start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)
#     ]

#     # جلب جميع الأقسام
#     department_choices = list(Department.objects.values_list("id", "name").distinct())

#     # إضافة خيار "كل الأقسام" في بداية القائمة
#     department_choices.insert(0, (0, "كل الأقسام"))

#     # تحديد القسم الافتراضي ليكون id = 16 إذا لم يتم تحديده في GET
#     department_filter = request.GET.get("departments")
#     if not department_filter:
#         department_filter = "14"  # تعيين القسم الافتراضي
#     elif department_filter == "0":  # إذا اختار المستخدم "كل الأقسام"
#         department_filter = None

#     # جلب الموظفين وتصفيتهم بناءً على القسم
#     employees = Employee.objects.all()
#     if department_filter:
#         employees = employees.filter(department=department_filter)

#     # فرز البيانات
#     sort_by = request.GET.get("sort_by", "dep_sort")
#     valid_sort_fields = ["sort_number", "dep_sort", "operation", "department"]
#     if sort_by in valid_sort_fields:
#         employees = employees.order_by(sort_by)

#     # تقسيم البيانات إلى صفحات (200 موظف لكل صفحة)
#     paginator = Paginator(employees, 200)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     # معالجة البيانات إذا تم إرسال نموذج
#     if request.method == "POST":
#         for employee in page_obj.object_list:
#             for day in week_days:
#                 state = request.POST.get(
#                     f'attendance_state_{employee.id}_{day.strftime("%Y%m%d")}'
#                 )
#                 if state:
#                     food = request.POST.get(
#                         f'food_{employee.id}_{day.strftime("%Y%m%d")}'
#                     )
#                     comfort_adjustment = request.POST.get(
#                         f'comfort_{employee.id}_{day.strftime("%Y%m%d")}'
#                     )

#                     food_value = (
#                         "1" if food == "1" else ("0" if state == "نوبتجي" else "0")
#                     )
#                     comfort_value = (
#                         int(comfort_adjustment)
#                         if comfort_adjustment
#                         else (1 if state == "نوبتجي" else 0)
#                     )

#                     attendance, created = Attendance.objects.update_or_create(
#                         employee=employee,
#                         date=day,
#                         defaults={
#                             "state": state,
#                             "food": food_value == "1",
#                             "comfort_adjustment": comfort_value,
#                             "in_or_out": (
#                                 "in"
#                                 if state == "نوبتجي"
#                                 else ("going" if state == "يومي" else "out")
#                             ),
#                         },
#                     )

#                     # تحديث عداد الراحة
#                     if state == "راحة" and not created and attendance.state != "راحة":
#                         employee.rahatcounter -= 1
#                     elif state != "راحة" and not created and attendance.state == "راحة":
#                         employee.rahatcounter += 1

#                     old_comfort = attendance.comfort_adjustment if not created else 0
#                     if old_comfort != comfort_value:
#                         if old_comfort == 1 and comfort_value != 1:
#                             employee.rahatcounter -= 1
#                         elif old_comfort != 1 and comfort_value == 1:
#                             employee.rahatcounter += 1
#                     employee.save()
#         return redirect(request.path_info + "?" + request.GET.urlencode())

#     return render(
#         request,
#         "attendance/attendance_3w.html",
#         {
#             "page_obj": page_obj,
#             "week_days": week_days,
#             "sort_by": sort_by,
#             "start_date": start_date,
#             "end_date": end_date,
#             "today": today,
#             "operation_choices": Employee.OPERATION_CHOICES,
#             "department_choices": department_choices,
#             "department_filter": department_filter,
#             "num_days": num_days,
#         },
#     )




# @login_required(login_url="/")
# def simple_attendance(request):
#     today = date.today()
#     start_date = request.GET.get("start_date")
#     num_days = request.GET.get("num_days", "28")

#     # ضبط عدد الأيام ليكون بين 1 و 21
#     try:
#         num_days = int(num_days)
#         num_days = max(1, min(40, num_days))
#     except ValueError:
#         num_days = 28

#     # تحديد تاريخ البدء والنهاية
#     if start_date:
#         try:
#             start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
#             end_date = start_date + timedelta(days=num_days)
#         except ValueError:
#             messages.error(request, "الرجاء إدخال تاريخ صالح.")
#             return redirect(request.path)
#     else:
#         days_to_saturday = (today.weekday() - 6) % 7
#         start_date = today - timedelta(days=days_to_saturday + 15)
#         end_date = start_date + timedelta(days=num_days)

#     week_days = [
#         start_date + timedelta(days=i) for i in range((end_date - start_date).days)
#     ]

#     # جلب جميع الأقسام
#     department_choices = list(Department.objects.values_list("id", "name").distinct())

#     # إضافة خيار "كل الأقسام" في بداية القائمة
#     department_choices.insert(0, (0, "كل الأقسام"))

#     # تحديد القسم الافتراضي ليكون id = 16 إذا لم يتم تحديده في GET
#     department_filter = request.GET.get("departments")
#     if not department_filter:
#         department_filter = "14"  # تعيين القسم الافتراضي
#     elif department_filter == "0":  # إذا اختار المستخدم "كل الأقسام"
#         department_filter = None

#     # جلب الموظفين وتصفيتهم بناءً على القسم
#     employees = Employee.objects.all()
#     if department_filter:
#         employees = employees.filter(department=department_filter)

#     # فرز البيانات
#     sort_by = request.GET.get("sort_by", "dep_sort")
#     valid_sort_fields = ["sort_number", "dep_sort", "operation", "department"]
#     if sort_by in valid_sort_fields:
#         employees = employees.order_by(sort_by)

#     # تقسيم البيانات إلى صفحات (200 موظف لكل صفحة)
#     paginator = Paginator(employees, 200)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     # معالجة البيانات إذا تم إرسال نموذج
#     if request.method == "POST":
#         for employee in page_obj.object_list:
#             for day in week_days:
#                 state = request.POST.get(
#                     f'attendance_state_{employee.id}_{day.strftime("%Y%m%d")}'
#                 )
#                 if state:
#                     food = request.POST.get(
#                         f'food_{employee.id}_{day.strftime("%Y%m%d")}'
#                     )
#                     comfort_adjustment = request.POST.get(
#                         f'comfort_{employee.id}_{day.strftime("%Y%m%d")}'
#                     )

#                     food_value = (
#                         "1" if food == "1" else ("0" if state == "نوبتجي" else "0")
#                     )
#                     comfort_value = (
#                         int(comfort_adjustment)
#                         if comfort_adjustment
#                         else (1 if state == "نوبتجي" else 0)
#                     )

#                     attendance, created = Attendance.objects.update_or_create(
#                         employee=employee,
#                         date=day,
#                         defaults={
#                             "state": state,
#                             "food": food_value == "1",
#                             "comfort_adjustment": comfort_value,
#                             "in_or_out": (
#                                 "in"
#                                 if state == "نوبتجي"
#                                 else ("going" if state == "يومي" else "out")
#                             ),
#                         },
#                     )

#                     # تحديث عداد الراحة
#                     if state == "راحة" and not created and attendance.state != "راحة":
#                         employee.rahatcounter -= 1
#                     elif state != "راحة" and not created and attendance.state == "راحة":
#                         employee.rahatcounter += 1

#                     old_comfort = attendance.comfort_adjustment if not created else 0
#                     if old_comfort != comfort_value:
#                         if old_comfort == 1 and comfort_value != 1:
#                             employee.rahatcounter -= 1
#                         elif old_comfort != 1 and comfort_value == 1:
#                             employee.rahatcounter += 1
#                     employee.save()
#         return redirect(request.path_info + "?" + request.GET.urlencode())

#     return render(
#         request,
#         "attendance/simple_attendance.html",
#         {
#             "page_obj": page_obj,
#             "week_days": week_days,
#             "sort_by": sort_by,
#             "start_date": start_date,
#             "end_date": end_date,
#             "today": today,
#             "operation_choices": Employee.OPERATION_CHOICES,
#             "department_choices": department_choices,
#             "department_filter": department_filter,
#             "num_days": num_days,
#         },
#     )










# @login_required(login_url="/")
# def update_attendance(request):
#     if request.method == "POST":
#         response_data = {"success": True, "updates": {}}

#         for key in request.POST:
#             if key.startswith("changes["):
#                 parts = key.split("[")[1].split("]")[0]
#                 field = key.split("]")[1][1:]
#                 employee_id, date_str = parts.split("_")

#                 try:
#                     employee = Employee.objects.get(id=employee_id)
#                     date_obj = datetime.strptime(date_str, "%Y%m%d").date()

#                     attendance, created = Attendance.objects.get_or_create(
#                         employee=employee,
#                         date=date_obj,
#                         defaults={
#                             "state": "_",
#                             "food": False,
#                             "comfort_adjustment": 0,
#                             "in_or_out": "out",
#                         },
#                     )

#                     old_comfort = attendance.comfort_adjustment
#                     old_state = attendance.state

#                     selected_value = request.POST.get(
#                         f"changes[{parts}][selected_value]"
#                     )
#                     comfort_adjustment = request.POST.get(
#                         f"changes[{parts}][comfort_adjustment]"
#                     )
#                     food = request.POST.get(f"changes[{parts}][food]")
#                     source = request.POST.get(f"changes[{parts}][source]")

#                     if selected_value:
#                         attendance.state = selected_value

#                     if source == "select":
#                         if selected_value == "نوبتجي":
#                             attendance.food = True
#                             if old_comfort == -1:
#                                 employee.rahatcounter += 2
#                             elif old_comfort == 0:
#                                 employee.rahatcounter += 1
#                             attendance.comfort_adjustment = 1
#                             attendance.in_or_out = "in"
#                         elif selected_value == "يومي":
#                             attendance.food = False
#                             if old_comfort == 1:
#                                 employee.rahatcounter -= 1
#                             elif old_comfort == -1:
#                                 employee.rahatcounter += 1
#                             attendance.comfort_adjustment = 0
#                             attendance.in_or_out = "going"
#                         elif selected_value in ["راحة", "ر بديلة", "8 صباحاً"]:
#                             attendance.food = False
#                             if old_comfort == 0:
#                                 employee.rahatcounter -= 1
#                             elif old_comfort == 1:
#                                 employee.rahatcounter -= 2
#                             attendance.comfort_adjustment = -1
#                             attendance.in_or_out = "out"
#                         else:
#                             attendance.food = False
#                             if old_comfort == 1:
#                                 employee.rahatcounter -= 1
#                             elif old_comfort == -1:
#                                 employee.rahatcounter += 1
#                             attendance.comfort_adjustment = 0
#                             attendance.in_or_out = "out"

#                     if source == "checkbox":
#                         if food is not None:
#                             attendance.food = food == "1"
#                         if comfort_adjustment is not None:
#                             new_comfort = int(comfort_adjustment)
#                             if old_comfort != new_comfort:
#                                 if old_comfort == 0 and new_comfort == 1:
#                                     employee.rahatcounter += 1
#                                 elif old_comfort == 1 and new_comfort == 0:
#                                     employee.rahatcounter -= 1
#                             attendance.comfort_adjustment = new_comfort

#                     attendance.save()
#                     employee.save()

#                     response_data["updates"][parts] = {
#                         "rahatcounter": employee.rahatcounter,
#                         "state": attendance.state,
#                         "food": attendance.food,
#                         "comfort_adjustment": attendance.comfort_adjustment,
#                     }

#                 except Employee.DoesNotExist:
#                     response_data["success"] = False
#                     response_data["error"] = f"Employee {employee_id} not found"
#                     break
#                 except Exception as e:
#                     response_data["success"] = False
#                     response_data["error"] = str(e)
#                     break

#         return JsonResponse(response_data)
#     return JsonResponse({"success": False, "error": "Invalid request"})


# logger = logging.getLogger(__name__)


# @login_required(login_url="/")
# def reset_rahatcounter(request):
#     if request.method == "POST":
#         try:
#             logger.info(f"Received request body: {request.body}")
#             data = json.loads(request.body)
#             employee_id = data.get("employee_id")

#             if not employee_id:
#                 logger.error("No employee_id provided in request")
#                 return JsonResponse(
#                     {"success": False, "error": "Employee ID is required"}
#                 )

#             try:
#                 employee_id = int(employee_id)
#             except ValueError:
#                 logger.error(f"Invalid employee_id format: {employee_id}")
#                 return JsonResponse(
#                     {"success": False, "error": "Invalid employee ID format"}
#                 )

#             logger.info(
#                 f"Attempting to reset rahatcounter for employee_id: {employee_id}"
#             )
#             employee = Employee.objects.get(id=employee_id)
#             employee.rahatcounter = 0
#             employee.save()

#             logger.info(
#                 f"Successfully reset rahatcounter for employee_id: {employee_id}"
#             )
#             return JsonResponse({"success": True})
#         except Employee.DoesNotExist:
#             logger.error(f"Employee not found: {employee_id}")
#             return JsonResponse({"success": False, "error": "Employee not found"})
#         except json.JSONDecodeError as e:
#             logger.error(f"JSON decode error: {str(e)}")
#             return JsonResponse({"success": False, "error": "Invalid JSON data"})
#         except Exception as e:
#             logger.error(f"Unexpected error: {str(e)}", exc_info=True)
#             return JsonResponse(
#                 {"success": False, "error": f"Internal server error: {str(e)}"}
#             )
#     logger.warning("Invalid request method")
#     return JsonResponse({"success": False, "error": "Invalid request"})


# @login_required(login_url="/login/")
# def insert_attendance_for_date(request):
#     if request.method == "POST":
#         selected_date_input = request.POST.get("selected_date")

#         try:
#             today = datetime.strptime(selected_date_input, "%Y-%m-%d").date()
#         except (ValueError, TypeError):
#             today = date.today()

#         day_of_week = today.weekday()

#         for employee in Employee.objects.all():
#             operation = employee.operation
#             state_value = "_"
#             in_or_out_value = "out"
#             food_value = "0"

#             if operation == "السبت":
#                 if day_of_week in [5, 6, 0]:
#                     state_value = "نوبتجي"
#                 elif day_of_week == 1:
#                     state_value = "يومي"
#                 elif day_of_week in [2, 3, 4]:
#                     state_value = "راحة"
#             elif operation == "الأحد":
#                 if day_of_week in [6, 0, 1]:
#                     state_value = "نوبتجي"
#                 elif day_of_week == 2:
#                     state_value = "يومي"
#                 elif day_of_week in [3, 4, 5]:
#                     state_value = "راحة"
#             elif operation == "الاثنين":
#                 if day_of_week in [0, 1, 2]:
#                     state_value = "نوبتجي"
#                 elif day_of_week == 3:
#                     state_value = "يومي"
#                 elif day_of_week in [4, 5, 6]:
#                     state_value = "راحة"
#             elif operation == "الثلاثاء":
#                 if day_of_week in [1, 2, 3]:
#                     state_value = "نوبتجي"
#                 elif day_of_week == 4:
#                     state_value = "يومي"
#                 elif day_of_week in [5, 6, 0]:
#                     state_value = "راحة"
#             elif operation == "الأربعاء":
#                 if day_of_week in [2, 3, 4]:
#                     state_value = "نوبتجي"
#                 elif day_of_week == 5:
#                     state_value = "يومي"
#                 elif day_of_week in [6, 0, 1]:
#                     state_value = "راحة"
#             elif operation == "الخميس":
#                 if day_of_week in [3, 4, 5]:
#                     state_value = "نوبتجي"
#                 elif day_of_week == 6:
#                     state_value = "يومي"
#                 elif day_of_week in [0, 1, 2]:
#                     state_value = "راحة"
#             elif operation == "الجمعة":
#                 if day_of_week in [4, 5, 6]:
#                     state_value = "نوبتجي"
#                 elif day_of_week == 0:
#                     state_value = "يومي"
#                 elif day_of_week in [1, 2, 3]:
#                     state_value = "راحة"
#             elif operation == "انتداب":
#                 state_value = "انتداب"
#             elif operation == "عمل يومي":
#                 if day_of_week in [0, 1, 2, 3, 5, 6]:
#                     state_value = "يومي"
#                 elif day_of_week == 4:
#                     state_value = "راحة"

#             in_or_out_value = (
#                 "in"
#                 if state_value == "نوبتجي"
#                 else ("2" if state_value == "يومي" else "3")
#             )
#             food_value = "1" if state_value == "نوبتجي" else "0"

#             if state_value == "نوبتجي":
#                 employee.rahatcounter += 1
#             elif state_value in ["8 صباحاً", "ر بديلة", "راحة"]:
#                 employee.rahatcounter -= 1

#             employee.save()

#             if not Attendance.objects.filter(employee=employee, date=today).exists():
#                 Attendance.objects.create(
#                     employee=employee,
#                     date=today,
#                     state=state_value,
#                     food=food_value == "1",
#                     in_or_out=in_or_out_value,
#                     comfort_adjustment=(
#                         1
#                         if state_value == "نوبتجي"
#                         else (
#                             0
#                             if state_value == "يومي"
#                             else (
#                                 -1
#                                 if state_value in ["راحة", "ر بديلة", "8 صباحاً"]
#                                 else 0
#                             )
#                         )
#                     ),
#                 )

#         return redirect("attendance_3w")

#     return render(request, "insertdayforall.html")


# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import Attendance
# from em_data.models import Employee
# from datetime import datetime, timedelta, date
# from dateutil.relativedelta import relativedelta


# @login_required(login_url="/")
# def one_employee(request):
#     today = date.today()
#     employees = Employee.objects.all()

#     selected_employee = request.GET.get("employee")
#     start_date_str = request.GET.get("start_date")
#     end_date_str = request.GET.get("end_date")

#     employee = None
#     start_date = today
#     end_date = (today + relativedelta(months=1)).replace(day=1) + relativedelta(
#         days=-1, months=1
#     )
#     week_days = []
#     week_days_chunked = []

#     if selected_employee:
#         try:
#             employee = Employee.objects.get(id=selected_employee)

#             operation_day_map = {
#                 "السبت": 5,
#                 "الأحد": 6,
#                 "الاثنين": 0,
#                 "الثلاثاء": 1,
#                 "الأربعاء": 2,
#                 "الخميس": 3,
#                 "الجمعة": 4,
#             }
#             default_start_date = today
#             if employee.operation in operation_day_map:
#                 target_weekday = operation_day_map[employee.operation]
#                 days_to_target = (today.weekday() - target_weekday) % 7
#                 default_start_date = today - timedelta(days=days_to_target + 35)

#             start_date = (
#                 datetime.strptime(start_date_str, "%Y-%m-%d").date()
#                 if start_date_str
#                 else default_start_date
#             )
#             end_date = (
#                 datetime.strptime(end_date_str, "%Y-%m-%d").date()
#                 if end_date_str
#                 else end_date
#             )

#             if end_date < start_date:
#                 messages.error(request, "تاريخ النهاية يجب أن يكون بعد تاريخ البداية.")
#                 return redirect(request.path)

#             week_days = [
#                 start_date + timedelta(days=i)
#                 for i in range((end_date - start_date).days + 1)
#             ]
#             week_days_chunked = [
#                 week_days[i : i + 7] for i in range(0, len(week_days), 7)
#             ]

#         except Employee.DoesNotExist:
#             messages.error(request, "الفرد المحدد غير موجود.")
#             return redirect(request.path)
#         except ValueError:
#             messages.error(request, "يرجى إدخال تواريخ صالحة.")
#             return redirect(request.path)

#     return render(
#         request,
#         "attendance/one_employee.html",
#         {
#             "employees": employees,
#             "selected_employee": selected_employee,
#             "employee": employee,
#             "week_days": week_days,
#             "week_days_chunked": week_days_chunked,
#             "start_date": start_date,
#             "end_date": end_date,
#             "today": today,
#         },
#     )


# @login_required(login_url="/")
# def get_attendance(request):
#     start_date_str = request.GET.get("start_date")
#     end_date_str = request.GET.get("end_date")
#     employee_id = request.GET.get("employee_id")

#     if not start_date_str or (employee_id and not end_date_str):
#         return JsonResponse(
#             {"success": False, "error": "Start date and employee ID are required"}
#         )

#     try:
#         start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
#         if end_date_str:
#             end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
#             week_days = [
#                 start_date + timedelta(days=i)
#                 for i in range((end_date - start_date).days + 1)
#             ]
#         else:
#             week_days = [start_date + timedelta(days=i) for i in range(32)]

#         if employee_id:
#             employees = Employee.objects.filter(id=employee_id)
#         else:
#             employees = Employee.objects.all()[:200]

#         attendance_data = {}
#         for employee in employees:
#             attendance_data[employee.id] = {}
#             for day in week_days:
#                 attendance = Attendance.objects.filter(
#                     employee=employee, date=day
#                 ).first()
#                 attendance_data[employee.id][day.strftime("%Y%m%d")] = {
#                     "state": attendance.state if attendance else "_",
#                     "comfort_adjustment": (
#                         attendance.comfort_adjustment if attendance else 0
#                     ),
#                     "food": attendance.food if attendance else False,
#                 }

#         return JsonResponse({"success": True, "attendance_data": attendance_data})
#     except ValueError:
#         return JsonResponse({"success": False, "error": "Invalid date format"})


# @login_required(login_url="/")
# def simple_get_att(request):
#     start_date_str = request.GET.get("start_date")
#     end_date_str = request.GET.get("end_date")
#     employee_id = request.GET.get("employee_id")

#     if not start_date_str or (employee_id and not end_date_str):
#         return JsonResponse(
#             {"success": False, "error": "Start date and employee ID are required"}
#         )

#     try:
#         start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
#         if end_date_str:
#             end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
#             week_days = [
#                 start_date + timedelta(days=i)
#                 for i in range((end_date - start_date).days + 0)
#             ]
#         else:
#             week_days = [start_date + timedelta(days=i) for i in range(32)]

#         if employee_id:
#             employees = Employee.objects.filter(id=employee_id)
#         else:
#             employees = Employee.objects.all()[:200]

#         attendance_data = {}
#         for employee in employees:
#             attendance_data[employee.id] = {}
#             for day in week_days:
#                 attendance = Attendance.objects.filter(
#                     employee=employee, date=day
#                 ).first()
#                 attendance_data[employee.id][day.strftime("%Y%m%d")] = {
#                     "state": attendance.state if attendance else "_",
#                     "comfort_adjustment": (
#                         attendance.comfort_adjustment if attendance else 0
#                     ),
#                     "food": attendance.food if attendance else False,
#                 }

#         return JsonResponse({"success": True, "attendance_data": attendance_data})
#     except ValueError:
#         return JsonResponse({"success": False, "error": "Invalid date format"})






# import json


# @login_required(login_url="/")
# def update_operation(request):
#     if request.method == "POST":
#         try:
#             # قراءة جسم الطلب وتحليله كـ JSON
#             data = json.loads(request.body)
#             employee_id = data.get("employee_id")
#             operation_value = data.get("operation")

#             print(
#                 f"Received: employee_id={employee_id}, operation={operation_value}, RAW_BODY={request.body.decode('utf-8')}"
#             )

#             if not employee_id or not operation_value:
#                 return JsonResponse(
#                     {"success": False, "error": "Missing employee_id or operation"}
#                 )

#             employee = Employee.objects.get(id=employee_id)
#             employee.operation = operation_value
#             employee.save()

#             print(
#                 f"Updated operation: employee={employee_id}, operation={operation_value}"
#             )
#             return JsonResponse({"success": True, "operation": employee.operation})
#         except json.JSONDecodeError:
#             return JsonResponse({"success": False, "error": "Invalid JSON data"})
#         except Employee.DoesNotExist:
#             return JsonResponse({"success": False, "error": "Employee not found"})
#         except Exception as e:
#             return JsonResponse({"success": False, "error": str(e)})
#     return JsonResponse({"success": False, "error": "Invalid request"})





# # yourapp/views.py
# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from .forms import DateForm
# from .models import Attendance
# from django.db.models import F
# from math import ceil
# from datetime import date

# # قاموس الأيام باللغة العربية
# ARABIC_DAYS = {
#     0: 'الإثنين',
#     1: 'الثلاثاء',
#     2: 'الأربعاء',
#     3: 'الخميس',
#     4: 'الجمعة',
#     5: 'السبت',
#     6: 'الأحد',
# }



# from datetime import date, timedelta 
# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from .forms import DateForm
# from .models import Attendance
# from django.db.models import F
# from math import ceil

# # قاموس الأيام باللغة العربية
# ARABIC_DAYS = {
#     0: 'الإثنين',
#     1: 'الثلاثاء',
#     2: 'الأربعاء',
#     3: 'الخميس',
#     4: 'الجمعة',
#     5: 'السبت',
#     6: 'الأحد',
# }

# @login_required
# def foodlist(request):
#     names_with_serials = []
#     selected_date = None
#     formatted_date = None

#     if request.method == 'POST':
#         form = DateForm(request.POST)
#         if form.is_valid():
#             selected_date = form.cleaned_data['date']
#             if selected_date:
#                 # Fetch 'name' from the related Employee model
#                 names = Attendance.objects.filter(
#                     date=selected_date,
#                     food=1,
#                     state__in=['نوبتجي', 'يومي', 'ت دوري', 'ت تكراري'],
#                     employee__food=1
#                 ).annotate(dep_sort=F('employee__dep_sort')) \
#                 .order_by('dep_sort') \
#                 .values_list('employee__name', flat=True)
                
#                 # إضافة الأرقام التسلسلية
#                 names_with_serials = [(index + 1, name) for index, name in enumerate(names)]
                
#                 # تنسيق التاريخ يدويًا
#                 day_name = ARABIC_DAYS[selected_date.weekday()]
#                 formatted_date = f"{day_name} {selected_date.day:02d}/{selected_date.month:02d}/{selected_date.year}"
#     else:
#         # تعيين التاريخ الافتراضي إلى غدًا
#         selected_date = date.today() + timedelta(days=1)
#         form = DateForm(initial={'date': selected_date})  # تهيئة النموذج بالتاريخ الافتراضي
#         # تنسيق التاريخ يدويًا للتاريخ الافتراضي
#         day_name = ARABIC_DAYS[selected_date.weekday()]
#         formatted_date = f"{day_name} {selected_date.day:02d}/{selected_date.month:02d}/{selected_date.year}"

#     total_rows = 39
#     num_columns = max(2, ceil(len(names_with_serials) / total_rows))
#     columns = [names_with_serials[i * total_rows: (i + 1) * total_rows] for i in range(num_columns)]

#     context = {
#         'form': form,
#         'selected_date': selected_date,
#         'formatted_date': formatted_date,
#         'columns': columns,
#         'num_rows': total_rows,
#     }
#     return render(request, 'attendance/foodlist.html', context)





# from datetime import datetime, timedelta
# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from .models import Attendance
# from math import ceil

# # قاموس الأيام باللغة العربية
# ARABIC_DAYS = {
#     0: 'الإثنين',
#     1: 'الثلاثاء',
#     2: 'الأربعاء',
#     3: 'الخميس',
#     4: 'الجمعة',
#     5: 'السبت',
#     6: 'الأحد',
# }

# from datetime import datetime, timedelta
# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from .models import Attendance
# from math import ceil

# # قاموس الأيام باللغة العربية
# ARABIC_DAYS = {
#     0: 'الإثنين',
#     1: 'الثلاثاء',
#     2: 'الأربعاء',
#     3: 'الخميس',
#     4: 'الجمعة',
#     5: 'السبت',
#     6: 'الأحد',
# }

# @login_required
# def amtmam_view(request):
#     # Get the selected date from the request (default to tomorrow)
#     default_date = datetime.now().date() + timedelta(days=1)  # Tomorrow as default
#     selected_date = request.GET.get('date', default_date.strftime('%Y-%m-%d'))

#     # Ensure selected_date is a datetime.date object
#     try:
#         selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
#     except ValueError:
#         selected_date = default_date

#     # Format the selected date in Arabic manually
#     day_name = ARABIC_DAYS[selected_date.weekday()]
#     formatted_date = f"{day_name} {selected_date.day:02d}/{selected_date.month:02d}/{selected_date.year}"

#     # Calculate the next day
#     next_day = selected_date + timedelta(days=1)

#     # Fetch records for the selected date where in_or_out is 1 or 2
#     records = Attendance.objects.filter(date=selected_date, in_or_out__in=['in', 'going']).select_related('employee__department')

#     # Fetch records for the next day where food = 1
#     tomorrow_food_count = Attendance.objects.filter(date=next_day, food=1).count()

#     # Helper function to process data for a table
#     def process_table_data(records, condition):
#         data = []
#         for record in records:
#             if condition(record):
#                 name = record.employee.nickname
#                 if record.state == 'نوبتجي':
#                     name = " ★ " + name
#                 data.append((record.employee.gender, record.employee.sort_number, name))  # Store gender, sort_number, and name
#         # Sort by gender (ذكر first, then أنثي), then by sort_number
#         data.sort(key=lambda x: (x[0] != 'ذكر', x[1]))  # 'ذكر' comes before 'أنثي', then sort by sort_number
#         return [name for (gender, sort_number, name) in data]  # Extract names after sorting

#     # Filter and process data for table1_data (department != فريق الموسيقي and tmamam = 1)
#     table1_data = process_table_data(
#         records,
#         lambda record: record.employee.tmamam == 1 and (record.employee.department is None or record.employee.department.name != 'فريق الموسيقي')
#     )

#     # Filter and process data for table2_data (department = فريق الموسيقي and tmamam = 1)
#     table2_data = process_table_data(
#         records,
#         lambda record: record.employee.tmamam == 1 and record.employee.department is not None and record.employee.department.name == 'فريق الموسيقي'
#     )

#     # Filter and process data for table3_data (tmamam = 0)
#     table3_data = process_table_data(
#         records,
#         lambda record: record.employee.tmamam == 0
#     )

#     # Add serial numbers to the data
#     table1_with_serials = [(i + 1, name) for i, name in enumerate(table1_data)]
#     table2_with_serials = [(i + 1, name) for i, name in enumerate(table2_data)]
#     table3_with_serials = [(i + 1, name) for i, name in enumerate(table3_data)]

#     # Split data into columns
#     total_rows = 39
#     table1_columns = [table1_with_serials[i * total_rows: (i + 1) * total_rows] for i in range(ceil(len(table1_with_serials) / total_rows))]
#     table2_columns = [table2_with_serials[i * total_rows: (i + 1) * total_rows] for i in range(ceil(len(table2_with_serials) / total_rows))]
#     table3_columns = [table3_with_serials[i * total_rows: (i + 1) * total_rows] for i in range(ceil(len(table3_with_serials) / total_rows))]

#     # Calculate totals
#     intamam = len(table1_data) + len(table2_data)
#     outtamam = len(table3_data)
#     alltamam = intamam + outtamam

#     context = {
#         'selected_date': selected_date,
#         'formatted_date': formatted_date,
#         'table1_columns': table1_columns,
#         'table2_columns': table2_columns,
#         'table3_columns': table3_columns,
#         'num_rows': total_rows,
#         'intamam': intamam,
#         'outtamam': outtamam,
#         'alltamam': alltamam,
#         'tomorrow_food_count': tomorrow_food_count,
#     }
#     return render(request, 'attendance/amtmam.html', context)






# from datetime import datetime, timedelta
# from django.shortcuts import render
# from django.db.models import Q
# from babel.dates import format_date as babel_format_date
# from .models import Employee, Attendance



# def get_attendance_count(gender, department_name, state, date, exclude_department=False):
#     """
#     إحصاء عدد الحضور بناءً على الجنس، القسم، الحالة، والتاريخ.
#     """
#     query = Attendance.objects.filter(
#         employee__gender=gender,
#         date=date
#     )
#     if isinstance(state, list):
#         query = query.filter(state__in=state)
#     else:
#         query = query.filter(state=state)
    
#     if exclude_department:
#         return query.exclude(employee__department__name=department_name).count()
#     else:
#         return query.filter(employee__department__name=department_name).count()

# def numreport(request):
#     # الحصول على التاريخ المحدد من الطلب (إذا لم يتم تحديد تاريخ، استخدم تاريخ غدا)
#     selected_date_str = request.GET.get('date', (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d'))
#     selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
#     formatted_date = babel_format_date(selected_date, format='EEEE dd MMMM yyyy', locale='ar')

#     # التحقق مما إذا كان اليوم المحدد هو الخميس (weekday() == 3)
#     is_thursday = selected_date.weekday() == 3
#     friday_date = selected_date + timedelta(days=1) if is_thursday else None
#     formatted_friday_date = babel_format_date(friday_date, format='EEEE dd MMMM yyyy', locale='ar') if is_thursday else None

#     # دالة مساعدة لحساب البيانات لتاريخ معين
#     def calculate_counts(date):
#         count1 = Employee.objects.filter(Q(gender='ذكر') & ~Q(department__name='فريق الموسيقي') & Q(mainornot=1)).count()
#         count2 = Employee.objects.filter(Q(gender='ذكر') & Q(department__name='فريق الموسيقي') & Q(mainornot=1)).count()
#         count3 = Employee.objects.filter(Q(gender='أنثي') & ~Q(department__name='فريق الموسيقي') & Q(mainornot=1)).count()
#         count4 = Employee.objects.filter(Q(gender='أنثي') & Q(department__name='فريق الموسيقي') & Q(mainornot=1)).count()
#         count5 = Employee.objects.filter(mainornot=1).count()

#         m_e_tarka = get_attendance_count('ذكر', 'فريق الموسيقي', 'طارئة', date, exclude_department=True)
#         m_m_tarka = get_attendance_count('ذكر', 'فريق الموسيقي', 'طارئة', date)
#         f_e_tarka = get_attendance_count('أنثي', 'فريق الموسيقي', 'طارئة', date, exclude_department=True)
#         f_m_tarka = get_attendance_count('أنثي', 'فريق الموسيقي', 'طارئة', date)
#         mf_tarka = Attendance.objects.filter(state='طارئة', date=date).count()

#         m_e_dawrya = get_attendance_count('ذكر', 'فريق الموسيقي', 'دورية', date, exclude_department=True)
#         m_m_dawrya = get_attendance_count('ذكر', 'فريق الموسيقي', 'دورية', date)
#         f_e_dawrya = get_attendance_count('أنثي', 'فريق الموسيقي', 'دورية', date, exclude_department=True)
#         f_m_dawrya = get_attendance_count('أنثي', 'فريق الموسيقي', 'دورية', date)
#         mf_dawrya = Attendance.objects.filter(state='دورية', date=date).count()

#         m_e_sick = get_attendance_count('ذكر', 'فريق الموسيقي', ['مرضي', 'قرار66'], date, exclude_department=True)
#         m_m_sick = get_attendance_count('ذكر', 'فريق الموسيقي', ['مرضي', 'قرار66'], date)
#         f_e_sick = get_attendance_count('أنثي', 'فريق الموسيقي', ['مرضي', 'قرار66'], date, exclude_department=True)
#         f_m_sick = get_attendance_count('أنثي', 'فريق الموسيقي', ['مرضي', 'قرار66'], date)
#         mf_sick = Attendance.objects.filter(Q(state='مرضي') | Q(state='قرار66'), date=date).count()

#         m_e_khas = get_attendance_count('ذكر', 'فريق الموسيقي', ['خاصه', 'ج وضع'], date, exclude_department=True)
#         m_m_khas = get_attendance_count('ذكر', 'فريق الموسيقي', ['خاصه', 'ج وضع'], date)
#         f_e_khas = get_attendance_count('أنثي', 'فريق الموسيقي', ['خاصه', 'ج وضع'], date, exclude_department=True)
#         f_m_khas = get_attendance_count('أنثي', 'فريق الموسيقي', ['خاصه', 'ج وضع'], date)
#         mf_khas = Attendance.objects.filter(Q(state='خاصه') | Q(state='ج وضع'), date=date).count()

#         m_e_mamrya = get_attendance_count('ذكر', 'فريق الموسيقي', ['مأمورية', 'مأمورية خ'], date, exclude_department=True)
#         m_m_mamrya = get_attendance_count('ذكر', 'فريق الموسيقي', ['مأمورية', 'مأمورية خ'], date)
#         f_e_mamrya = get_attendance_count('أنثي', 'فريق الموسيقي', ['مأمورية', 'مأمورية خ'], date, exclude_department=True)
#         f_m_mamrya = get_attendance_count('أنثي', 'فريق الموسيقي', ['مأمورية', 'مأمورية خ'], date)
#         mf_mamrya = Attendance.objects.filter(Q(state='مأمورية') | Q(state='مأمورية خ'), date=date).count()

#         m_e_intdab = get_attendance_count('ذكر', 'فريق الموسيقي', 'انتداب', date, exclude_department=True)
#         m_m_intdab = get_attendance_count('ذكر', 'فريق الموسيقي', 'انتداب', date)
#         f_e_intdab = get_attendance_count('أنثي', 'فريق الموسيقي', 'انتداب', date, exclude_department=True)
#         f_m_intdab = get_attendance_count('أنثي', 'فريق الموسيقي', 'انتداب', date)
#         mf_intdab = Attendance.objects.filter(state='انتداب', date=date).count()

#         m_e_ferka = get_attendance_count('ذكر', 'فريق الموسيقي', ['فرقة', 'ت دوري', 'ت تكراري'], date, exclude_department=True)
#         m_m_ferka = get_attendance_count('ذكر', 'فريق الموسيقي', ['فرقة', 'ت دوري', 'ت تكراري'], date)
#         f_e_ferka = get_attendance_count('أنثي', 'فريق الموسيقي', ['فرقة', 'ت دوري', 'ت تكراري'], date, exclude_department=True)
#         f_m_ferka = get_attendance_count('أنثي', 'فريق الموسيقي', ['فرقة', 'ت دوري', 'ت تكراري'], date)
#         mf_ferka = Attendance.objects.filter(Q(state='فرقة') | Q(state='ت دوري') | Q(state='ت تكراري'), date=date).count()

#         m_e_salam = get_attendance_count('ذكر', 'فريق الموسيقي', 'حفظ سلام', date, exclude_department=True)
#         m_m_salam = get_attendance_count('ذكر', 'فريق الموسيقي', 'حفظ سلام', date)
#         f_e_salam = get_attendance_count('أنثي', 'فريق الموسيقي', 'حفظ سلام', date, exclude_department=True)
#         f_m_salam = get_attendance_count('أنثي', 'فريق الموسيقي', 'حفظ سلام', date)
#         mf_salam = Attendance.objects.filter(state='حفظ سلام', date=date).count()

#         m_e_wafaa = get_attendance_count('ذكر', 'فريق الموسيقي', 'وفاه', date, exclude_department=True)
#         m_m_wafaa = get_attendance_count('ذكر', 'فريق الموسيقي', 'وفاه', date)
#         f_e_wafaa = get_attendance_count('أنثي', 'فريق الموسيقي', 'وفاه', date, exclude_department=True)
#         f_m_wafaa = get_attendance_count('أنثي', 'فريق الموسيقي', 'وفاه', date)
#         mf_wafaa = Attendance.objects.filter(state='وفاه', date=date).count()

#         m_e_raha = get_attendance_count('ذكر', 'فريق الموسيقي', ['منحة', 'عطلة', '8 صباحاً', 'ر بديلة', 'راحة'], date, exclude_department=True)
#         m_m_raha = get_attendance_count('ذكر', 'فريق الموسيقي', ['منحة', 'عطلة', '8 صباحاً', 'ر بديلة', 'راحة'], date)
#         f_e_raha = get_attendance_count('أنثي', 'فريق الموسيقي', ['منحة', 'عطلة', '8 صباحاً', 'ر بديلة', 'راحة'], date, exclude_department=True)
#         f_m_raha = get_attendance_count('أنثي', 'فريق الموسيقي', ['منحة', 'عطلة', '8 صباحاً', 'ر بديلة', 'راحة'], date)
#         mf_raha = Attendance.objects.filter(Q(state='منحة') | Q(state='عطلة') | Q(state='8 صباحاً') | Q(state='ر بديلة') | Q(state='راحة'), date=date).count()

#         m_e_e3ara = get_attendance_count('ذكر', 'فريق الموسيقي', 'إعارة', date, exclude_department=True)
#         m_m_e3ara = get_attendance_count('ذكر', 'فريق الموسيقي', 'إعارة', date)
#         f_e_e3ara = get_attendance_count('أنثي', 'فريق الموسيقي', 'إعارة', date, exclude_department=True)
#         f_m_e3ara = get_attendance_count('أنثي', 'فريق الموسيقي', 'إعارة', date)
#         mf_e3ara = Attendance.objects.filter(state='إعارة', date=date).count()

#         m_e_ghyab = get_attendance_count('ذكر', 'فريق الموسيقي', 'غياب', date, exclude_department=True)
#         m_m_ghyab = get_attendance_count('ذكر', 'فريق الموسيقي', 'غياب', date)
#         f_e_ghyab = get_attendance_count('أنثي', 'فريق الموسيقي', 'غياب', date, exclude_department=True)
#         f_m_ghyab = get_attendance_count('أنثي', 'فريق الموسيقي', 'غياب', date)
#         mf_ghyab = Attendance.objects.filter(state='غياب', date=date).count()

#         m_e_out = m_e_tarka + m_e_dawrya + m_e_sick + m_e_khas + m_e_mamrya + m_e_intdab + m_e_ferka + m_e_salam + m_e_wafaa + m_e_raha + m_e_e3ara + m_e_ghyab
#         m_m_out = m_m_tarka + m_m_dawrya + m_m_sick + m_m_khas + m_m_mamrya + m_m_intdab + m_m_ferka + m_m_salam + m_m_wafaa + m_m_raha + m_m_e3ara + m_m_ghyab
#         f_e_out = f_e_tarka + f_e_dawrya + f_e_sick + f_e_khas + f_e_mamrya + f_e_intdab + f_e_ferka + f_e_salam + f_e_wafaa + f_e_raha + f_e_e3ara + f_e_ghyab
#         f_m_out = f_m_tarka + f_m_dawrya + f_m_sick + f_m_khas + f_m_mamrya + f_m_intdab + f_m_ferka + f_m_salam + f_m_wafaa + f_m_raha + f_m_e3ara + f_m_ghyab
#         mf_out = mf_tarka + mf_dawrya + mf_sick + mf_khas + mf_mamrya + mf_intdab + mf_ferka + mf_salam + mf_wafaa + mf_raha + mf_e3ara + mf_ghyab

#         m_e_in = count1 - m_e_out
#         m_m_in = count2 - m_m_out
#         f_e_in = count3 - f_e_out
#         f_m_in = count4 - f_m_out
#         mf_in = count5 - mf_out

#         return {
#             'count1': count1, 'count2': count2, 'count3': count3, 'count4': count4, 'count5': count5,
#             'm_e_tarka': m_e_tarka, 'm_m_tarka': m_m_tarka, 'f_e_tarka': f_e_tarka, 'f_m_tarka': f_m_tarka, 'mf_tarka': mf_tarka,
#             'm_e_dawrya': m_e_dawrya, 'm_m_dawrya': m_m_dawrya, 'f_e_dawrya': f_e_dawrya, 'f_m_dawrya': f_m_dawrya, 'mf_dawrya': mf_dawrya,
#             'm_e_sick': m_e_sick, 'm_m_sick': m_m_sick, 'f_e_sick': f_e_sick, 'f_m_sick': f_m_sick, 'mf_sick': mf_sick,
#             'm_e_khas': m_e_khas, 'm_m_khas': m_m_khas, 'f_e_khas': f_e_khas, 'f_m_khas': f_m_khas, 'mf_khas': mf_khas,
#             'm_e_mamrya': m_e_mamrya, 'm_m_mamrya': m_m_mamrya, 'f_e_mamrya': f_e_mamrya, 'f_m_mamrya': f_m_mamrya, 'mf_mamrya': mf_mamrya,
#             'm_e_intdab': m_e_intdab, 'm_m_intdab': m_m_intdab, 'f_e_intdab': f_e_intdab, 'f_m_intdab': f_m_intdab, 'mf_intdab': mf_intdab,
#             'm_e_ferka': m_e_ferka, 'm_m_ferka': m_m_ferka, 'f_e_ferka': f_e_ferka, 'f_m_ferka': f_m_ferka, 'mf_ferka': mf_ferka,
#             'm_e_salam': m_e_salam, 'm_m_salam': m_m_salam, 'f_e_salam': f_e_salam, 'f_m_salam': f_m_salam, 'mf_salam': mf_salam,
#             'm_e_wafaa': m_e_wafaa, 'm_m_wafaa': m_m_wafaa, 'f_e_wafaa': f_e_wafaa, 'f_m_wafaa': f_m_wafaa, 'mf_wafaa': mf_wafaa,
#             'm_e_raha': m_e_raha, 'm_m_raha': m_m_raha, 'f_e_raha': f_e_raha, 'f_m_raha': f_m_raha, 'mf_raha': mf_raha,
#             'm_e_e3ara': m_e_e3ara, 'm_m_e3ara': m_m_e3ara, 'f_e_e3ara': f_e_e3ara, 'f_m_e3ara': f_m_e3ara, 'mf_e3ara': mf_e3ara,
#             'm_e_ghyab': m_e_ghyab, 'm_m_ghyab': m_m_ghyab, 'f_e_ghyab': f_e_ghyab, 'f_m_ghyab': f_m_ghyab, 'mf_ghyab': mf_ghyab,
#             'm_e_out': m_e_out, 'm_m_out': m_m_out, 'f_e_out': f_e_out, 'f_m_out': f_m_out, 'mf_out': mf_out,
#             'm_e_in': m_e_in, 'm_m_in': m_m_in, 'f_e_in': f_e_in, 'f_m_in': f_m_in, 'mf_in': mf_in,
#         }

#     # حساب بيانات يوم الخميس
#     thursday_data = calculate_counts(selected_date)

#     # إذا كان اليوم الخميس، احسب بيانات يوم الجمعة
#     friday_data = calculate_counts(friday_date) if is_thursday else None

#     # إعداد السياق
#     context = {
#         'selected_date': selected_date,
#         'formatted_date': formatted_date,
#         'is_thursday': is_thursday,
#         'friday_date': friday_date,
#         'formatted_friday_date': formatted_friday_date,
#         'thursday_data': thursday_data,
#         'friday_data': friday_data,
#     }

#     return render(request, 'attendance/numreport.html', context)





# from django.shortcuts import render
# from django.utils.formats import date_format  # Ensure this is imported
# from datetime import datetime, timedelta
# from django.db.models import Q
# from django.contrib.auth.decorators import login_required
# from .models import Attendance

# @login_required
# def bus_view(request):
#     # Set selected_date to today by default
#     selected_date = datetime.today().date()  # Default to current date
#     tomorrow = selected_date + timedelta(days=1)  # Tomorrow based on default
#     departing_today = []
#     attending_tomorrow = []

#     if request.method == 'GET' and 'date' in request.GET:
#         selected_date_input = request.GET.get('date')
#         if selected_date_input:  # Only override if a date is provided
#             try:
#                 selected_date = datetime.strptime(selected_date_input, "%Y-%m-%d").date()
#                 tomorrow = selected_date + timedelta(days=1)
#             except ValueError:
#                 selected_date = datetime.today().date()  # Fallback to today if invalid
#                 tomorrow = selected_date + timedelta(days=1)

#     # Calculate previous_date based on selected_date (whether default or user-provided)
#     previous_date = selected_date

#     # Departing today
#     departing_today = Attendance.objects.filter(
#         date=selected_date,
#         in_or_out='going',
#         employee__bus=1
#     ).values('employee__name', 'employee__sort_number').distinct().order_by('employee__sort_number')

#     # Employees who were '2' or '3' on previous_date
#     valid_previous_employees = Attendance.objects.filter(
#         date=previous_date,
#         in_or_out__in=['going', 'out']
#     ).values_list('employee_id', flat=True).distinct()

#     # Attending tomorrow
#     attending_tomorrow = Attendance.objects.filter(
#         date=tomorrow,
#         in_or_out__in=['in', 'going'],
#         employee__bus=1,
#         employee_id__in=valid_previous_employees
#     ).exclude(
#         employee__in=Attendance.objects.filter(
#             date=previous_date,
#             in_or_out='in'
#         ).values_list('employee_id', flat=True)
#     ).values('employee__name', 'employee__sort_number').distinct().order_by('employee__sort_number')

#     # Format dates
#     formatted_date = date_format(selected_date, format='dd/MM/yyyy', use_l10n=True)
#     formatted_tomorrow = date_format(tomorrow, format='dd/MM/yyyy', use_l10n=True)

#     context = {
#         'departing_today': departing_today,
#         'attending_tomorrow': attending_tomorrow,
#         'selected_date': selected_date,
#         'formatted_date': formatted_date,
#         'tomorrow': tomorrow,
#         'formatted_tomorrow': formatted_tomorrow,
#     }
#     return render(request, 'attendance/bus.html', context)






# from datetime import datetime, timedelta
# from django.shortcuts import render
# from .models import Employee, Attendance
# from django.contrib.auth.decorators import login_required

# @login_required
# def kashftmam(request):
#     selected_date = request.GET.get('date')
#     start = request.GET.get('start', 1)  # القيمة الافتراضية 1
#     end = request.GET.get('end', 47)    # القيمة الافتراضية 47
#     padding_size = request.GET.get('padding_size', 1)  # القيمة الافتراضية 1

#     attendance_data = []
#     employees = Employee.objects.select_related('department').all().order_by('dep_sort')
#     date_range = []

#     if selected_date:
#         selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
#         date_range = [selected_date + timedelta(days=i) for i in range(7)]
#         attendance_data = Attendance.objects.filter(date__in=date_range).order_by('date')

#     start = int(start) if start else 1
#     end = int(end) if end else 47
#     filtered_employees = employees[start - 1:end]
    
#     for idx, employee in enumerate(filtered_employees, start=start):
#         employee.serial_number = idx  

#     return render(request, 'attendance/kashftmam.html', {
#         'attendance_data': attendance_data,
#         'selected_date': selected_date,
#         'date_range': date_range,
#         'filtered_employees': filtered_employees,
#         'first_number': start,
#         'last_number': end,
#         'padding_size': padding_size,
#     })
    
    
# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from datetime import datetime, date, timedelta
# from babel.dates import format_date
# from .forms import DateForm, ChunkSizeForm
# from .models import Attendance

# def split_into_chunks(lst, chunk_size):
#     """Split a list into chunks of specified size."""
#     for i in range(0, len(lst), chunk_size):
#         yield lst[i:i + chunk_size]

# from django.shortcuts import render
# from .models import Attendance
# from django.db.models import Count
# from datetime import datetime

# def outs(request):
#     # Get the date from request.GET, default to today's date if not provided
#     date_str = request.GET.get('date', datetime.today().strftime('%Y-%m-%d'))
#     try:
#         selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
#     except ValueError:
#         selected_date = datetime.today().date()

#     # Get all attendance records for the selected date
#     attendance_records = Attendance.objects.filter(date=selected_date)

#     # Count occurrences of each state
#     state_counts = attendance_records.values('state').annotate(
#         count=Count('state')
#     ).order_by('state')

#     # Create a dictionary with states and their employee names
#     state_employees = {}
#     for record in attendance_records:
#         if record.state not in state_employees:
#             state_employees[record.state] = []
#         state_employees[record.state].append(record.employee.name)

#     # Prepare context for the template
#     context = {
#         'selected_date': selected_date,
#         'state_counts': state_counts,
#         'state_employees': state_employees,
#         'total_records': attendance_records.count(),
#     }

#     return render(request, 'attendance/outs.html', context)   
    
    
    
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from datetime import datetime, timedelta
# from .models import Attendance
# from em_data.models import Employee

# @login_required
# def insert_many_attendance(request):
#     employees = Employee.objects.all().order_by('sort_number')
#     if request.method == 'POST':
#         from_date = request.POST.get('from_date')
#         to_date = request.POST.get('to_date')
#         employee_ids = request.POST.getlist('employee_ids')  # Get multiple employee IDs as a list
#         state = request.POST.get('state')
#         in_or_out = 'out'  # تصحيح لتتناسب مع خيارات النموذج
#         food = False  # تصحيح لأن الحقل BooleanField

#         print(f"POST Data: {request.POST}")  # تصحيح الأخطاء: طباعة البيانات
#         print(f"From Date: {from_date}, To Date: {to_date}, Employee IDs: {employee_ids}, State: {state}")

#         if from_date and to_date and employee_ids and state:
#             try:
#                 from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
#                 to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
#             except ValueError as e:
#                 return render(request, 'attendance/insertmany.html', {
#                     'employees': employees,
#                     'error': 'تنسيق التاريخ غير صحيح'
#                 })

#             if from_date > to_date:
#                 return render(request, 'attendance/insertmany.html', {
#                     'employees': employees,
#                     'error': 'نطاق التاريخ غير صالح'
#                 })

#             # قائمة لتخزين السجلات الجديدة لـ bulk_create
#             new_attendance_records = []

#             # حلقة عبر كل موظف
#             for employee_id in employee_ids:
#                 try:
#                     employee = Employee.objects.get(id=employee_id)
#                     print(f"Found Employee: {employee.name}")  # تصحيح الأخطاء: طباعة معلومات الموظف
#                 except Employee.DoesNotExist:
#                     return render(request, 'attendance/insertmany.html', {
#                         'employees': employees,
#                         'error': f'معرف الموظف {employee_id} غير موجود'
#                     })

#                 # توليد التواريخ في النطاق
#                 current_date = from_date
#                 while current_date <= to_date:
#                     # التحقق من وجود سجل حالي
#                     existing_record = Attendance.objects.filter(
#                         employee=employee,  # استخدام الكائن بدلاً من employee_id
#                         date=current_date
#                     ).first()

#                     if existing_record:
#                         # تحديث السجل الموجود
#                         existing_record.state = state
#                         existing_record.in_or_out = in_or_out
#                         existing_record.food = food
#                         existing_record.save()
#                         print(f"Updated record for {employee.name} on {current_date}")
#                     else:
#                         # إضافة سجل جديد إلى القائمة
#                         new_attendance_records.append(
#                             Attendance(
#                                 employee=employee,  # استخدام كائن Employee
#                                 date=current_date,
#                                 state=state,
#                                 in_or_out=in_or_out,
#                                 food=food
#                             )
#                         )
#                         print(f"Queued new record for {employee.name} on {current_date}")

#                     # الانتقال إلى التاريخ التالي
#                     current_date += timedelta(days=1)

#             # إنشاء السجلات الجديدة دفعة واحدة
#             if new_attendance_records:
#                 Attendance.objects.bulk_create(new_attendance_records)
#                 print(f"Created {len(new_attendance_records)} new records")

#             print("Records processed successfully")  # تصحيح الأخطاء: طباعة النجاح
#             return redirect('insert_many_attendance')  # إعادة توجيه عند النجاح

#         else:
#             return render(request, 'attendance/insertmany.html', {
#                 'employees': employees,
#                 'error': 'يرجى ملء جميع الحقول المطلوبة'
#             })

#     return render(request, 'attendance/insertmany.html', {'employees': employees})


# from django.shortcuts import render
# from django.db.models import Count, Q, OuterRef, Subquery
# from django.db import models
# from .models import Employee, Attendance
# from datetime import datetime, timedelta
# import calendar
# @login_required
# def monthly_discount(request):
#     months = [
#         (1, "يناير"), (2, "فبراير"), (3, "مارس"), (4, "أبريل"),
#         (5, "مايو"), (6, "يونيو"), (7, "يوليو"), (8, "أغسطس"),
#         (9, "سبتمبر"), (10, "أكتوبر"), (11, "نوفمبر"), (12, "ديسمبر")
#     ]
    
#     years = range(2020, datetime.now().year + 1)
    
#     if request.method == 'POST':
#         month = int(request.POST.get('month'))
#         year = int(request.POST.get('year'))
        
#         if month == 12:
#             next_month = 1
#             next_year = year + 1
#         else:
#             next_month = month + 1
#             next_year = year
        
#         num_days_in_next_month = calendar.monthrange(next_year, next_month)[1]
        
#         attendance_subquery_d_t = Attendance.objects.filter(
#             employee=OuterRef('pk'),
#             date__year=year,
#             date__month=month,
#             state__in=['دورية', 'طارئة']
#         ).values('employee').annotate(
#             total_d_t=Count('state')
#         ).values('total_d_t')
        
#         attendance_subquery_rahat = Attendance.objects.filter(
#             employee=OuterRef('pk'),
#             date__year=year,
#             date__month=month,
#             state__in=['راحة', 'ر بديلة', '8 صباحاً', 'عطلة', 'منحة']
#         ).values('employee').annotate(
#             total_rahat=Count('state')
#         ).values('total_rahat')
        
#         attendance_subquery_food = Attendance.objects.filter(
#             employee=OuterRef('pk'),
#             date__year=year,
#             date__month=month,
#             food=True
#         ).values('employee').annotate(
#             total_food=Count('food')
#         ).values('total_food')
        
#         attendance_subquery_maradi = Attendance.objects.filter(
#             employee=OuterRef('pk'),
#             date__year=year,
#             date__month=month,
#             state='مرضي'
#         ).values('employee').annotate(
#             total_maradi=Count('state')
#         ).values('total_maradi')
        
#         employees = Employee.objects.select_related('rank').annotate(
#             total_d_t=Subquery(attendance_subquery_d_t, output_field=models.IntegerField()),
#             total_rahat=Subquery(attendance_subquery_rahat, output_field=models.IntegerField()),
#             total_food=Subquery(attendance_subquery_food, output_field=models.IntegerField()),
#             total_maradi=Subquery(attendance_subquery_maradi, output_field=models.IntegerField())
#         ).order_by('sort_number').values('name', 'nots', 'rank__name', 'dep_sort', 'total_d_t', 'total_rahat', 'total_food', 'total_maradi')

#         for employee in employees:
#             total_d_t = employee['total_d_t'] or 0
#             total_rahat = employee['total_rahat'] or 0
#             total_food = employee['total_food'] or 0
#             total_maradi = employee['total_maradi'] or 0
            
#             employee['total_discount'] = total_d_t + total_rahat + total_food + total_maradi
#             employee['total_eligible'] = num_days_in_next_month - employee['total_discount']
        
#         context = {
#             'employees': employees,
#             'month': month,
#             'year': year,
#             'months': months,
#             'years': years,
#         }
        
#         return render(request, 'attendance/monthlyDiscount.html', context)
    
#     context = {
#         'months': months,
#         'years': years,
#     }
#     return render(request, 'attendance/monthlyDiscount.html', context)


@login_required(login_url='/login/')
def names_index_view(request):
    # Get parameters with defaults
    columns = request.GET.get('columns', '5')
    font_size = request.GET.get('font_size', '10')
    row_height = request.GET.get('row_height', '20')
    orientation = request.GET.get('orientation', 'landscape')
    rows_per_column = request.GET.get('rows_per_column', '0')
    serial_width = request.GET.get('serial_width', '20')
    name_width = request.GET.get('name_width', '300')
    
    # Validation/Conversion
    try: columns = int(columns)
    except: columns = 5
        
    try: font_size = int(font_size)
    except: font_size = 10
        
    try: row_height = int(row_height)
    except: row_height = 20
    
    try: rows_per_column = int(rows_per_column)
    except: rows_per_column = 0

    try: serial_width = int(serial_width)
    except: serial_width = 20

    # name_width can be 'auto' or int
    if name_width != 'auto':
        try: name_width = int(name_width)
        except: name_width = 300
        
    employees = list(Employee.objects.filter(mainornot=1).order_by('sort_number'))
    
    # Fill last column if rows_per_column is set
    if rows_per_column > 0:
        current_count = len(employees)
        remainder = current_count % rows_per_column
        if remainder > 0:
            entries_needed = rows_per_column - remainder
            # Creates dummy entries to fill the rest of the column
            for _ in range(entries_needed):
                employees.append(None)

    context = {
        'employees': employees,
        'columns': columns,
        'font_size': font_size,
        'row_height': row_height,
        'orientation': orientation,
        'rows_per_column': rows_per_column,
        'serial_width': serial_width,
        'name_width': name_width
    }
    
    return render(request, 'attendance/names_index.html', context)






