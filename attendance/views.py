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
from datetime import datetime, timedelta, date
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required(login_url="/")
def attendance_3w(request):
    today = date.today()
    start_date = request.GET.get("start_date")
    num_days = request.GET.get("num_days", "20")

    # ضبط عدد الأيام ليكون بين 1 و 21
    try:
        num_days = int(num_days)
        num_days = max(1, min(20, num_days))
    except ValueError:
        num_days = 20

    # تحديد تاريخ البدء والنهاية
    if start_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = start_date + timedelta(days=num_days)
        except ValueError:
            messages.error(request, "الرجاء إدخال تاريخ صالح.")
            return redirect(request.path)
    else:
        days_to_saturday = (today.weekday() - 5) % 7
        start_date = today - timedelta(days=days_to_saturday + 7)
        end_date = start_date + timedelta(days=num_days)

    week_days = [
        start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)
    ]

    # جلب جميع الأقسام
    department_choices = list(Department.objects.values_list("id", "name").distinct())

    # إضافة خيار "كل الأقسام" في بداية القائمة
    department_choices.insert(0, (0, "كل الأقسام"))

    # تحديد القسم الافتراضي ليكون id = 16 إذا لم يتم تحديده في GET
    department_filter = request.GET.get("departments")
    if not department_filter:
        department_filter = "14"  # تعيين القسم الافتراضي
    elif department_filter == "0":  # إذا اختار المستخدم "كل الأقسام"
        department_filter = None

    # جلب الموظفين وتصفيتهم بناءً على القسم
    employees = Employee.objects.all()
    if department_filter:
        employees = employees.filter(department=department_filter)

    # فرز البيانات
    sort_by = request.GET.get("sort_by", "dep_sort")
    valid_sort_fields = ["sort_number", "dep_sort", "operation", "department"]
    if sort_by in valid_sort_fields:
        employees = employees.order_by(sort_by)

    # تقسيم البيانات إلى صفحات (200 موظف لكل صفحة)
    paginator = Paginator(employees, 200)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # معالجة البيانات إذا تم إرسال نموذج
    if request.method == "POST":
        for employee in page_obj.object_list:
            for day in week_days:
                state = request.POST.get(
                    f'attendance_state_{employee.id}_{day.strftime("%Y%m%d")}'
                )
                if state:
                    food = request.POST.get(
                        f'food_{employee.id}_{day.strftime("%Y%m%d")}'
                    )
                    comfort_adjustment = request.POST.get(
                        f'comfort_{employee.id}_{day.strftime("%Y%m%d")}'
                    )

                    food_value = (
                        "1" if food == "1" else ("0" if state == "نوبتجي" else "0")
                    )
                    comfort_value = (
                        int(comfort_adjustment)
                        if comfort_adjustment
                        else (1 if state == "نوبتجي" else 0)
                    )

                    attendance, created = Attendance.objects.update_or_create(
                        employee=employee,
                        date=day,
                        defaults={
                            "state": state,
                            "food": food_value == "1",
                            "comfort_adjustment": comfort_value,
                            "in_or_out": (
                                "1"
                                if state == "نوبتجي"
                                else ("2" if state == "يومي" else "3")
                            ),
                        },
                    )

                    # تحديث عداد الراحة
                    if state == "راحة" and not created and attendance.state != "راحة":
                        employee.rahatcounter -= 1
                    elif state != "راحة" and not created and attendance.state == "راحة":
                        employee.rahatcounter += 1

                    old_comfort = attendance.comfort_adjustment if not created else 0
                    if old_comfort != comfort_value:
                        if old_comfort == 1 and comfort_value != 1:
                            employee.rahatcounter -= 1
                        elif old_comfort != 1 and comfort_value == 1:
                            employee.rahatcounter += 1
                    employee.save()
        return redirect(request.path_info + "?" + request.GET.urlencode())

    return render(
        request,
        "attendance/attendance_3w.html",
        {
            "page_obj": page_obj,
            "week_days": week_days,
            "sort_by": sort_by,
            "start_date": start_date,
            "end_date": end_date,
            "today": today,
            "operation_choices": Employee.OPERATION_CHOICES,
            "department_choices": department_choices,
            "department_filter": department_filter,
            "num_days": num_days,
        },
    )




@login_required(login_url="/")
def simple_attendance(request):
    today = date.today()
    start_date = request.GET.get("start_date")
    num_days = request.GET.get("num_days", "28")

    # ضبط عدد الأيام ليكون بين 1 و 21
    try:
        num_days = int(num_days)
        num_days = max(1, min(40, num_days))
    except ValueError:
        num_days = 28

    # تحديد تاريخ البدء والنهاية
    if start_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = start_date + timedelta(days=num_days)
        except ValueError:
            messages.error(request, "الرجاء إدخال تاريخ صالح.")
            return redirect(request.path)
    else:
        days_to_saturday = (today.weekday() - 6) % 7
        start_date = today - timedelta(days=days_to_saturday + 15)
        end_date = start_date + timedelta(days=num_days)

    week_days = [
        start_date + timedelta(days=i) for i in range((end_date - start_date).days)
    ]

    # جلب جميع الأقسام
    department_choices = list(Department.objects.values_list("id", "name").distinct())

    # إضافة خيار "كل الأقسام" في بداية القائمة
    department_choices.insert(0, (0, "كل الأقسام"))

    # تحديد القسم الافتراضي ليكون id = 16 إذا لم يتم تحديده في GET
    department_filter = request.GET.get("departments")
    if not department_filter:
        department_filter = "14"  # تعيين القسم الافتراضي
    elif department_filter == "0":  # إذا اختار المستخدم "كل الأقسام"
        department_filter = None

    # جلب الموظفين وتصفيتهم بناءً على القسم
    employees = Employee.objects.all()
    if department_filter:
        employees = employees.filter(department=department_filter)

    # فرز البيانات
    sort_by = request.GET.get("sort_by", "dep_sort")
    valid_sort_fields = ["sort_number", "dep_sort", "operation", "department"]
    if sort_by in valid_sort_fields:
        employees = employees.order_by(sort_by)

    # تقسيم البيانات إلى صفحات (200 موظف لكل صفحة)
    paginator = Paginator(employees, 200)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # معالجة البيانات إذا تم إرسال نموذج
    if request.method == "POST":
        for employee in page_obj.object_list:
            for day in week_days:
                state = request.POST.get(
                    f'attendance_state_{employee.id}_{day.strftime("%Y%m%d")}'
                )
                if state:
                    food = request.POST.get(
                        f'food_{employee.id}_{day.strftime("%Y%m%d")}'
                    )
                    comfort_adjustment = request.POST.get(
                        f'comfort_{employee.id}_{day.strftime("%Y%m%d")}'
                    )

                    food_value = (
                        "1" if food == "1" else ("0" if state == "نوبتجي" else "0")
                    )
                    comfort_value = (
                        int(comfort_adjustment)
                        if comfort_adjustment
                        else (1 if state == "نوبتجي" else 0)
                    )

                    attendance, created = Attendance.objects.update_or_create(
                        employee=employee,
                        date=day,
                        defaults={
                            "state": state,
                            "food": food_value == "1",
                            "comfort_adjustment": comfort_value,
                            "in_or_out": (
                                "1"
                                if state == "نوبتجي"
                                else ("2" if state == "يومي" else "3")
                            ),
                        },
                    )

                    # تحديث عداد الراحة
                    if state == "راحة" and not created and attendance.state != "راحة":
                        employee.rahatcounter -= 1
                    elif state != "راحة" and not created and attendance.state == "راحة":
                        employee.rahatcounter += 1

                    old_comfort = attendance.comfort_adjustment if not created else 0
                    if old_comfort != comfort_value:
                        if old_comfort == 1 and comfort_value != 1:
                            employee.rahatcounter -= 1
                        elif old_comfort != 1 and comfort_value == 1:
                            employee.rahatcounter += 1
                    employee.save()
        return redirect(request.path_info + "?" + request.GET.urlencode())

    return render(
        request,
        "attendance/simple_attendance.html",
        {
            "page_obj": page_obj,
            "week_days": week_days,
            "sort_by": sort_by,
            "start_date": start_date,
            "end_date": end_date,
            "today": today,
            "operation_choices": Employee.OPERATION_CHOICES,
            "department_choices": department_choices,
            "department_filter": department_filter,
            "num_days": num_days,
        },
    )










