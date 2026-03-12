from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from collections import defaultdict
import json
from datetime import datetime, timedelta
from .models import Employee, TrainingTeam, Places, EmTrainingTeams, PeriodicTraining, EmPeriodicTraining, QualifyingTraining, EmQualifyingTraining
from attendance.models import Attendance

# 1. عرض صفحة الفرق التدريبية الرئيسية (training.html)
@login_required(login_url='/login/')
def training_page_view(request):
    return render(request, 'training/training.html')

# 2. عرض الفرق التدريبية حسب الفرد (em_training_teams.html)
@login_required(login_url='/login/')
def em_training_teams_view(request):
    employees = Employee.objects.all().order_by('sort_number')
    teams = EmTrainingTeams.objects.select_related('employee', 'training_team', 'place').order_by('employee__sort_number', 'start_date')

    employee_teams = defaultdict(list)
    for team in teams:
        employee_teams[team.employee].append(team)

    for employee in employees:
        while len(employee_teams[employee]) < 15:
            employee_teams[employee].append(None)

    context = {
        'employee_teams': {employee: employee_teams[employee] for employee in employees},
    }
    return render(request, 'training/em_training_teams.html', context)




# 3. عرض الفرق التدريبية حسب اسم الفرقة (training_teams.html)
@login_required(login_url='/login/')
def training_teams_view(request):
    # إنشاء قاموس يجمع الأفراد حسب اسم الفرقة التدريبية
    training_teams = {}

    for team in EmTrainingTeams.objects.select_related('employee', 'training_team').order_by('employee__sort_number'):
        team_name = team.training_team.name  # اسم الفرقة
        if team_name not in training_teams:
            training_teams[team_name] = []
        
        training_teams[team_name].append(team.employee.name)  # إضافة أسماء الأفراد

    # ترتيب الفرق حسب عدد الأفراد (من الأكثر إلى الأقل)
    # training_teams = dict(sorted(training_teams.items(), key=lambda x: len(x[1]), reverse=True))
    training_teams = dict(sorted(training_teams.items(), key=lambda x: x[0]))  # ترتيب حسب اسم الفرقة


    # التأكد من أن كل فرقة تحتوي على 80 صفًا على الأقل
    for team_name in training_teams:
        while len(training_teams[team_name]) < 160 and len(training_teams[team_name]) > 0:
            training_teams[team_name].append("")  # إضافة صفوف فارغة
    # إضافة عمود رقم تسلسلي لكل فرد
    for team_name, employees in training_teams.items():
        training_teams[team_name] = [(i + 1, employees[i]) for i in range(len(employees))]

    context = {
        'training_teams': training_teams
    }
    
    return render(request, 'training/training_teams.html', context)



# 4. فلتر الفرق التدريبية (training-teams-filter.html)
@login_required(login_url='/login/')
def training_teams_filter(request):
    name_query = request.GET.get('name', '')
    training_team_query = request.GET.get('training_team', '')
    employee_query = request.GET.get('employee', '')

    teams = EmTrainingTeams.objects.all()

    if name_query:
        teams = teams.filter(name__icontains=name_query)
    if training_team_query:
        teams = teams.filter(training_team_id=training_team_query)
    if employee_query:
        teams = teams.filter(employee_id=employee_query)

    training_teams = TrainingTeam.objects.all().order_by('name')
    employees = Employee.objects.all().order_by('sort_number')

    context = {
        'teams': teams,
        'training_teams': training_teams,
        'employees': employees,
        'name_query': name_query,
        'training_team_query': training_team_query,
        'employee_query': employee_query
    }
    return render(request, 'training/training-teams-filter.html', context)

# 5. إضافة فرقة تدريبية جديدة (insert_training.html)
@login_required(login_url='/login/')
def insert_training(request):
    if request.method == "POST":
        employees = request.POST.getlist('employees')
        training_team = TrainingTeam.objects.get(id=request.POST['training_team'])
        place = Places.objects.get(id=request.POST['place'])
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        result = request.POST.get('result', 'إنتظار')
        note = request.POST.get('note', '')
        round_num = request.POST.get('round_num')
        success_certificate_image = request.FILES.get('success_certificate_image')
        
        if round_num == '':
            round_num = None

        if not employees:
            messages.error(request, "يجب اختيار موظف واحد على الأقل")
            return redirect('insert_training')

        try:
            for emp_id in employees:
                employee = Employee.objects.get(id=emp_id)
                # Check for existing record to avoid crash due to UniqueConstraint
                if EmTrainingTeams.objects.filter(
                    employee=employee,
                    training_team=training_team,
                    start_date=start_date,
                    end_date=end_date
                ).exists():
                    messages.warning(request, f"التدريب موجود مسبقاً للموظف: {employee.name}")
                    continue

                EmTrainingTeams.objects.create(
                    employee=employee,
                    name=employee.name,
                    training_team=training_team,
                    place=place,
                    start_date=start_date,
                    end_date=end_date,
                    result=result,
                    round_num=round_num,
                    note=note,
                    success_certificate_image=success_certificate_image
                )

                # Add Attendance records for the duration of the training
                start = datetime.strptime(start_date, "%Y-%m-%d").date()
                end = datetime.strptime(end_date, "%Y-%m-%d").date()
                delta = end - start

                for i in range(delta.days + 1):
                    day = start + timedelta(days=i)
                    Attendance.objects.update_or_create(
                        employee=employee,
                        date=day,
                        defaults={
                            'state': 'فرقة',
                            'note': note
                        }
                    )
            
            messages.success(request, "تمت عملية الإضافة وتحديث سجل الحضور.")
        except Exception as e:
            messages.error(request, f"حدث خطأ أثناء الحفظ: {str(e)}")
            
        return redirect('insert_training')

    employees = Employee.objects.all().order_by('sort_number')
    training_teams = TrainingTeam.objects.all().order_by('name')
    places = Places.objects.all().order_by('name')

    context = {
        'employees': employees,
        'training_teams': training_teams,
        'places': places
    }
    return render(request, 'training/insert_training.html', context)

