
from em_data.models import Employee
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from em_data.forms import EmployeeForm
from django.shortcuts import get_object_or_404


@login_required
def home(request):
    employees = Employee.objects.all().order_by("sort_number")  # ترتيب الموظفين حسب الرقم
    return render(request, "em_data/home.html", {"employees": employees})

@login_required
def add_employee(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save(commit=False)
            if request.user.institute:  # التأكد من أن المستخدم مرتبط بمعهد
                employee.institute = request.user.institute
            employee.save()
            return redirect("home")  # توجيه المستخدم إلى قائمة الموظفين بعد الإضافة
    else:
        form = EmployeeForm()

    return render(request, "em_data/add_employee.html", {"form": form})








@login_required
def edit_employee(request, employee_id):  # Use 'employee_id' here
    employee = get_object_or_404(Employee, id=employee_id)  # Match with 'id'

    if request.method == "POST":
        employee.name = request.POST["name"]
        employee.rank = request.POST["rank"]
        employee.police_number = request.POST["police_number"]
        employee.insurance_number = request.POST["insurance_number"]
        employee.date_of_birth = request.POST.get("date_of_birth") or None
        employee.date_of_appointment = request.POST.get("date_of_appointment") or None
        employee.save()
        return redirect("home")  # Redirect after saving

    return render(request, "em_data/edit_employee.html", {
        "employee": employee,
        "rank_choices": Employee.RANK_CHOICES
    })