@login_required(login_url="/")
def update_attendance(request):
    if request.method == "POST":
        response_data = {"success": True, "updates": {}}

        for key in request.POST:
            if key.startswith("changes["):
                parts = key.split("[")[1].split("]")[0]
                field = key.split("]")[1][1:]
                employee_id, date_str = parts.split("_")

                try:
                    employee = Employee.objects.get(id=employee_id)
                    date_obj = datetime.strptime(date_str, "%Y%m%d").date()

                    attendance, created = Attendance.objects.get_or_create(
                        employee=employee,
                        date=date_obj,
                        defaults={
                            "state": "_",
                            "food": False,
                            "comfort_adjustment": 0,
                            "in_or_out": "out",
                        },
                    )

                    old_comfort = attendance.comfort_adjustment
                    old_state = attendance.state

                    selected_value = request.POST.get(
                        f"changes[{parts}][selected_value]"
                    )
                    comfort_adjustment = request.POST.get(
                        f"changes[{parts}][comfort_adjustment]"
                    )
                    food = request.POST.get(f"changes[{parts}][food]")
                    source = request.POST.get(f"changes[{parts}][source]")

                    if selected_value:
                        attendance.state = selected_value

                    if source == "select":
                        if selected_value == "نوبتجي":
                            attendance.food = True
                            if old_comfort == -1:
                                employee.rahatcounter += 2
                            elif old_comfort == 0:
                                employee.rahatcounter += 1
                            attendance.comfort_adjustment = 1
                            attendance.in_or_out = "in"
                        elif selected_value == "يومي":
                            attendance.food = False
                            if old_comfort == 1:
                                employee.rahatcounter -= 1
                            elif old_comfort == -1:
                                employee.rahatcounter += 1
                            attendance.comfort_adjustment = 0
                            attendance.in_or_out = "going"
                        elif selected_value in ["راحة", "ر بديلة", "8 صباحاً"]:
                            attendance.food = False
                            if old_comfort == 0:
                                employee.rahatcounter -= 1
                            elif old_comfort == 1:
                                employee.rahatcounter -= 2
                            attendance.comfort_adjustment = -1
                            attendance.in_or_out = "out"
                        else:
                            attendance.food = False
                            if old_comfort == 1:
                                employee.rahatcounter -= 1
                            elif old_comfort == -1:
                                employee.rahatcounter += 1
                            attendance.comfort_adjustment = 0
                            attendance.in_or_out = "out"

                    if source == "checkbox":
                        if food is not None:
                            attendance.food = food == "1"
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

                    response_data["updates"][parts] = {
                        "rahatcounter": employee.rahatcounter,
                        "state": attendance.state,
                        "food": attendance.food,
                        "comfort_adjustment": attendance.comfort_adjustment,
                    }

                except Employee.DoesNotExist:
                    response_data["success"] = False
                    response_data["error"] = f"Employee {employee_id} not found"
                    break
                except Exception as e:
                    response_data["success"] = False
                    response_data["error"] = str(e)
                    break

        return JsonResponse(response_data)
    return JsonResponse({"success": False, "error": "Invalid request"})


logger = logging.getLogger(__name__)


@login_required(login_url="/")
def reset_rahatcounter(request):
    if request.method == "POST":
        try:
            logger.info(f"Received request body: {request.body}")
            data = json.loads(request.body)
            employee_id = data.get("employee_id")

            if not employee_id:
                logger.error("No employee_id provided in request")
                return JsonResponse(
                    {"success": False, "error": "Employee ID is required"}
                )

            try:
                employee_id = int(employee_id)
            except ValueError:
                logger.error(f"Invalid employee_id format: {employee_id}")
                return JsonResponse(
                    {"success": False, "error": "Invalid employee ID format"}
                )

            logger.info(
                f"Attempting to reset rahatcounter for employee_id: {employee_id}"
            )
            employee = Employee.objects.get(id=employee_id)
            employee.rahatcounter = 0
            employee.save()

            logger.info(
                f"Successfully reset rahatcounter for employee_id: {employee_id}"
            )
            return JsonResponse({"success": True})
        except Employee.DoesNotExist:
            logger.error(f"Employee not found: {employee_id}")
            return JsonResponse({"success": False, "error": "Employee not found"})
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            return JsonResponse({"success": False, "error": "Invalid JSON data"})
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return JsonResponse(
                {"success": False, "error": f"Internal server error: {str(e)}"}
            )
    logger.warning("Invalid request method")
    return JsonResponse({"success": False, "error": "Invalid request"})


