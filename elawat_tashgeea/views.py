from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Employee, ElawaRecord, NominationRecord
from .forms import ElawaBatchForm, ElawaRecordForm, MultiElawaForm
from django.utils import timezone
from datetime import datetime
from tarkyat.models import Promotion
from secret_reports.models import SecretReport

def index(request):
    return render(request, "elawat_tashgeea/index.html")

def batch_create(request):
    if request.method == 'POST':
        form = ElawaBatchForm(request.POST)
        if form.is_valid():
            decision_number = form.cleaned_data.get('decision_number')
            elawa_date = form.cleaned_data['elawa_date']
            notes = form.cleaned_data.get('notes')
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




def add_multiple_elawat(request):
    selected_employee = None
    old_elawat = []
    
    # محاولة الحصول على الموظف من الـ POST أو الـ GET
    emp_id = request.POST.get("employee") or request.GET.get("employee_id")
    
    if emp_id:
        try:
            selected_employee = Employee.objects.get(id=emp_id)
            old_elawat = ElawaRecord.objects.filter(employee=selected_employee).order_by("-elawa_date")
        except (Employee.DoesNotExist, ValueError):
            pass

    if request.method == "POST":
        # إذا لم يكن المستخدم يضغط فقط على زر "عرض العلاوات القديمة"
        if "load_old" not in request.POST:
            if not selected_employee:
                messages.error(request, "يرجى اختيار موظف أولاً.")
            else:
                try:
                    count = int(request.POST.get("count", "0"))
                except ValueError:
                    count = 0
                    
                saved_any = False
                for i in range(1, count + 1):
                    decision_number = request.POST.get(f"decision_number_{i}")
                    elawa_date = request.POST.get(f"elawa_date_{i}")
                    notes = request.POST.get(f"notes_{i}")

                    if elawa_date:
                        ElawaRecord.objects.create(
                            employee=selected_employee,
                            decision_number=decision_number,
                            elawa_date=elawa_date,
                            notes=notes
                        )
                        saved_any = True
                
                if saved_any:
                    messages.success(request, "✓ تم حفظ العلاوات الجديدة بنجاح")
                    # نعود لنفس الصفحة مع بقاء اسم الموظف مختاراً
                    return redirect(f"{request.path}?employee_id={selected_employee.id}")

    form = MultiElawaForm(initial={"employee": emp_id} if emp_id else None)
    return render(request, "elawat_tashgeea/add_multiple_elawat.html", {
        "form": form,
        "selected_employee": selected_employee,
        "old_elawat": old_elawat,
    })


def nominate_employees(request):
    current_year = datetime.now().year
    year_str = request.GET.get('year')
    
    try:
        year = int(year_str) if year_str else current_year
    except ValueError:
        year = current_year

    if request.method == "POST":
        selected_ids = request.POST.getlist('employee_ids')
        # مسح الترشيحات السابقة لهذا العام
        NominationRecord.objects.filter(year=year).delete()
        # إضافة المرشحين الجدد
        for emp_id in selected_ids:
            try:
                emp_id_int = int(emp_id)
                NominationRecord.objects.create(employee_id=emp_id_int, year=year)
            except (ValueError, TypeError):
                continue
                
        messages.success(request, f"✓ تم حفظ قائمة المرشحين لعام {year} بنجاح")
        return redirect(f"{request.path}?year={year}")

    employees = Employee.objects.filter(deleted_at__isnull=True).order_by('sort_number')
    nominated_ids = list(NominationRecord.objects.filter(year=year).values_list('employee_id', flat=True))
    
    # قائمة السنوات (5 سنوات قبل وبعد السنة الحالية)
    years_list = range(current_year - 5, current_year + 6)

    return render(request, "elawat_tashgeea/nominate_employees.html", {
        "employees": employees,
        "year": year,
        "nominated_ids": nominated_ids,
        "years_list": years_list
    })


def final_nomination_list(request):
    current_year = datetime.now().year
    nomination_year_str = request.GET.get('nomination_year')
    
    try:
        nomination_year = int(nomination_year_str) if nomination_year_str else current_year
    except ValueError:
        nomination_year = current_year

    report_year_1 = request.GET.get('report_year_1', str(nomination_year - 2))
    report_year_2 = request.GET.get('report_year_2', str(nomination_year - 1))

    try:
        ry1 = int(report_year_1)
        ry2 = int(report_year_2)
    except:
        ry1 = nomination_year - 2
        ry2 = nomination_year - 1

    sort_by = request.GET.get('sort_by', 'sort_number')
    if sort_by not in ['sort_number', 'seniority_order']:
        sort_by = 'sort_number'

    # جلب المرشحين لهذا العام
    nominations = NominationRecord.objects.filter(year=nomination_year).select_related(
        'employee', 'employee__rank', 'employee__department'
    ).order_by(f'employee__{sort_by}')
    
    data_list = []
    
    def get_rating(score):
        if score is None: return "-"
        if score >= 90: return "ممتاز"
        if score >= 85: return "جيد جدا"
        if score >= 75: return "جيد"
        if score >= 65: return "مقبول"
        return "ضعيف"

    # السنوات الـ 5 السابقة للعلاوات
    allowance_years = [nomination_year - i for i in range(1, 6)]

    for nom in nominations:
        emp = nom.employee
        
        # تاريخ آخر ترقية
        last_promotion = Promotion.objects.filter(employee=emp).order_by('-promotion_date').first()
        promotion_date = last_promotion.promotion_date if last_promotion else "-"
        
        # التقارير السرية
        rep1 = SecretReport.objects.filter(employee=emp, year=ry1).first()
        rep2 = SecretReport.objects.filter(employee=emp, year=ry2).first()
        
        # تفاصيل العلاوات السابقة (جميع السنوات التي حصل فيها على علاوة)
        all_prev_allws = ElawaRecord.objects.filter(employee=emp).order_by('elawa_date')
        all_years = [r.elawa_date.year for r in all_prev_allws]
        
        # نأخذ أول 5 سنوات (الأقدم) حصل فيها على العلاوة للعرض في الأعمدة الـ 5
        first_5_years = all_years[:5]
        while len(first_5_years) < 5:
            first_5_years.append("-") # إضافة شرطات في النهاية إذا كان العدد أقل من 5
            
        # إجمالي عدد العلاوات المسجلة
        total_allw_count = len(all_years)

        data_list.append({
            'emp': emp,
            'promotion_date': promotion_date,
            'report1': {'score': rep1.score if rep1 else "-", 'rating': get_rating(rep1.score) if rep1 else "-"},
            'report2': {'score': rep2.score if rep2 else "-", 'rating': get_rating(rep2.score) if rep2 else "-"},
            'prev_allw_details': first_5_years,
            'total_allw_count': total_allw_count,
        })

    years_list = range(current_year - 10, current_year + 5)

    return render(request, "elawat_tashgeea/final_nomination_list.html", {
        "data_list": data_list,
        "nomination_year": nomination_year,
        "ry1": ry1,
        "ry2": ry2,
        "years_list": years_list,
        "allowance_years": allowance_years,
        "sort_by": sort_by
    })