# 6. تعديل سجل تدريبي (edit_training_record.html)
@login_required(login_url='/login/')
def edit_training_record(request):
    employees = Employee.objects.all().order_by('sort_number')
    return render(request, 'training/edit_training_record.html', {'employees': employees})



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import EmTrainingTeams

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_training_record(request, training_id):
    try:
        # Delete record from EmTrainingTeams using the provided training_id
        training_record = EmTrainingTeams.objects.get(id=training_id)
        training_record.delete()
        return JsonResponse({"success": True, "message": "تم الحذف بنجاح"})
    except EmTrainingTeams.DoesNotExist:
        return JsonResponse({"success": False, "error": "السجل التدريبي غير موجود"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)





@login_required(login_url='/login/')
def get_employee_training_data(request, employee_id):
    """Fetch training data for a selected employee and return as JSON."""
    training_records = EmTrainingTeams.objects.filter(employee_id=employee_id).select_related('place', 'training_team').order_by('start_date')
    
    training_data = []
    for record in training_records:
        training_data.append({
            'id': record.id,
            'employee__name': record.employee.name,
            'start_date': record.start_date.strftime('%Y-%m-%d'),
            'end_date': record.end_date.strftime('%Y-%m-%d'),
            'result': record.result,
            'round_num': record.round_num,
            'place_id': record.place_id,
            'training_team_id': record.training_team_id,
            'note': record.note,
            'success_certificate_image_url': record.success_certificate_image.url if record.success_certificate_image else None
        })
    
    places = list(Places.objects.values('id', 'name'))  # Fetch available places
    training_teams = list(TrainingTeam.objects.values('id', 'name'))  # Fetch available training teams
    
    return JsonResponse({
        "training_data": training_data,
        "places": places,
        "training_teams": training_teams
    })

@login_required(login_url='/login/')
@csrf_exempt
def update_training_record(request):
    if request.method == "POST":
        try:
            # Check if it's FormData (with files) or JSON
            if request.content_type and 'application/json' in request.content_type:
                data = json.loads(request.body)
                training_record = EmTrainingTeams.objects.get(id=data['id'])
                
                training_record.start_date = data['start_date']
                training_record.end_date = data['end_date']
                training_record.result = data.get('result', '')
                training_record.round_num = data.get('round_num', None)
                training_record.place_id = data['place_id']
                training_record.training_team_id = data['training_team_id']
                training_record.note = data.get('note', '')
            else:
                # Handle FormData (with potential file upload)
                training_record = EmTrainingTeams.objects.get(id=request.POST.get('id'))
                
                training_record.start_date = request.POST.get('start_date')
                training_record.end_date = request.POST.get('end_date')
                training_record.result = request.POST.get('result', '')
                training_record.round_num = request.POST.get('round_num') or None
                training_record.place_id = request.POST.get('place_id')
                training_record.training_team_id = request.POST.get('training_team_id')
                training_record.note = request.POST.get('note', '')
                
                # Handle file upload
                if 'success_certificate_image' in request.FILES:
                    training_record.success_certificate_image = request.FILES['success_certificate_image']
            
            training_record.save()

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})







from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Places
from .forms import PlacesForm

def places_page(request):
    places = Places.objects.all()
    form = PlacesForm()

    if request.method == "POST":
        if "delete" in request.POST:  # Handle Delete
            place = get_object_or_404(Places, pk=request.POST.get("place_id"))
            place.delete()
        else:  # Handle Add/Edit
            if request.POST.get("place_id"):  # Edit
                place = get_object_or_404(Places, pk=request.POST.get("place_id"))
                form = PlacesForm(request.POST, instance=place)
            else:  # Add
                form = PlacesForm(request.POST)
            
            if form.is_valid():
                form.save()
    
        return redirect("places_page")

    return render(request, "training/places.html", {"places": places, "form": form})

