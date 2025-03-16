from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from collections import defaultdict
import json
from .models import Employee, TrainingTeam, Places, EmTrainingTeams

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
    training_teams = dict(sorted(training_teams.items(), key=lambda x: len(x[1]), reverse=True))

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

    training_teams = TrainingTeam.objects.all()
    employees = Employee.objects.all()

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
        result = request.POST.get('result', 'ناجح')
        round_num = request.POST.get('round_num')
        if round_num == '':
            round_num = None

        for emp_id in employees:
            employee = Employee.objects.get(id=emp_id)
            EmTrainingTeams.objects.create(
                employee=employee,
                name=employee.name,  # اسم الموظف كـ Training Name
                training_team=training_team,
                place=place,
                start_date=start_date,
                end_date=end_date,
                result=result,
                round_num=round_num
            )

        messages.success(request, "تمت إضافة التدريب بنجاح!")
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
    employees = Employee.objects.all()
    return render(request, 'training/edit_training_record.html', {'employees': employees})

@login_required(login_url='/login/')
def get_employee_training_data(request, employee_id):
    """Fetch training data for a selected employee and return as JSON."""
    training_data = EmTrainingTeams.objects.filter(employee_id=employee_id).select_related('place', 'training_team').values(
        'id', 'employee__name', 'start_date', 'end_date', 'result', 'round_num', 'place_id', 'training_team_id'
    )
    
    places = list(Places.objects.values('id', 'name'))  # Fetch available places
    training_teams = list(TrainingTeam.objects.values('id', 'name'))  # Fetch available training teams
    
    return JsonResponse({
        "training_data": list(training_data),
        "places": places,
        "training_teams": training_teams
    })

@login_required(login_url='/login/')
@csrf_exempt
def update_training_record(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            training_record = EmTrainingTeams.objects.get(id=data['id'])
            
            training_record.start_date = data['start_date']
            training_record.end_date = data['end_date']
            training_record.result = data.get('result', '')
            training_record.round_num = data.get('round_num', None)
            training_record.place_id = data['place_id']
            training_record.training_team_id = data['training_team_id']
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
