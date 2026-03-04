from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Case, When, Value, IntegerField, Q
import json
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from .models import Attendance
from em_data.models import Employee
from departments.models import Department
from .validation_utils import validate_attendance, check_operation_compliance

@login_required
def attendance_validation_view(request):
    # Default params simliar to attendance_3w
    if 'start_date' not in request.GET:
        today = datetime.today()
        # Find prev Saturday
        last_week = today - timedelta(days=7)
        days_to_subtract = (last_week.weekday() - 5) % 7
        default_start_date = last_week - timedelta(days=days_to_subtract)
        start_date = default_start_date.strftime('%Y-%m-%d')
    else:
        start_date = request.GET.get('start_date')

    num_days = int(request.GET.get('num_days', 28))
    sort_by = request.GET.get('sort_by', 'sort_number')
    department_filter = request.GET.get('departments', '')
    gender_filter = request.GET.get('gender', '')
    search_query = request.GET.get('q', '')

    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = start_date_obj + timedelta(days=num_days - 1)
    
    # Week days for header
    week_days = [start_date_obj + timedelta(days=i) for i in range(num_days)]
    
    # Fetch Employees
    employees = Employee.objects.filter(mainornot=1)
    if department_filter:
        employees = employees.filter(department_id=department_filter)
    
    if gender_filter:
        employees = employees.filter(gender=gender_filter)

    if search_query:
        employees = employees.filter(
            Q(name__icontains=search_query) | 
            Q(nickname__icontains=search_query) | 
            Q(police_number__icontains=search_query)
        )

    if sort_by == 'operation':
        employees = employees.annotate(
            operation_order=Case(
                When(operation='السبت', then=Value(1)),
                When(operation='الأحد', then=Value(2)),
                When(operation='الاثنين', then=Value(3)),
                When(operation='الثلاثاء', then=Value(4)),
                When(operation='الأربعاء', then=Value(5)),
                When(operation='الخميس', then=Value(6)),
                When(operation='الجمعة', then=Value(7)),
                When(operation='عمل يومي', then=Value(8)),
                When(operation='انتداب', then=Value(9)),
                When(operation='خاصه', then=Value(10)),
                default=Value(11),
                output_field=IntegerField(),
            )
        ).order_by('operation_order', 'sort_number')
    elif sort_by in ['dep_sort', 'sort_number', 'department']:
        employees = employees.order_by(sort_by)

    # We need to process ALL matching employees to filter by error
    # This might be slow if there are thousands? If so, paginate first?
    # User says "Display individuals who have attendance statuses in incorrect order".
    # This implies filtering.
    
    # Prepare date range for validation (need history - e.g. 7 days before start)
    history_start = start_date_obj.date() - timedelta(days=7) # .date() because datetime object needs to match model DateField?
    # Actually start_date_obj is likely datetime.
    
    validation_end = end_date_obj.date()
    # Fetch all relevant attendance records in bulk
    attendance_records = Attendance.objects.filter(
        employee__in=employees,
        date__range=[history_start, validation_end]
    ).select_related('employee')
    
    # Map attendance: employee_id -> date -> record
    att_map = {}
    for r in attendance_records:
        if r.employee_id not in att_map:
            att_map[r.employee_id] = {}
        att_map[r.employee_id][r.date] = r
        
    error_employees = []
    
    for emp in employees:
        emp_att_map = att_map.get(emp.id, {})
        # call validation
        # Start date for validation is start_date_obj.date()
        # Num days to check is num_days
        # But we pass the MAP which contains history.
        errors = validate_attendance(emp, emp_att_map, start_date_obj.date(), num_days)
        
        # Filter errors to only show those within the selected date range
        filtered_errors = [
            error for error in errors 
            if error['date'] >= start_date_obj.date() and error['date'] <= end_date_obj.date()
        ]
        
        if filtered_errors:
            emp.validation_errors = filtered_errors
            error_employees.append(emp)
            
    # Now paginate the error_employees
    paginator = Paginator(error_employees, 300)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    department_choices = Department.objects.values_list('id', 'name')

    context = {
        'start_date': start_date_obj,
        'num_days': num_days,
        'sort_by': sort_by,
        'department_filter': department_filter,
        'gender_filter': gender_filter,
        'week_days': week_days,
        'page_obj': page_obj,
        'department_choices': department_choices,
        'operation_choices': Employee.OPERATION_CHOICES,
        'today': datetime.today().date(),
        'search_query': search_query,
    }
    return render(request, 'attendance/attendance_validation.html', context)


