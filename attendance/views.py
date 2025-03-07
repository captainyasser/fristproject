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
        department_filter = "16"  # تعيين القسم الافتراضي
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
        department_filter = "0"  # تعيين القسم الافتراضي
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
    paginator = Paginator(employees, 100)
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
                .values_list('employee__name', flat=True)  # Changed 'name' to 'employee__name'
                
                # إضافة الأرقام التسلسلية
                names_with_serials = [(index + 1, name) for index, name in enumerate(names)]
                
                # تنسيق التاريخ يدويًا
                day_name = ARABIC_DAYS[selected_date.weekday()]
                formatted_date = f"{day_name} {selected_date.day:02d}/{selected_date.month:02d}/{selected_date.year}"
    else:
        form = DateForm()
        selected_date = date.today()
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




