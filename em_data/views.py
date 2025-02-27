

from django.contrib.auth.decorators import login_required
from .models import Employee, Rank, Department
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import datetime
from dateutil.relativedelta import relativedelta

@login_required
def home(request):
    employees = Employee.objects.all().order_by("sort_number")
    ranks = Rank.objects.all()
    departments = Department.objects.all()

    return render(request, "em_data/home.html", {
        "employees": employees,
        "ranks": ranks,
        "departments": departments,
    })

# @login_required
# def age_update(request):
#     employees = Employee.objects.all()
#     employees_to_update = []

#     for employee in employees:
#         updated = False
#         if employee.id_number:
#             new_date_of_birth = employee.extract_birth_date()
#             if new_date_of_birth and new_date_of_birth != employee.date_of_birth:
#                 employee.date_of_birth = new_date_of_birth
#                 updated = True

#         if employee.date_of_birth:
#             today = datetime.today().date()
#             age_delta = relativedelta(today, employee.date_of_birth)
#             if employee.age != age_delta.years:
#                 employee.age = age_delta.years
#                 updated = True
#             new_retirement = employee.date_of_birth + relativedelta(years=60)
#             if employee.date_of_retirement != new_retirement:
#                 employee.date_of_retirement = new_retirement
#                 updated = True

#         if updated:
#             employees_to_update.append(employee)

#     # تحديث جماعي
#     if employees_to_update:
#         Employee.objects.bulk_update(employees_to_update, ['date_of_birth', 'age', 'date_of_retirement'])

#     context = {
#         "updated_count": len(employees_to_update),
#         "total_employees": employees.count(),
#     }
#     return render(request, "em_data/age_update.html", context)




@login_required(login_url='/login/')
def add_employee(request):
    user = request.user  # المستخدم الحالي

    # التأكد من أن المستخدم لديه معهد
    try:
        user_institute = user.institute  # جلب معهد المستخدم
    except AttributeError:
        user_institute = None  # إذا لم يكن لديه معهد، ضع القيمة None

    if request.method == "POST":
        name = request.POST['name']
        sort_number = request.POST['sort_number']
        rank_id = request.POST['rank']
        department_id = request.POST.get('department', None)
        date_of_appointment = request.POST.get('date_of_appointment', None)

        # إنشاء الموظف الجديد وربطه بمعهد المستخدم
        Employee.objects.create(
            name=name,
            sort_number=sort_number,
            rank_id=rank_id,
            department_id=department_id,
            institute=user_institute,  # تعيين معهد المستخدم افتراضيًا
            date_of_appointment=date_of_appointment
        )

        return redirect('home')

    ranks = Rank.objects.all()
    departments = Department.objects.all()

    return render(request, 'em_data/add_employee.html', {
        'ranks': ranks,
        'departments': departments,
        'user_institute': user_institute  # تمرير المعهد إلى القالب
    })


@login_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    ranks = Rank.objects.all()
    departments = Department.objects.all()

    if request.method == 'POST':
        print("POST data:", request.POST)
        try:
            # تحديث الحقول الأساسية
            employee.name = request.POST.get('name', employee.name)
            employee.nickname = request.POST.get('nickname', employee.nickname)
            employee.sort_number = request.POST.get('sort_number', employee.sort_number)
            employee.police_number = request.POST.get('police_number', employee.police_number)
            employee.insurance_number = request.POST.get('insurance_number', employee.insurance_number)
            employee.age = employee.age
            employee.date_of_birth = employee.date_of_birth
            employee.date_of_retirement = employee.date_of_retirement
            # تحويل القيمة الفارغة إلى None لـ DateField
            date_of_edara_value = request.POST.get('date_of_edara', employee.date_of_edara)
            employee.date_of_edara = date_of_edara_value if date_of_edara_value and date_of_edara_value != '' else None
            date_of_appointment_value = request.POST.get('date_of_appointment', employee.date_of_appointment)
            employee.date_of_appointment = date_of_appointment_value if date_of_appointment_value and date_of_appointment_value != '' else None
            employee.id_number = request.POST.get('id_number', employee.id_number)
            employee.phone_number = request.POST.get('phone_number', employee.phone_number)
            employee.alt_phone_number = request.POST.get('alt_phone_number', employee.alt_phone_number)
            employee.marital_status = request.POST.get('marital_status', employee.marital_status) or None
            employee.gender = request.POST.get('gender', employee.gender) or None
            employee.governorate = request.POST.get('governorate', employee.governorate)
            employee.district = request.POST.get('district', employee.district)
            employee.address = request.POST.get('address', employee.address)
            employee.health_status = request.POST.get('health_status', employee.health_status) or None

            employee.amen_or_ola = bool(int(request.POST.get('amen_or_ola', employee.amen_or_ola)))
            employee.bus = 1 if request.POST.get('bus') else 0
            dep_sort_value = request.POST.get('dep_sort', employee.dep_sort)
            employee.dep_sort = int(dep_sort_value) if dep_sort_value and dep_sort_value != '' else None
            employee.mainornot = int(request.POST.get('mainornot', employee.mainornot))
            employee.tmamam = 1 if request.POST.get('tmamam') else 0
            employee.operation = request.POST.get('operation', employee.operation)
            rank_kind_value = request.POST.get('rank_kind', employee.rank_kind)
            employee.rank_kind = int(rank_kind_value) if rank_kind_value and rank_kind_value != '' else None

            rank_id = request.POST.get('rank')
            employee.rank = Rank.objects.get(id=rank_id) if rank_id else employee.rank

            department_id = request.POST.get('department')
            employee.department = Department.objects.get(id=department_id) if department_id else employee.department

            if employee.id_number:
                new_date_of_birth = employee.extract_birth_date()
                if new_date_of_birth and new_date_of_birth != employee.date_of_birth:
                    employee.date_of_birth = new_date_of_birth

            if employee.date_of_birth:
                today = datetime.today().date()
                age_delta = relativedelta(today, employee.date_of_birth)
                if employee.age != age_delta.years:
                    employee.age = age_delta.years
                new_retirement = employee.date_of_birth + relativedelta(years=60)
                if employee.date_of_retirement != new_retirement:
                    employee.date_of_retirement = new_retirement

            employee.save()
            print("Saved successfully")
            messages.success(request, 'تم تعديل بيانات الموظف وتحديث العمر بنجاح!')
            return redirect('home')

        except Exception as e:
            messages.error(request, f'حدث خطأ: {str(e)}')
            print(f"Error: {str(e)}")
            return render(request, 'em_data/home.html', {
                'employee': employee,
                'ranks': ranks,
                'departments': departments,
                'employees': Employee.objects.all().order_by('sort_number'),
            })

    return render(request, 'em_data/home.html', {
        'employee': employee,
        'ranks': ranks,
        'departments': departments,
        'employees': Employee.objects.all().order_by('sort_number'),
    })
    
    
    


def employee_statement(request):
    employees = Employee.objects.all().order_by('sort_number')
    selected_employee = None

    if request.method == 'GET' and 'employee' in request.GET:
        employee_id = request.GET.get('employee')
        if employee_id:
            selected_employee = Employee.objects.get(id=employee_id)

    return render(request, 'em_data/employee_statement.html', {
        'employees': employees,
        'selected_employee': selected_employee,
    })