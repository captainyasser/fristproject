from django.shortcuts import render, redirect
from .models import Promotion
from em_data.models import Employee
from ranks.models import Rank

def add_tarkya(request):
    if request.method == 'POST':
        employee_ids = request.POST.getlist('employee')  # يعمل مع checkboxes
        to_rank = Rank.objects.get(id=request.POST['to_rank'])
        from_rank = Rank.objects.get(id=request.POST['from_rank']) if request.POST['from_rank'] else None

        for emp_id in employee_ids:
            employee = Employee.objects.get(id=emp_id)
            promotion = Promotion(
                employee=employee,
                from_rank=from_rank if from_rank else employee.rank,
                to_rank=to_rank,
                promotion_date=request.POST['promotion_date'],
                promotion_course_number=request.POST['promotion_course_number'],
                training_start_date=request.POST['training_start_date'],
                training_end_date=request.POST['training_end_date'],
                training_course_number=request.POST['training_course_number'],
                training_location=request.POST['training_location'],
                notes=request.POST['notes']
            )
            promotion.save()
        return redirect('add_tarkya')

    employees = Employee.objects.all()
    ranks = Rank.objects.all()
    return render(request, 'tarkyat/add_tarkya.html', {'employees': employees, 'ranks': ranks})