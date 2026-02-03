# E:\yasser\emapi2025\myproject\secret_reports\views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from datetime import date
from .models import SecretReport
from em_data.models import Employee

# كلمة المرور الثابتة
PASSWORD_CODE = "323"


# 🟢 الصفحة الرئيسية
def index(request):
    return render(request, 'secret_reports/index.html')


# 🟡 تعديل الدرجات حسب الفرد
def edit_by_employee(request):
    employees = Employee.objects.all().order_by('sort_number')
    selected_employee = None
    reports = {}
    years = []

    employee_id = request.GET.get('employee_id')
    if employee_id:
        selected_employee = get_object_or_404(Employee, id=employee_id)
        start_year = selected_employee.date_of_appointment.year
        end_year = start_year + 60  # حتى سن المعاش
        years = list(range(start_year, end_year + 1))

        if request.method == 'POST':
            for year in years:
                score = request.POST.get(f'score_{year}')
                if score == '':
                    score = None  # لا تجعلها صفر
                SecretReport.objects.update_or_create(
                    employee=selected_employee,
                    year=year,
                    defaults={'score': score}
                )
            # البقاء على نفس الصفحة بعد الحفظ
            return redirect(f"{request.path}?employee_id={employee_id}")

        reports = {r.year: r.score for r in SecretReport.objects.filter(employee=selected_employee)}

    return render(request, 'secret_reports/edit_by_employee.html', {
        'employees': employees,
        'selected_employee': selected_employee,
        'reports': reports,
        'years': years,
    })


# 🟣 عرض درجات فرد (عرض فقط)
def view_by_employee(request):
    employees = Employee.objects.all().order_by('sort_number')
    selected_employee = None
    reports = {}
    years = []

    employee_id = request.GET.get('employee_id')
    if employee_id:
        selected_employee = get_object_or_404(Employee, id=employee_id)
        start_year = selected_employee.date_of_appointment.year
        current_year = date.today().year
        years = list(range(start_year, current_year + 1))
        reports = {r.year: r.score for r in SecretReport.objects.filter(employee=selected_employee)}

    return render(request, 'secret_reports/view_by_employee.html', {
        'employees': employees,
        'selected_employee': selected_employee,
        'reports': reports,
        'years': years,
    })


# 🔵 تعديل الدرجات حسب العام
def edit_by_year(request):
    employees = Employee.objects.all().order_by('sort_number')
    all_years = sorted(SecretReport.objects.values_list('year', flat=True).distinct())
    selected_year = request.GET.get('year')
    reports = {}

    if selected_year:
        selected_year = int(selected_year)
        reports = {r.employee_id: r.score for r in SecretReport.objects.filter(year=selected_year)}

        if request.method == 'POST':
            for emp in employees:
                score = request.POST.get(f'score_{emp.id}')
                if score == '':
                    score = None
                SecretReport.objects.update_or_create(
                    employee=emp,
                    year=selected_year,
                    defaults={'score': score}
                )
            # البقاء على نفس الصفحة بعد الحفظ
            return redirect(f"{request.path}?year={selected_year}")

    return render(request, 'secret_reports/edit_by_year.html', {
        'employees': employees,
        'all_years': all_years,
        'selected_year': selected_year,
        'reports': reports,
    })


# 🧩 واجهة AJAX للتحقق من كلمة المرور (لـ SweetAlert)
def check_password_ajax(request):
    password = request.GET.get('password')

    # لو المستخدم كتب الباسورد الصحيح
    if password == PASSWORD_CODE:
        request.session['secret_reports_authenticated'] = True
        return JsonResponse({'success': True})

    # لو فقط فحص هل الجلسة لا تزال فعالة
    if request.GET.get('check_only'):
        if request.session.get('secret_reports_authenticated'):
            return JsonResponse({'authenticated': True})
        else:
            return JsonResponse({'authenticated': False})

    return JsonResponse({'success': False})





from django.shortcuts import render
from openpyxl import Workbook
from django.http import HttpResponse
from datetime import date
from .models import SecretReport
from em_data.models import Employee


def chunk_list(lst, size):
    """تجزئة القائمة إلى مجموعات"""
    return [lst[i:i + size] for i in range(0, len(lst), size)]


def secrets_dfter(request):
    employees = Employee.objects.all().order_by('sort_number')
    data = []

    for emp in employees:
        reports = SecretReport.objects.filter(employee=emp).order_by('year')
        year_score_map = {r.year: r.score for r in reports}

        # 🔹 حساب بداية الخدمة ونهاية الخدمة
        start_year = emp.date_of_appointment.year if emp.date_of_appointment else None
        if emp.date_of_birth:
            end_year = emp.date_of_birth.year + 60
        else:
            end_year = date.today().year

        # 🔹 تحديد جميع الأعوام من التعيين إلى التقاعد
        if start_year:
            all_years = list(range(start_year, end_year + 1))
        else:
            all_years = sorted(year_score_map.keys())

        # 🔹 استبعاد أول عام فارغ إذا كان قبل 2024 ولا يحتوي على درجة
        if all_years:
            first_year = all_years[0]
            if first_year < 2024 and not year_score_map.get(first_year):
                all_years = [y for y in all_years if y > first_year]

        # 🔹 تقسيم الأعوام إلى مجموعات من 7
        years_chunks = chunk_list(all_years, 7)
        scores_chunks = [
            [year_score_map.get(y, '') for y in chunk]
            for chunk in years_chunks
        ]

        # 🔹 إكمال إلى 7 أزواج حتى لو أقل
        while len(years_chunks) < 7:
            years_chunks.append([""] * 7)
            scores_chunks.append([""] * 7)

        combined = list(zip(years_chunks, scores_chunks))
        data.append({'employee': emp, 'years_chunks': combined})

    # ===========================
    # 📤 تصدير إلى Excel
    # ===========================
    if 'export' in request.GET:
        wb = Workbook()
        ws = wb.active
        ws.title = "التقارير السرية"

        for i, entry in enumerate(data, start=1):
            emp = entry['employee']
            years_chunks = entry['years_chunks']

            # 🔹 صف العنوان الخاص بكل فرد
            ws.append(["م", "الدرجة", "رقم الشرطة", "الجهة الفرعية", "الاسم", "البيان"])

            # 🔹 أول مجموعة في نفس صف الاسم
            first_years, first_scores = years_chunks[0]
            ws.append([
                i,
                str(emp.rank) if emp.rank else '',
                emp.police_number or '',
                "إدارة موسيقات الشرطة",
                emp.name or '',
                "الأعوام",
            ] + first_years)
            ws.append(["", "", "", "", "", "الدرجات"] + first_scores)

            # 🔹 بقية المجموعات حتى 7 أزواج كاملة
            for years, scores in years_chunks[1:]:
                ws.append(["", "", "", "", "", "الأعوام"] + years)
                ws.append(["", "", "", "", "", "الدرجات"] + scores)

        # 📦 تجهيز الملف
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="secret_reports.xlsx"'
        wb.save(response)
        return response

    # ===========================
    # 🖥️ عرض HTML
    # ===========================
    return render(request, 'secret_reports/secrets_dfter.html', {'data': data})












