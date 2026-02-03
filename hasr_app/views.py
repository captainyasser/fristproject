from django.shortcuts import render, get_object_or_404
from datetime import date
from dateutil.relativedelta import relativedelta

from em_data.models import Employee


def pad_list(lst, min_length):
    """إكمال القائمة بعدد أسطر ثابت"""
    return list(lst) + [None] * max(0, min_length - len(lst))


# =========================
# صفحة اختيار الموظف
# =========================
def hasr_select_employee_view(request):
    employees = (
        Employee.objects
        .only('id', 'nickname', 'police_number')
        .order_by('sort_number', 'id')
    )

    return render(request, 'hasr_app/select_employee.html', {
        'employees': employees
    })


# =========================
# صفحة دفتر الحصر
# =========================
def hasr_sheet_view(request, employee_id):
    employee = get_object_or_404(
        Employee.objects
        .select_related('rank', 'department', 'institute')
        .prefetch_related(
            'educations',
            'promotions__to_rank',
            'training_teams__training_team',
            'elawat',
            'special_leaves'
        ),
        id=employee_id
    )

    # قائمة الموظفين (للتنقل السريع إن أحببت)
    all_employees = (
        Employee.objects
        .values('id', 'nickname', 'police_number')
        .order_by('nickname')
    )

    # =========================
    # تاريخ الإحالة للمعاش
    # =========================
    retirement_date = None
    if employee.date_of_birth:
        retirement_date = employee.date_of_birth + relativedelta(years=60)

    # =========================
    # الرتبة
    # =========================
    rank_name = employee.rank.name if employee.rank else ""

    # =========================
    # محل الميلاد / الإقامة
    # =========================
    birth_place = ""  # غير موجود صراحة بالموديل
    residence_parts = [
        employee.governorate,
        employee.district,
        employee.address
    ]
    residence_str = " - ".join(filter(None, residence_parts))

    # =========================
    # الحالة الاجتماعية
    # =========================
    marital_status = employee.marital_status or ""
    children_count = ""  # غير موجود حاليًا

    # =========================
    # الفرق / الدورات التدريبية (10 أسطر)
    # =========================
    training_teams_raw = [
        t.training_team.name
        for t in employee.training_teams.all()
        if t.training_team
    ]
    training_teams = pad_list(training_teams_raw, 10)

    # =========================
    # الترقيات (7 أسطر)
    # =========================
    promotions_list = list(
        employee.promotions.all().order_by('promotion_date')
    )
    promotions = pad_list(promotions_list, 7)

    # =========================
    # العلاوات (7 أسطر)
    # =========================
    elawat_list = list(
        employee.elawat.all().order_by('elawa_date')
    )
    elawat = pad_list(elawat_list, 7)

    # =========================
    # الإجازات الخاصة (سطرين)
    # =========================
    special_leaves_list = list(
        employee.special_leaves.all().order_by('start_date')
    )
    special_leaves = pad_list(special_leaves_list, 2)

    # =========================
    # جداول بدون أسطر
    # =========================
    disciplinary = []
    peacekeeping = []
    hajj = []

    # =========================
    # جداول بسطرين فارغين
    # =========================
    honors = pad_list([], 2)
    prev_work = pad_list([], 2)

    # =========================
    # Context
    # =========================
    context = {
        'employee': employee,
        'all_employees': all_employees,
        'retirement_date': retirement_date,
        'rank_name': rank_name,
        'birth_place': birth_place,
        'residence_str': residence_str,
        'marital_status': marital_status,
        'children_count': children_count,
        'training_teams': training_teams,
        'promotions': promotions,
        'elawat': elawat,
        'special_leaves': special_leaves,
        'disciplinary': disciplinary,
        'peacekeeping': peacekeeping,
        'hajj': hajj,
        'honors': honors,
        'prev_work': prev_work,
    }

    return render(request, 'hasr_app/hasr_sheet.html', context)
