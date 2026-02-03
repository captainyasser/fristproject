from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Employee, ElawaRecord
from .forms import ElawaBatchForm, ElawaRecordForm

def index(request):
    return render(request, "elawat_tashgeea/index.html")

def batch_create(request):
    if request.method == 'POST':
        form = ElawaBatchForm(request.POST)
        if form.is_valid():
            decision_number = form.cleaned_data['decision_number']
            elawa_date = form.cleaned_data['elawa_date']
            notes = form.cleaned_data['notes']
            employees = form.cleaned_data['employees']
            for emp in employees:
                ElawaRecord.objects.create(
                    employee=emp,
                    decision_number=decision_number,
                    elawa_date=elawa_date,
                    notes=notes
                )
            messages.success(request, "تم حفظ العلاوة لجميع الأفراد المحددين.")
            return redirect('elawat_tashgeea:index')
    else:
        form = ElawaBatchForm()
    return render(request, "elawat_tashgeea/batch_create.html", {"form": form})

def employee_elawat(request):
    employees = Employee.objects.filter(deleted_at__isnull=True).order_by('sort_number')
    selected_emp_id = request.GET.get('employee_id')
    selected_employee = None
    elawat = []
    if selected_emp_id:
        selected_employee = get_object_or_404(Employee, id=selected_emp_id)
        elawat = ElawaRecord.objects.filter(employee=selected_employee).order_by('-elawa_date')
    return render(request, "elawat_tashgeea/employee_elawat.html", {
        "employees": employees,
        "selected_employee": selected_employee,
        "elawat": elawat,
        "selected_emp_id": selected_emp_id,
    })

def edit_elawa(request, pk):
    elawa = get_object_or_404(ElawaRecord, id=pk)
    if request.method == 'POST':
        form = ElawaRecordForm(request.POST, instance=elawa)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تعديل العلاوة بنجاح")
            return redirect(f"/elawat-tashgeea/employee/select/?employee_id={elawa.employee.id}")
    else:
        form = ElawaRecordForm(instance=elawa)
    return render(request, "elawat_tashgeea/edit_elawa.html", {"form": form, "elawa": elawa})

def delete_elawa(request, pk):
    elawa = get_object_or_404(ElawaRecord, id=pk)
    employee_id = elawa.employee.id
    elawa.delete()
    return redirect(f"/elawat-tashgeea/employee/select/?employee_id={employee_id}")


def elawat_by_year(request):
    year = request.GET.get('year')
    elawat = []
    if year:
        elawat = ElawaRecord.objects.filter(elawa_date__year=year).order_by('-elawa_date')
    return render(request, "elawat_tashgeea/elawat_by_year.html", {"elawat": elawat, "year": year})





from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ElawaRecord
from em_data.models import Employee
from .forms import MultiElawaForm

def add_multiple_elawat(request):
    selected_employee = None
    old_elawat = []

    if request.method == "POST":
        # إذا كان المستخدم اختار اسم الموظف فقط لعرض العلاوات
        if "employee" in request.POST and "load_old" in request.POST:
            emp_id = request.POST.get("employee")
            if emp_id:
                selected_employee = Employee.objects.get(id=emp_id)
                old_elawat = ElawaRecord.objects.filter(employee=selected_employee).order_by("-elawa_date")
            form = MultiElawaForm(initial={"employee": emp_id})
            return render(request, "elawat_tashgeea/add_multiple_elawat.html", {
                "form": form,
                "selected_employee": selected_employee,
                "old_elawat": old_elawat,
            })

        # إذا كان المستخدم يريد حفظ العلاوات الجديدة
        employee_id = request.POST.get("employee")
        selected_employee = Employee.objects.get(id=employee_id)

        count = int(request.POST.get("count"))

        for i in range(1, count + 1):
            decision_number = request.POST.get(f"decision_number_{i}")
            elawa_date = request.POST.get(f"elawa_date_{i}")
            notes = request.POST.get(f"notes_{i}")

            if decision_number and elawa_date:
                ElawaRecord.objects.create(
                    employee=selected_employee,
                    decision_number=decision_number,
                    elawa_date=elawa_date,
                    notes=notes
                )

        messages.success(request, "✓ تم حفظ العلاوات الجديدة بنجاح")
        return redirect("elawat_tashgeea:add_multiple_elawat")

    # GET request
    form = MultiElawaForm()
    return render(request, "elawat_tashgeea/add_multiple_elawat.html", {"form": form})