@login_required(login_url="/login/")
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
            in_or_out_value = "3"
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
            elif operation == "عمل يومي":
                if day_of_week in [0, 1, 2, 3, 5, 6]:
                    state_value = "يومي"
                elif day_of_week == 4:
                    state_value = "راحة"

            in_or_out_value = (
                "1"
                if state_value == "نوبتجي"
                else ("2" if state_value == "يومي" else "3")
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

    return render(request, "insertdayforall.html")


# @login_required(login_url="/")
# def get_attendance_data(request):
#     start_date_str = request.GET.get("start_date")
#     page = request.GET.get("page", "1")
#     num_days = request.GET.get("num_days", "15")

#     if not start_date_str:
#         return JsonResponse({"success": False, "error": "Start date is required"})

#     try:
#         start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
#         num_days = int(num_days)
#         num_days = max(1, min(21, num_days))
#         week_days = [start_date + timedelta(days=i) for i in range(num_days)]

#         employees = Employee.objects.all()
#         paginator = Paginator(employees, 50)  # تقليل إلى 50 موظفًا لكل صفحة
#         page_obj = paginator.get_page(page)

#         attendance_data = {}
#         for employee in page_obj:
#             attendance_records = Attendance.objects.filter(
#                 employee=employee, date__range=(start_date, week_days[-1])
#             ).values("date", "state", "comfort_adjustment", "food")

#             attendance_dict = {
#                 rec["date"].strftime("%Y%m%d"): {
#                     "state": rec["state"],
#                     "comfort_adjustment": rec["comfort_adjustment"],
#                     "food": rec["food"],
#                 }
#                 for rec in attendance_records
#             }

#             attendance_data[employee.id] = {}
#             for day in week_days:
#                 date_str = day.strftime("%Y%m%d")
#                 attendance_data[employee.id][date_str] = attendance_dict.get(
#                     date_str, {"state": "_", "comfort_adjustment": 0, "food": False}
#                 )

#         return JsonResponse({"success": True, "attendance_data": attendance_data})
#     except ValueError:
#         return JsonResponse({"success": False, "error": "Invalid date format"})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Attendance
from em_data.models import Employee
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta


@login_required(login_url="/")
def one_employee(request):
    today = date.today()
    employees = Employee.objects.all()

    selected_employee = request.GET.get("employee")
    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")

    employee = None
    start_date = today
    end_date = (today + relativedelta(months=1)).replace(day=1) + relativedelta(
        days=-1, months=1
    )
    week_days = []
    week_days_chunked = []

    if selected_employee:
        try:
            employee = Employee.objects.get(id=selected_employee)

            operation_day_map = {
                "السبت": 5,
                "الأحد": 6,
                "الاثنين": 0,
                "الثلاثاء": 1,
                "الأربعاء": 2,
                "الخميس": 3,
                "الجمعة": 4,
            }
            default_start_date = today
            if employee.operation in operation_day_map:
                target_weekday = operation_day_map[employee.operation]
                days_to_target = (today.weekday() - target_weekday) % 7
                default_start_date = today - timedelta(days=days_to_target + 35)

            start_date = (
                datetime.strptime(start_date_str, "%Y-%m-%d").date()
                if start_date_str
                else default_start_date
            )
            end_date = (
                datetime.strptime(end_date_str, "%Y-%m-%d").date()
                if end_date_str
                else end_date
            )

            if end_date < start_date:
                messages.error(request, "تاريخ النهاية يجب أن يكون بعد تاريخ البداية.")
                return redirect(request.path)

            week_days = [
                start_date + timedelta(days=i)
                for i in range((end_date - start_date).days + 1)
            ]
            week_days_chunked = [
                week_days[i : i + 7] for i in range(0, len(week_days), 7)
            ]

        except Employee.DoesNotExist:
            messages.error(request, "الفرد المحدد غير موجود.")
            return redirect(request.path)
        except ValueError:
            messages.error(request, "يرجى إدخال تواريخ صالحة.")
            return redirect(request.path)

    return render(
        request,
        "attendance/one_employee.html",
        {
            "employees": employees,
            "selected_employee": selected_employee,
            "employee": employee,
            "week_days": week_days,
            "week_days_chunked": week_days_chunked,
            "start_date": start_date,
            "end_date": end_date,
            "today": today,
        },
    )


@login_required(login_url="/")
def get_attendance(request):
    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")
    employee_id = request.GET.get("employee_id")

    if not start_date_str or (employee_id and not end_date_str):
        return JsonResponse(
            {"success": False, "error": "Start date and employee ID are required"}
        )

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            week_days = [
                start_date + timedelta(days=i)
                for i in range((end_date - start_date).days + 1)
            ]
        else:
            week_days = [start_date + timedelta(days=i) for i in range(32)]

        if employee_id:
            employees = Employee.objects.filter(id=employee_id)
        else:
            employees = Employee.objects.all()[:200]

        attendance_data = {}
        for employee in employees:
            attendance_data[employee.id] = {}
            for day in week_days:
                attendance = Attendance.objects.filter(
                    employee=employee, date=day
                ).first()
                attendance_data[employee.id][day.strftime("%Y%m%d")] = {
                    "state": attendance.state if attendance else "_",
                    "comfort_adjustment": (
                        attendance.comfort_adjustment if attendance else 0
                    ),
                    "food": attendance.food if attendance else False,
                }

        return JsonResponse({"success": True, "attendance_data": attendance_data})
    except ValueError:
        return JsonResponse({"success": False, "error": "Invalid date format"})


@login_required(login_url="/")
def simple_get_att(request):
    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")
    employee_id = request.GET.get("employee_id")

    if not start_date_str or (employee_id and not end_date_str):
        return JsonResponse(
            {"success": False, "error": "Start date and employee ID are required"}
        )

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            week_days = [
                start_date + timedelta(days=i)
                for i in range((end_date - start_date).days + 0)
            ]
        else:
            week_days = [start_date + timedelta(days=i) for i in range(32)]

        if employee_id:
            employees = Employee.objects.filter(id=employee_id)
        else:
            employees = Employee.objects.all()[:200]

        attendance_data = {}
        for employee in employees:
            attendance_data[employee.id] = {}
            for day in week_days:
                attendance = Attendance.objects.filter(
                    employee=employee, date=day
                ).first()
                attendance_data[employee.id][day.strftime("%Y%m%d")] = {
                    "state": attendance.state if attendance else "_",
                    "comfort_adjustment": (
                        attendance.comfort_adjustment if attendance else 0
                    ),
                    "food": attendance.food if attendance else False,
                }

        return JsonResponse({"success": True, "attendance_data": attendance_data})
    except ValueError:
        return JsonResponse({"success": False, "error": "Invalid date format"})






import json


@login_required(login_url="/")
def update_operation(request):
    if request.method == "POST":
        try:
            # قراءة جسم الطلب وتحليله كـ JSON
            data = json.loads(request.body)
            employee_id = data.get("employee_id")
            operation_value = data.get("operation")

            print(
                f"Received: employee_id={employee_id}, operation={operation_value}, RAW_BODY={request.body.decode('utf-8')}"
            )

            if not employee_id or not operation_value:
                return JsonResponse(
                    {"success": False, "error": "Missing employee_id or operation"}
                )

            employee = Employee.objects.get(id=employee_id)
            employee.operation = operation_value
            employee.save()

            print(
                f"Updated operation: employee={employee_id}, operation={operation_value}"
            )
            return JsonResponse({"success": True, "operation": employee.operation})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON data"})
        except Employee.DoesNotExist:
            return JsonResponse({"success": False, "error": "Employee not found"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    return JsonResponse({"success": False, "error": "Invalid request"})





# yourapp/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import DateForm
from .models import Attendance
from django.db.models import F
from math import ceil
from datetime import date

# قاموس الأيام باللغة العربية
ARABIC_DAYS = {
    0: 'الإثنين',
    1: 'الثلاثاء',
    2: 'الأربعاء',
    3: 'الخميس',
    4: 'الجمعة',
    5: 'السبت',
    6: 'الأحد',
}



from datetime import date, timedelta 
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import DateForm
from .models import Attendance
from django.db.models import F
from math import ceil

# قاموس الأيام باللغة العربية
ARABIC_DAYS = {
    0: 'الإثنين',
    1: 'الثلاثاء',
    2: 'الأربعاء',
    3: 'الخميس',
    4: 'الجمعة',
    5: 'السبت',
    6: 'الأحد',
}

@login_required(login_url='/login/')
def foodlist(request):
    names_with_serials = []
    selected_date = None
    formatted_date = None

    if request.method == 'POST':
        form = DateForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['date']
            if selected_date:
                # Fetch 'name' from the related Employee model
                names = Attendance.objects.filter(
                    date=selected_date,
                    food=1,
                    state__in=['نوبتجي', 'يومي'],
                    employee__food=1
                ).annotate(dep_sort=F('employee__dep_sort')) \
                .order_by('dep_sort') \
                .values_list('employee__name', flat=True)
                
                # إضافة الأرقام التسلسلية
                names_with_serials = [(index + 1, name) for index, name in enumerate(names)]
                
                # تنسيق التاريخ يدويًا
                day_name = ARABIC_DAYS[selected_date.weekday()]
                formatted_date = f"{day_name} {selected_date.day:02d}/{selected_date.month:02d}/{selected_date.year}"
    else:
        # تعيين التاريخ الافتراضي إلى غدًا
        selected_date = date.today() + timedelta(days=1)
        form = DateForm(initial={'date': selected_date})  # تهيئة النموذج بالتاريخ الافتراضي
        # تنسيق التاريخ يدويًا للتاريخ الافتراضي
        day_name = ARABIC_DAYS[selected_date.weekday()]
        formatted_date = f"{day_name} {selected_date.day:02d}/{selected_date.month:02d}/{selected_date.year}"

    total_rows = 39
    num_columns = max(2, ceil(len(names_with_serials) / total_rows))
    columns = [names_with_serials[i * total_rows: (i + 1) * total_rows] for i in range(num_columns)]

    context = {
        'form': form,
        'selected_date': selected_date,
        'formatted_date': formatted_date,
        'columns': columns,
        'num_rows': total_rows,
    }
    return render(request, 'attendance/foodlist.html', context)





from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Attendance
from math import ceil

# قاموس الأيام باللغة العربية
ARABIC_DAYS = {
    0: 'الإثنين',
    1: 'الثلاثاء',
    2: 'الأربعاء',
    3: 'الخميس',
    4: 'الجمعة',
    5: 'السبت',
    6: 'الأحد',
}

from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Attendance
from math import ceil

# قاموس الأيام باللغة العربية
ARABIC_DAYS = {
    0: 'الإثنين',
    1: 'الثلاثاء',
    2: 'الأربعاء',
    3: 'الخميس',
    4: 'الجمعة',
    5: 'السبت',
    6: 'الأحد',
}

@login_required(login_url='/login/')
def amtmam_view(request):
    # Get the selected date from the request (default to tomorrow)
    default_date = datetime.now().date() + timedelta(days=1)  # Tomorrow as default
    selected_date = request.GET.get('date', default_date.strftime('%Y-%m-%d'))

    # Ensure selected_date is a datetime.date object
    try:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        selected_date = default_date

    # Format the selected date in Arabic manually
    day_name = ARABIC_DAYS[selected_date.weekday()]
    formatted_date = f"{day_name} {selected_date.day:02d}/{selected_date.month:02d}/{selected_date.year}"

    # Calculate the next day
    next_day = selected_date + timedelta(days=1)

    # Fetch records for the selected date where in_or_out is 1 or 2
    records = Attendance.objects.filter(date=selected_date, in_or_out__in=[1, 2]).select_related('employee__department')

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
                data.append((record.employee.gender, record.employee.sort_number, name))  # Store gender, sort_number, and name
        # Sort by gender (ذكر first, then أنثي), then by sort_number
        data.sort(key=lambda x: (x[0] != 'ذكر', x[1]))  # 'ذكر' comes before 'أنثي', then sort by sort_number
        return [name for (gender, sort_number, name) in data]  # Extract names after sorting

    # Filter and process data for table1_data (department != فريق الموسيقي and tmamam = 1)
    table1_data = process_table_data(
        records,
        lambda record: record.employee.tmamam == 1 and (record.employee.department is None or record.employee.department.name != 'فريق الموسيقي')
    )

    # Filter and process data for table2_data (department = فريق الموسيقي and tmamam = 1)
    table2_data = process_table_data(
        records,
        lambda record: record.employee.tmamam == 1 and record.employee.department is not None and record.employee.department.name == 'فريق الموسيقي'
    )

    # Filter and process data for table3_data (tmamam = 0)
    table3_data = process_table_data(
        records,
        lambda record: record.employee.tmamam == 0
    )

    # Add serial numbers to the data
    table1_with_serials = [(i + 1, name) for i, name in enumerate(table1_data)]
    table2_with_serials = [(i + 1, name) for i, name in enumerate(table2_data)]
    table3_with_serials = [(i + 1, name) for i, name in enumerate(table3_data)]

    # Split data into columns
    total_rows = 39
    table1_columns = [table1_with_serials[i * total_rows: (i + 1) * total_rows] for i in range(ceil(len(table1_with_serials) / total_rows))]
    table2_columns = [table2_with_serials[i * total_rows: (i + 1) * total_rows] for i in range(ceil(len(table2_with_serials) / total_rows))]
    table3_columns = [table3_with_serials[i * total_rows: (i + 1) * total_rows] for i in range(ceil(len(table3_with_serials) / total_rows))]

    # Calculate totals
    intamam = len(table1_data) + len(table2_data)
    outtamam = len(table3_data)
    alltamam = intamam + outtamam

    context = {
        'selected_date': selected_date,
        'formatted_date': formatted_date,
        'table1_columns': table1_columns,
        'table2_columns': table2_columns,
        'table3_columns': table3_columns,
        'num_rows': total_rows,
        'intamam': intamam,
        'outtamam': outtamam,
        'alltamam': alltamam,
        'tomorrow_food_count': tomorrow_food_count,
    }
    return render(request, 'attendance/amtmam.html', context)






from datetime import datetime, timedelta
from django.shortcuts import render
from django.db.models import Q
from babel.dates import format_date as babel_format_date
from .models import Employee, Attendance



def get_attendance_count(gender, department_name, state, date, exclude_department=False):
    """
    إحصاء عدد الحضور بناءً على الجنس، القسم، الحالة، والتاريخ.
    """
    query = Attendance.objects.filter(
        employee__gender=gender,
        date=date
    )
    if isinstance(state, list):
        query = query.filter(state__in=state)
    else:
        query = query.filter(state=state)
    
    if exclude_department:
        return query.exclude(employee__department__name=department_name).count()
    else:
        return query.filter(employee__department__name=department_name).count()

def numreport(request):
    # الحصول على التاريخ المحدد من الطلب (إذا لم يتم تحديد تاريخ، استخدم تاريخ غدا)
    selected_date_str = request.GET.get('date', (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
    formatted_date = babel_format_date(selected_date, format='EEEE dd MMMM yyyy', locale='ar')

    # التحقق مما إذا كان اليوم المحدد هو الخميس (weekday() == 3)
    is_thursday = selected_date.weekday() == 3
    friday_date = selected_date + timedelta(days=1) if is_thursday else None
    formatted_friday_date = babel_format_date(friday_date, format='EEEE dd MMMM yyyy', locale='ar') if is_thursday else None

    # دالة مساعدة لحساب البيانات لتاريخ معين
    def calculate_counts(date):
        count1 = Employee.objects.filter(Q(gender='ذكر') & ~Q(department__name='فريق الموسيقي') & Q(mainornot=1)).count()
        count2 = Employee.objects.filter(Q(gender='ذكر') & Q(department__name='فريق الموسيقي') & Q(mainornot=1)).count()
        count3 = Employee.objects.filter(Q(gender='أنثي') & ~Q(department__name='فريق الموسيقي') & Q(mainornot=1)).count()
        count4 = Employee.objects.filter(Q(gender='أنثي') & Q(department__name='فريق الموسيقي') & Q(mainornot=1)).count()
        count5 = Employee.objects.filter(mainornot=1).count()

        m_e_tarka = get_attendance_count('ذكر', 'فريق الموسيقي', 'طارئة', date, exclude_department=True)
        m_m_tarka = get_attendance_count('ذكر', 'فريق الموسيقي', 'طارئة', date)
        f_e_tarka = get_attendance_count('أنثي', 'فريق الموسيقي', 'طارئة', date, exclude_department=True)
        f_m_tarka = get_attendance_count('أنثي', 'فريق الموسيقي', 'طارئة', date)
        mf_tarka = Attendance.objects.filter(state='طارئة', date=date).count()

        m_e_dawrya = get_attendance_count('ذكر', 'فريق الموسيقي', 'دورية', date, exclude_department=True)
        m_m_dawrya = get_attendance_count('ذكر', 'فريق الموسيقي', 'دورية', date)
        f_e_dawrya = get_attendance_count('أنثي', 'فريق الموسيقي', 'دورية', date, exclude_department=True)
        f_m_dawrya = get_attendance_count('أنثي', 'فريق الموسيقي', 'دورية', date)
        mf_dawrya = Attendance.objects.filter(state='دورية', date=date).count()

        m_e_sick = get_attendance_count('ذكر', 'فريق الموسيقي', ['مرضي', 'قرار66'], date, exclude_department=True)
        m_m_sick = get_attendance_count('ذكر', 'فريق الموسيقي', ['مرضي', 'قرار66'], date)
        f_e_sick = get_attendance_count('أنثي', 'فريق الموسيقي', ['مرضي', 'قرار66'], date, exclude_department=True)
        f_m_sick = get_attendance_count('أنثي', 'فريق الموسيقي', ['مرضي', 'قرار66'], date)
        mf_sick = Attendance.objects.filter(Q(state='مرضي') | Q(state='قرار66'), date=date).count()

        m_e_khas = get_attendance_count('ذكر', 'فريق الموسيقي', ['خاصه', 'ج وضع'], date, exclude_department=True)
        m_m_khas = get_attendance_count('ذكر', 'فريق الموسيقي', ['خاصه', 'ج وضع'], date)
        f_e_khas = get_attendance_count('أنثي', 'فريق الموسيقي', ['خاصه', 'ج وضع'], date, exclude_department=True)
        f_m_khas = get_attendance_count('أنثي', 'فريق الموسيقي', ['خاصه', 'ج وضع'], date)
        mf_khas = Attendance.objects.filter(Q(state='خاصه') | Q(state='ج وضع'), date=date).count()

        m_e_mamrya = get_attendance_count('ذكر', 'فريق الموسيقي', ['مأمورية', 'مأمورية خ'], date, exclude_department=True)
        m_m_mamrya = get_attendance_count('ذكر', 'فريق الموسيقي', ['مأمورية', 'مأمورية خ'], date)
        f_e_mamrya = get_attendance_count('أنثي', 'فريق الموسيقي', ['مأمورية', 'مأمورية خ'], date, exclude_department=True)
        f_m_mamrya = get_attendance_count('أنثي', 'فريق الموسيقي', ['مأمورية', 'مأمورية خ'], date)
        mf_mamrya = Attendance.objects.filter(Q(state='مأمورية') | Q(state='مأمورية خ'), date=date).count()

        m_e_intdab = get_attendance_count('ذكر', 'فريق الموسيقي', 'انتداب', date, exclude_department=True)
        m_m_intdab = get_attendance_count('ذكر', 'فريق الموسيقي', 'انتداب', date)
        f_e_intdab = get_attendance_count('أنثي', 'فريق الموسيقي', 'انتداب', date, exclude_department=True)
        f_m_intdab = get_attendance_count('أنثي', 'فريق الموسيقي', 'انتداب', date)
        mf_intdab = Attendance.objects.filter(state='انتداب', date=date).count()

        m_e_ferka = get_attendance_count('ذكر', 'فريق الموسيقي', ['فرقة', 'ت دوري', 'ت تكراري'], date, exclude_department=True)
        m_m_ferka = get_attendance_count('ذكر', 'فريق الموسيقي', ['فرقة', 'ت دوري', 'ت تكراري'], date)
        f_e_ferka = get_attendance_count('أنثي', 'فريق الموسيقي', ['فرقة', 'ت دوري', 'ت تكراري'], date, exclude_department=True)
        f_m_ferka = get_attendance_count('أنثي', 'فريق الموسيقي', ['فرقة', 'ت دوري', 'ت تكراري'], date)
        mf_ferka = Attendance.objects.filter(Q(state='فرقة') | Q(state='ت دوري') | Q(state='ت تكراري'), date=date).count()

        m_e_salam = get_attendance_count('ذكر', 'فريق الموسيقي', 'حفظ سلام', date, exclude_department=True)
        m_m_salam = get_attendance_count('ذكر', 'فريق الموسيقي', 'حفظ سلام', date)
        f_e_salam = get_attendance_count('أنثي', 'فريق الموسيقي', 'حفظ سلام', date, exclude_department=True)
        f_m_salam = get_attendance_count('أنثي', 'فريق الموسيقي', 'حفظ سلام', date)
        mf_salam = Attendance.objects.filter(state='حفظ سلام', date=date).count()

        m_e_wafaa = get_attendance_count('ذكر', 'فريق الموسيقي', 'وفاه', date, exclude_department=True)
        m_m_wafaa = get_attendance_count('ذكر', 'فريق الموسيقي', 'وفاه', date)
        f_e_wafaa = get_attendance_count('أنثي', 'فريق الموسيقي', 'وفاه', date, exclude_department=True)
        f_m_wafaa = get_attendance_count('أنثي', 'فريق الموسيقي', 'وفاه', date)
        mf_wafaa = Attendance.objects.filter(state='وفاه', date=date).count()

        m_e_raha = get_attendance_count('ذكر', 'فريق الموسيقي', ['منحة', 'عطلة', '8 صباحاً', 'ر بديلة', 'راحة'], date, exclude_department=True)
        m_m_raha = get_attendance_count('ذكر', 'فريق الموسيقي', ['منحة', 'عطلة', '8 صباحاً', 'ر بديلة', 'راحة'], date)
        f_e_raha = get_attendance_count('أنثي', 'فريق الموسيقي', ['منحة', 'عطلة', '8 صباحاً', 'ر بديلة', 'راحة'], date, exclude_department=True)
        f_m_raha = get_attendance_count('أنثي', 'فريق الموسيقي', ['منحة', 'عطلة', '8 صباحاً', 'ر بديلة', 'راحة'], date)
        mf_raha = Attendance.objects.filter(Q(state='منحة') | Q(state='عطلة') | Q(state='8 صباحاً') | Q(state='ر بديلة') | Q(state='راحة'), date=date).count()

        m_e_e3ara = get_attendance_count('ذكر', 'فريق الموسيقي', 'إعارة', date, exclude_department=True)
        m_m_e3ara = get_attendance_count('ذكر', 'فريق الموسيقي', 'إعارة', date)
        f_e_e3ara = get_attendance_count('أنثي', 'فريق الموسيقي', 'إعارة', date, exclude_department=True)
        f_m_e3ara = get_attendance_count('أنثي', 'فريق الموسيقي', 'إعارة', date)
        mf_e3ara = Attendance.objects.filter(state='إعارة', date=date).count()

        m_e_ghyab = get_attendance_count('ذكر', 'فريق الموسيقي', 'غياب', date, exclude_department=True)
        m_m_ghyab = get_attendance_count('ذكر', 'فريق الموسيقي', 'غياب', date)
        f_e_ghyab = get_attendance_count('أنثي', 'فريق الموسيقي', 'غياب', date, exclude_department=True)
        f_m_ghyab = get_attendance_count('أنثي', 'فريق الموسيقي', 'غياب', date)
        mf_ghyab = Attendance.objects.filter(state='غياب', date=date).count()

        m_e_out = m_e_tarka + m_e_dawrya + m_e_sick + m_e_khas + m_e_mamrya + m_e_intdab + m_e_ferka + m_e_salam + m_e_wafaa + m_e_raha + m_e_e3ara + m_e_ghyab
        m_m_out = m_m_tarka + m_m_dawrya + m_m_sick + m_m_khas + m_m_mamrya + m_m_intdab + m_m_ferka + m_m_salam + m_m_wafaa + m_m_raha + m_m_e3ara + m_m_ghyab
        f_e_out = f_e_tarka + f_e_dawrya + f_e_sick + f_e_khas + f_e_mamrya + f_e_intdab + f_e_ferka + f_e_salam + f_e_wafaa + f_e_raha + f_e_e3ara + f_e_ghyab
        f_m_out = f_m_tarka + f_m_dawrya + f_m_sick + f_m_khas + f_m_mamrya + f_m_intdab + f_m_ferka + f_m_salam + f_m_wafaa + f_m_raha + f_m_e3ara + f_m_ghyab
        mf_out = mf_tarka + mf_dawrya + mf_sick + mf_khas + mf_mamrya + mf_intdab + mf_ferka + mf_salam + mf_wafaa + mf_raha + mf_e3ara + mf_ghyab

        m_e_in = count1 - m_e_out
        m_m_in = count2 - m_m_out
        f_e_in = count3 - f_e_out
        f_m_in = count4 - f_m_out
        mf_in = count5 - mf_out

        return {
            'count1': count1, 'count2': count2, 'count3': count3, 'count4': count4, 'count5': count5,
            'm_e_tarka': m_e_tarka, 'm_m_tarka': m_m_tarka, 'f_e_tarka': f_e_tarka, 'f_m_tarka': f_m_tarka, 'mf_tarka': mf_tarka,
            'm_e_dawrya': m_e_dawrya, 'm_m_dawrya': m_m_dawrya, 'f_e_dawrya': f_e_dawrya, 'f_m_dawrya': f_m_dawrya, 'mf_dawrya': mf_dawrya,
            'm_e_sick': m_e_sick, 'm_m_sick': m_m_sick, 'f_e_sick': f_e_sick, 'f_m_sick': f_m_sick, 'mf_sick': mf_sick,
            'm_e_khas': m_e_khas, 'm_m_khas': m_m_khas, 'f_e_khas': f_e_khas, 'f_m_khas': f_m_khas, 'mf_khas': mf_khas,
            'm_e_mamrya': m_e_mamrya, 'm_m_mamrya': m_m_mamrya, 'f_e_mamrya': f_e_mamrya, 'f_m_mamrya': f_m_mamrya, 'mf_mamrya': mf_mamrya,
            'm_e_intdab': m_e_intdab, 'm_m_intdab': m_m_intdab, 'f_e_intdab': f_e_intdab, 'f_m_intdab': f_m_intdab, 'mf_intdab': mf_intdab,
            'm_e_ferka': m_e_ferka, 'm_m_ferka': m_m_ferka, 'f_e_ferka': f_e_ferka, 'f_m_ferka': f_m_ferka, 'mf_ferka': mf_ferka,
            'm_e_salam': m_e_salam, 'm_m_salam': m_m_salam, 'f_e_salam': f_e_salam, 'f_m_salam': f_m_salam, 'mf_salam': mf_salam,
            'm_e_wafaa': m_e_wafaa, 'm_m_wafaa': m_m_wafaa, 'f_e_wafaa': f_e_wafaa, 'f_m_wafaa': f_m_wafaa, 'mf_wafaa': mf_wafaa,
            'm_e_raha': m_e_raha, 'm_m_raha': m_m_raha, 'f_e_raha': f_e_raha, 'f_m_raha': f_m_raha, 'mf_raha': mf_raha,
            'm_e_e3ara': m_e_e3ara, 'm_m_e3ara': m_m_e3ara, 'f_e_e3ara': f_e_e3ara, 'f_m_e3ara': f_m_e3ara, 'mf_e3ara': mf_e3ara,
            'm_e_ghyab': m_e_ghyab, 'm_m_ghyab': m_m_ghyab, 'f_e_ghyab': f_e_ghyab, 'f_m_ghyab': f_m_ghyab, 'mf_ghyab': mf_ghyab,
            'm_e_out': m_e_out, 'm_m_out': m_m_out, 'f_e_out': f_e_out, 'f_m_out': f_m_out, 'mf_out': mf_out,
            'm_e_in': m_e_in, 'm_m_in': m_m_in, 'f_e_in': f_e_in, 'f_m_in': f_m_in, 'mf_in': mf_in,
        }

    # حساب بيانات يوم الخميس
    thursday_data = calculate_counts(selected_date)

    # إذا كان اليوم الخميس، احسب بيانات يوم الجمعة
    friday_data = calculate_counts(friday_date) if is_thursday else None

    # إعداد السياق
    context = {
        'selected_date': selected_date,
        'formatted_date': formatted_date,
        'is_thursday': is_thursday,
        'friday_date': friday_date,
        'formatted_friday_date': formatted_friday_date,
        'thursday_data': thursday_data,
        'friday_data': friday_data,
    }

    return render(request, 'attendance/numreport.html', context)





from django.shortcuts import render
from django.utils.formats import date_format  # Ensure this is imported
from datetime import datetime, timedelta
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Attendance

@login_required(login_url='/login/')
def bus_view(request):
    # Set selected_date to today by default
    selected_date = datetime.today().date()  # Default to current date
    tomorrow = selected_date + timedelta(days=1)  # Tomorrow based on default
    departing_today = []
    attending_tomorrow = []

    if request.method == 'GET' and 'date' in request.GET:
        selected_date_input = request.GET.get('date')
        if selected_date_input:  # Only override if a date is provided
            try:
                selected_date = datetime.strptime(selected_date_input, "%Y-%m-%d").date()
                tomorrow = selected_date + timedelta(days=1)
            except ValueError:
                selected_date = datetime.today().date()  # Fallback to today if invalid
                tomorrow = selected_date + timedelta(days=1)

    # Calculate previous_date based on selected_date (whether default or user-provided)
    previous_date = selected_date

    # Departing today
    departing_today = Attendance.objects.filter(
        date=selected_date,
        in_or_out='2',
        employee__bus=1
    ).values('employee__name', 'employee__sort_number').distinct().order_by('employee__sort_number')

    # Employees who were '2' or '3' on previous_date
    valid_previous_employees = Attendance.objects.filter(
        date=previous_date,
        in_or_out__in=['2', '3']
    ).values_list('employee_id', flat=True).distinct()

    # Attending tomorrow
    attending_tomorrow = Attendance.objects.filter(
        date=tomorrow,
        in_or_out__in=['1', '2'],
        employee__bus=1,
        employee_id__in=valid_previous_employees
    ).exclude(
        employee__in=Attendance.objects.filter(
            date=previous_date,
            in_or_out='1'
        ).values_list('employee_id', flat=True)
    ).values('employee__name', 'employee__sort_number').distinct().order_by('employee__sort_number')

    # Format dates
    formatted_date = date_format(selected_date, format='dd/MM/yyyy', use_l10n=True)
    formatted_tomorrow = date_format(tomorrow, format='dd/MM/yyyy', use_l10n=True)

    context = {
        'departing_today': departing_today,
        'attending_tomorrow': attending_tomorrow,
        'selected_date': selected_date,
        'formatted_date': formatted_date,
        'tomorrow': tomorrow,
        'formatted_tomorrow': formatted_tomorrow,
    }
    return render(request, 'attendance/bus.html', context)






from datetime import datetime, timedelta
from django.shortcuts import render
from .models import Employee, Attendance
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def kashftmam(request):
    selected_date = request.GET.get('date')
    start = request.GET.get('start', 1)  # القيمة الافتراضية 1
    end = request.GET.get('end', 47)    # القيمة الافتراضية 47
    padding_size = request.GET.get('padding_size', 1)  # القيمة الافتراضية 1

    attendance_data = []
    employees = Employee.objects.select_related('department').all().order_by('dep_sort')
    date_range = []

    if selected_date:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        date_range = [selected_date + timedelta(days=i) for i in range(7)]
        attendance_data = Attendance.objects.filter(date__in=date_range).order_by('date')

    start = int(start) if start else 1
    end = int(end) if end else 47
    filtered_employees = employees[start - 1:end]
    
    for idx, employee in enumerate(filtered_employees, start=start):
        employee.serial_number = idx  

    return render(request, 'attendance/kashftmam.html', {
        'attendance_data': attendance_data,
        'selected_date': selected_date,
        'date_range': date_range,
        'filtered_employees': filtered_employees,
        'first_number': start,
        'last_number': end,
        'padding_size': padding_size,
    })
    
    
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, timedelta
from babel.dates import format_date
from .forms import DateForm, ChunkSizeForm
from .models import Attendance

def split_into_chunks(lst, chunk_size):
    """Split a list into chunks of specified size."""
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

@login_required(login_url='/login/')
def outs(request):
    # Calculate tomorrow's date
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_str = tomorrow.strftime('%Y-%m-%d')

    # Initialize the forms with default values
    selected_date = request.GET.get('date', tomorrow_str)
    chunk_size = int(request.GET.get('chunk_size', 40))  # Default to 40

    # Process the form submissions
    date_form = DateForm(request.GET or {'date': tomorrow_str})
    chunk_size_form = ChunkSizeForm(request.GET or {'chunk_size': chunk_size})

    if date_form.is_valid():
        selected_date = date_form.cleaned_data['date']
    if chunk_size_form.is_valid():
        chunk_size = chunk_size_form.cleaned_data['chunk_size']

    # Ensure selected_date is a date object
    if not isinstance(selected_date, date):
        selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
    else:
        selected_date_obj = selected_date

    # Format the selected date in Arabic
    formatted_date = format_date(selected_date_obj, format='EEEE dd/MM/yyyy', locale='ar')

    # Fetch records for the selected date
    records = Attendance.objects.filter(date=selected_date_obj, in_or_out='3').select_related('employee')

    # Organize data by state
    data = {}
    for record in records:
        # Merge specific states into broader categories
        state_mappings = {
            'منحة': 'راحات', 'عطلة': 'راحات', '8 صباحاً': 'راحات', 'ر بديلة': 'راحات', 'راحة': 'راحات',
            'فرقة': 'فرق', 'ت دوري': 'فرق', 'ت تكراري': 'فرق',
            'مأمورية': 'مأمورية', 'مأمورية خ': 'مأمورية',
            'مرضي': 'مرضي', 'قرار66': 'مرضي',
            'خاصه': 'خاصه', 'ج وضع': 'خاصه'
        }
        state = state_mappings.get(record.state, record.state)
        if state not in data:
            data[state] = []
        data[state].append(record.employee.nickname)

    # Add serial numbers and 5 empty rows
    serialized_data = {}
    for state, nicknames in data.items():
        entries = [(i + 1, nickname) for i, nickname in enumerate(nicknames)]
        last_serial = entries[-1][0] if entries else 0
        entries.extend((last_serial + i, '') for i in range(1, 6))  # Add 5 empty rows
        serialized_data[state] = entries

    # Calculate totals
    out_states = [
        'راحة', 'دورية', 'ر بديلة', 'طارئة', 'مأمورية', 'مأمورية خ', 'فرقة', 'انتداب', 
        'مرضي', 'ج وضع', 'خاصه', '8 صباحاً', 'ت دوري', 'ت تكراري', 'منحة', 'عطلة', 'غياب', 'قرار66'
    ]
    total_out_states_records = Attendance.objects.filter(
        date=selected_date_obj, state__in=out_states
    ).count()

    in_states = ['نوبتجي', 'يومي']
    total_in_states_records = Attendance.objects.filter(
        date=selected_date_obj, state__in=in_states
    ).count()

    not_states = ['_']
    total_not_states_records = Attendance.objects.filter(
        date=selected_date_obj, state__in=not_states
    ).count()

    total_all_states = total_in_states_records + total_out_states_records + total_not_states_records

    # Order data for display
    STATE_ORDER = ['دورية', '_', 'طارئة', 'مرضي', 'خاصه', 'فرق', 'انتداب', 'مأمورية', 'راحات', 'غياب']
    ordered_data = []
    for state in STATE_ORDER:
        if state in serialized_data:
            ordered_data.extend((state, serial, nickname) for serial, nickname in serialized_data[state])

    # Split into chunks
    grouped_data = list(split_into_chunks(ordered_data, chunk_size))

    context = {
        'date_form': date_form,
        'chunk_size_form': chunk_size_form,
        'selected_date': selected_date_obj,
        'formatted_date': formatted_date,
        'grouped_data': grouped_data,
        'serialized_data': serialized_data,
        'total_in_states_records': total_in_states_records,
        'total_out_states_records': total_out_states_records,
        'total_all_states': total_all_states,
    }
    return render(request, 'attendance/outs.html', context)
    
    
    
    
    
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from .models import Attendance
from em_data.models import Employee

@login_required(login_url='/login/')
def insert_many_attendance(request):
    employees = Employee.objects.all().order_by('sort_number')
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        employee_ids = request.POST.getlist('employee_ids')  # Get multiple employee IDs as a list
        state = request.POST.get('state')
        in_or_out = 'out'  # تصحيح لتتناسب مع خيارات النموذج
        food = False  # تصحيح لأن الحقل BooleanField

        print(f"POST Data: {request.POST}")  # تصحيح الأخطاء: طباعة البيانات
        print(f"From Date: {from_date}, To Date: {to_date}, Employee IDs: {employee_ids}, State: {state}")

        if from_date and to_date and employee_ids and state:
            try:
                from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
                to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
            except ValueError as e:
                return render(request, 'attendance/insertmany.html', {
                    'employees': employees,
                    'error': 'تنسيق التاريخ غير صحيح'
                })

            if from_date > to_date:
                return render(request, 'attendance/insertmany.html', {
                    'employees': employees,
                    'error': 'نطاق التاريخ غير صالح'
                })

            # قائمة لتخزين السجلات الجديدة لـ bulk_create
            new_attendance_records = []

            # حلقة عبر كل موظف
            for employee_id in employee_ids:
                try:
                    employee = Employee.objects.get(id=employee_id)
                    print(f"Found Employee: {employee.name}")  # تصحيح الأخطاء: طباعة معلومات الموظف
                except Employee.DoesNotExist:
                    return render(request, 'attendance/insertmany.html', {
                        'employees': employees,
                        'error': f'معرف الموظف {employee_id} غير موجود'
                    })

                # توليد التواريخ في النطاق
                current_date = from_date
                while current_date <= to_date:
                    # التحقق من وجود سجل حالي
                    existing_record = Attendance.objects.filter(
                        employee=employee,  # استخدام الكائن بدلاً من employee_id
                        date=current_date
                    ).first()

                    if existing_record:
                        # تحديث السجل الموجود
                        existing_record.state = state
                        existing_record.in_or_out = in_or_out
                        existing_record.food = food
                        existing_record.save()
                        print(f"Updated record for {employee.name} on {current_date}")
                    else:
                        # إضافة سجل جديد إلى القائمة
                        new_attendance_records.append(
                            Attendance(
                                employee=employee,  # استخدام كائن Employee
                                date=current_date,
                                state=state,
                                in_or_out=in_or_out,
                                food=food
                            )
                        )
                        print(f"Queued new record for {employee.name} on {current_date}")

                    # الانتقال إلى التاريخ التالي
                    current_date += timedelta(days=1)

            # إنشاء السجلات الجديدة دفعة واحدة
            if new_attendance_records:
                Attendance.objects.bulk_create(new_attendance_records)
                print(f"Created {len(new_attendance_records)} new records")

            print("Records processed successfully")  # تصحيح الأخطاء: طباعة النجاح
            return redirect('insert_many_attendance')  # إعادة توجيه عند النجاح

        else:
            return render(request, 'attendance/insertmany.html', {
                'employees': employees,
                'error': 'يرجى ملء جميع الحقول المطلوبة'
            })

    return render(request, 'attendance/insertmany.html', {'employees': employees})


from django.shortcuts import render
from django.db.models import Count, Q, OuterRef, Subquery
from django.db import models
from .models import Employee, Attendance
from datetime import datetime, timedelta
import calendar
@login_required(login_url='/login/')
def monthly_discount(request):
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
        
        attendance_subquery_d_t = Attendance.objects.filter(
            employee=OuterRef('pk'),
            date__year=year,
            date__month=month,
            state__in=['دورية', 'طارئة']
        ).values('employee').annotate(
            total_d_t=Count('state')
        ).values('total_d_t')
        
        attendance_subquery_rahat = Attendance.objects.filter(
            employee=OuterRef('pk'),
            date__year=year,
            date__month=month,
            state__in=['راحة', 'ر بديلة', '8 صباحاً', 'عطلة', 'منحة']
        ).values('employee').annotate(
            total_rahat=Count('state')
        ).values('total_rahat')
        
        attendance_subquery_food = Attendance.objects.filter(
            employee=OuterRef('pk'),
            date__year=year,
            date__month=month,
            food=True
        ).values('employee').annotate(
            total_food=Count('food')
        ).values('total_food')
        
        attendance_subquery_maradi = Attendance.objects.filter(
            employee=OuterRef('pk'),
            date__year=year,
            date__month=month,
            state='مرضي'
        ).values('employee').annotate(
            total_maradi=Count('state')
        ).values('total_maradi')
        
        employees = Employee.objects.select_related('rank').annotate(
            total_d_t=Subquery(attendance_subquery_d_t, output_field=models.IntegerField()),
            total_rahat=Subquery(attendance_subquery_rahat, output_field=models.IntegerField()),
            total_food=Subquery(attendance_subquery_food, output_field=models.IntegerField()),
            total_maradi=Subquery(attendance_subquery_maradi, output_field=models.IntegerField())
        ).order_by('sort_number').values('name', 'nots', 'rank__name', 'dep_sort', 'total_d_t', 'total_rahat', 'total_food', 'total_maradi')

        for employee in employees:
            total_d_t = employee['total_d_t'] or 0
            total_rahat = employee['total_rahat'] or 0
            total_food = employee['total_food'] or 0
            total_maradi = employee['total_maradi'] or 0
            
            employee['total_discount'] = total_d_t + total_rahat + total_food + total_maradi
            employee['total_eligible'] = num_days_in_next_month - employee['total_discount']
        
        context = {
            'employees': employees,
            'month': month,
            'year': year,
            'months': months,
            'years': years,
        }
        
        return render(request, 'attendance/monthlyDiscount.html', context)
    
    context = {
        'months': months,
        'years': years,
    }
    return render(request, 'attendance/monthlyDiscount.html', context)







