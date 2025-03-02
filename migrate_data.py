import os
import django
from django.db import connections
from datetime import datetime

# إعداد بيئة Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# استيراد النموذج الجديد فقط من تطبيق em_data
from em_data.models import Employee as NewEmployee

def migrate_data():
    # استخدام اتصال قاعدة em لجلب البيانات مباشرة
    with connections['em'].cursor() as cursor:
        cursor.execute("""
            SELECT id, id_number, date_of_birth, date_of_retirement, age, name, mainornot,
                   sort_number, dep_sort, image, amen_or_ola, rank_kind, nickname,
                   operation, police_number, insurance_number, date_of_edara, date_of_appointment,
                   phone_number, alt_phone_number, marital_status, gender, governorate, district,
                   address, health_status, tmamam, food, rahatcounter, total_leave, bus,
                   deleted_at, created_at, updated_at
            FROM employees
        """)
        rows = cursor.fetchall()

    for row in rows:
        # تعيين البيانات إلى النموذج الجديد مع تعيين institute_id إلى 1 افتراضيًا
        new_emp = NewEmployee(
            id=row[0],
            id_number=row[1],
            date_of_birth=row[2],
            date_of_retirement=row[3],
            age=row[4],
            name=row[5],
            mainornot=row[6],
            sort_number=row[7],
            dep_sort=row[8],
            image=row[9],
            amen_or_ola=row[10],
            rank_kind=row[11],
            nickname=row[12],
            operation=row[13],
            police_number=row[14],
            insurance_number=row[15],
            date_of_edara=row[16],
            date_of_appointment=row[17],
            phone_number=row[18],
            alt_phone_number=row[19],
            marital_status=row[20],
            gender=row[21],
            governorate=row[22],
            district=row[23],
            address=row[24],
            health_status=row[25],
            tmamam=row[26],
            food=row[27],
            rahatcounter=row[28],
            total_leave=row[29],
            bus=row[30],
            deleted_at=row[31],
            created_at=row[32],
            updated_at=row[33],
            institute_id=1  # تعيين قيمة افتراضية 1 لـ institute_id
        )
        new_emp.save(using='default')  # استخدام 'default' لأن yasser معرفة كـ default
        print(f"تم نقل الموظف: {new_emp.name}")

    # تقرير عما تم نقله وما تبقى
    print("\n=== تقرير النقل ===")
    print("الأعمدة التي تم نقلها:")
    transferred_fields = [
        'id', 'id_number', 'date_of_birth', 'date_of_retirement', 'age', 'name', 'mainornot',
        'sort_number', 'dep_sort', 'image', 'amen_or_ola', 'rank_kind', 'nickname',
        'operation', 'police_number', 'insurance_number', 'date_of_edara', 'date_of_appointment',
        'phone_number', 'alt_phone_number', 'marital_status', 'gender', 'governorate', 'district',
        'address', 'health_status', 'tmamam', 'food', 'rahatcounter', 'total_leave', 'bus',
        'deleted_at', 'created_at', 'updated_at', 'institute_id (بقيمة افتراضية 1)'
    ]
    for field in transferred_fields:
        print(f"- {field}")

    print("\nالأعمدة التي لم يتم نقلها:")
    omitted_fields = ['rank', 'department', 'nots']
    for field in omitted_fields:
        print(f"- {field} ({'جديد' if field == 'nots' else 'تم تجاهله أو يتطلب تحويل إلى ForeignKey'})")

if __name__ == "__main__":
    migrate_data()