@login_required(login_url='/login/')
def current_teams_view(request):
    # Get the filter date from request, default to today
    filter_date_str = request.GET.get('start_date')
    if filter_date_str:
        try:
            filter_date = datetime.strptime(filter_date_str, '%Y-%m-%d').date()
        except ValueError:
            filter_date = datetime.today().date()
    else:
        filter_date = datetime.today().date()
    
    # Teams that are active from the selected date onwards (end_date >= filter_date)
    current_active_records = EmTrainingTeams.objects.filter(
        end_date__gte=filter_date
    ).select_related('employee', 'training_team', 'place', 'employee__rank', 'employee__department').order_by('training_team__name', 'start_date', 'employee__rank__id', 'employee__sort_number')
    
    # Grouping by unique training instance
    teams_map = {}
    for record in current_active_records:
        # Create a unique key for the course instance
        key = f"{record.training_team.id}_{record.place.id}_{record.start_date}_{record.end_date}"
        
        if key not in teams_map:
            teams_map[key] = {
                'team_name': record.training_team.name,
                'place_name': record.place.name,
                'start_date': record.start_date,
                'end_date': record.end_date,
                'employees': []
            }
        teams_map[key]['employees'].append(record.employee)
        
    context = {
        'grouped_teams': list(teams_map.values()),
        'today': datetime.today().date(),
        'selected_date': filter_date
    }
    return render(request, 'training/current_teams.html', context)

# --- Periodic Training Views ---

@login_required(login_url='/login/')
def periodic_training_dashboard(request):
    """Dashboard for Periodic Training."""
    return render(request, 'training/periodic_dashboard.html')

@login_required(login_url='/login/')
def insert_periodic_training(request):
    """Insert Periodic Training records and update attendance."""
    if request.method == "POST":
        employees = request.POST.getlist('employees')
        training_type = PeriodicTraining.objects.get(id=request.POST['training_type'])
        place = Places.objects.get(id=request.POST['place'])
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        round_num = request.POST.get('round_num')
        note = request.POST.get('note', '')

        if not employees:
            messages.error(request, "يجب اختيار موظف واحد على الأقل")
            return redirect('insert_periodic_training')

        try:
            for emp_id in employees:
                employee = Employee.objects.get(id=emp_id)
                
                EmPeriodicTraining.objects.create(
                    employee=employee,
                    training_type=training_type,
                    place=place,
                    start_date=start_date,
                    end_date=end_date,
                    round_num=round_num,
                    note=note
                )

                # Add Attendance records with 'ت دوري'
                start = datetime.strptime(start_date, "%Y-%m-%d").date()
                end = datetime.strptime(end_date, "%Y-%m-%d").date()
                delta = end - start

                for i in range(delta.days + 1):
                    day = start + timedelta(days=i)
                    Attendance.objects.update_or_create(
                        employee=employee,
                        date=day,
                        defaults={
                            'state': 'ت دوري',
                            'note': note
                        }
                    )
            
            messages.success(request, "تمت عملية إضافة التدريب الدوري وتحديث سجل الحضور.")
        except Exception as e:
            messages.error(request, f"حدث خطأ أثناء الحفظ: {str(e)}")
            
        return redirect('insert_periodic_training')

    employees = Employee.objects.all().order_by('sort_number')
    training_types = PeriodicTraining.objects.all().order_by('name')
    places = Places.objects.all().order_by('name')

    context = {
        'employees': employees,
        'training_types': training_types,
        'places': places
    }
    return render(request, 'training/insert_periodic.html', context)

@login_required(login_url='/login/')
def periodic_training_by_employee(request):
    """Grid view of periodic training by employee with date filtering."""
    # Default to Jan 1st of current year
    default_date = datetime(datetime.now().year, 1, 1).date()
    filter_date_str = request.GET.get('start_date')
    
    if filter_date_str:
        try:
            filter_date = datetime.strptime(filter_date_str, '%Y-%m-%d').date()
        except ValueError:
            filter_date = default_date
    else:
        filter_date = default_date

    employees = Employee.objects.all().order_by('sort_number')
    # Filter records that cover the period FROM the selected date
    periodic_records = EmPeriodicTraining.objects.filter(
        end_date__gte=filter_date
    ).select_related('employee', 'training_type', 'place').order_by('employee__sort_number', 'start_date')

    employee_periodic = defaultdict(list)
    for record in periodic_records:
        employee_periodic[record.employee].append(record)

    # Ensure slot filling for grid display
    for employee in employees:
        while len(employee_periodic[employee]) < 15:
            employee_periodic[employee].append(None)

    context = {
        'employee_periodic': {employee: employee_periodic[employee] for employee in employees},
        'selected_date': filter_date,
    }
    return render(request, 'training/periodic_by_employee.html', context)

@login_required(login_url='/login/')
def qualifying_training_by_employee(request):
    """Grid view of qualifying training by employee."""
    employees = Employee.objects.all().order_by('sort_number')
    qualifying_records = EmQualifyingTraining.objects.select_related('employee', 'training_type', 'place').order_by('employee__sort_number', 'start_date')

    employee_qualifying = defaultdict(list)
    for record in qualifying_records:
        employee_qualifying[record.employee].append(record)

    # Ensure slot filling for grid display
    for employee in employees:
        while len(employee_qualifying[employee]) < 15:
            employee_qualifying[employee].append(None)

    context = {
        'employee_qualifying': {employee: employee_qualifying[employee] for employee in employees},
    }
    return render(request, 'training/qualifying_by_employee.html', context)
