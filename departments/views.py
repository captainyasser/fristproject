from django.shortcuts import render, redirect
from .models import Department

def departments_list(request):
    departments = Department.objects.all()
    return render(request, 'departments/departments.html', {'departments': departments})

def add_department(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Department.objects.create(name=name)
        return redirect('departments_list')

def edit_department(request, department_id):
    department = Department.objects.get(id=department_id)
    if request.method == "POST":
        department.name = request.POST.get("name")
        department.save()
        return redirect('departments_list')

def delete_department(request, department_id):
    department = Department.objects.get(id=department_id)
    department.delete()
    return redirect('departments_list')