@login_required
def irregular_validation_view(request):
    # Default params simliar to attendance_3w
    if 'start_date' not in request.GET:
        today = datetime.today()
        # Find prev Saturday
        last_week = today - timedelta(days=7)
        days_to_subtract = (last_week.weekday() - 5) % 7
        default_start_date = last_week - timedelta(days=days_to_subtract)
        start_date = default_start_date.strftime('%Y-%m-%d')
    else:
        start_date = request.GET.get('start_date')

    num_days = int(request.GET.get('num_days', 28))
    sort_by = request.GET.get('sort_by', 'sort_number')
    department_filter = request.GET.get('departments', '')
    gender_filter = request.GET.get('gender', '')
    search_query = request.GET.get('q', '')

    try:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    except ValueError:
        today = datetime.today()
        start_date_obj = today
        start_date = today.strftime('%Y-%m-%d')

    end_date_obj = start_date_obj + timedelta(days=num_days - 1)
    
    # Week days for header
    week_days = [start_date_obj + timedelta(days=i) for i in range(num_days)]
    
    # Fetch Employees
    employees = Employee.objects.filter(mainornot=1)
    if department_filter:
        employees = employees.filter(department_id=department_filter)
    
    if gender_filter:
        employees = employees.filter(gender=gender_filter)

    if search_query:
        employees = employees.filter(
            Q(name__icontains=search_query) | 
            Q(nickname__icontains=search_query) | 
            Q(police_number__icontains=search_query)
        )

    if sort_by == 'operation':
        employees = employees.annotate(
            operation_order=Case(
                When(operation='السبت', then=Value(1)),
                When(operation='الأحد', then=Value(2)),
                When(operation='الاثنين', then=Value(3)),
                When(operation='الثلاثاء', then=Value(4)),
                When(operation='الأربعاء', then=Value(5)),
                When(operation='الخميس', then=Value(6)),
                When(operation='الجمعة', then=Value(7)),
                When(operation='عمل يومي', then=Value(8)),
                When(operation='انتداب', then=Value(9)),
                When(operation='خاصه', then=Value(10)),
                default=Value(11),
                output_field=IntegerField(),
            )
        ).order_by('operation_order', 'sort_number')
    elif sort_by in ['dep_sort', 'sort_number', 'department']:
        employees = employees.order_by(sort_by)

    history_start = start_date_obj.date() - timedelta(days=7) 
    validation_end = end_date_obj.date()
    
    # Fetch all relevant attendance records in bulk
    attendance_records = Attendance.objects.filter(
        employee__in=employees,
        date__range=[history_start, validation_end]
    ).select_related('employee')
    
    # Map attendance: employee_id -> date -> record
    att_map = {}
    for r in attendance_records:
        if r.employee_id not in att_map:
            att_map[r.employee_id] = {}
        att_map[r.employee_id][r.date] = r
        
    error_employees = []
    
    # Use a dictionary to store errors for easier JS access: { employee_id: { date_str: error_message } }
    validation_errors_dict = {}

    for emp in employees:
        emp_att_map = att_map.get(emp.id, {})
        # Call IRREGULAR validation (Operation Compliance)
        errors = check_operation_compliance(emp, emp_att_map, start_date_obj.date(), num_days)
        
        # Filter errors to only show those within the selected date range
        filtered_errors = [
            error for error in errors 
            if error['date'] >= start_date_obj.date() and error['date'] <= end_date_obj.date()
        ]
        
        if filtered_errors:
            emp.validation_errors = filtered_errors
            error_employees.append(emp)
            
            # Populate dictionary
            if emp.id not in validation_errors_dict:
                validation_errors_dict[emp.id] = {}
            for err in filtered_errors:
                date_str = err['date'].strftime('%Y%m%d') # Match JS data-date format
                validation_errors_dict[emp.id][date_str] = err['message']
            
    # Pagination
    paginator = Paginator(error_employees, 300)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    department_choices = Department.objects.values_list('id', 'name')

    context = {
        'start_date': start_date_obj,
        'num_days': num_days,
        'sort_by': sort_by,
        'department_filter': department_filter,
        'gender_filter': gender_filter,
        'week_days': week_days,
        'page_obj': page_obj,
        'department_choices': department_choices,
        'operation_choices': Employee.OPERATION_CHOICES,
        'today': datetime.today().date(),
        'validation_errors_dict': json.dumps(validation_errors_dict),
        'search_query': search_query,
    }
    # Render the new template
    return render(request, 'attendance/irregular_validation.html', context)
