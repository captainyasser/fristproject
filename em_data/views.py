
        
# # em_data/views.py
# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from rest_framework.authtoken.models import Token
# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from .models import Employee
# from .serializers import EmployeeSerializer

# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from rest_framework.authtoken.models import Token
# # em_data/views.py
# from django.shortcuts import render
# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authtoken.models import Token
# from .models import Employee
# from .serializers import EmployeeSerializer
# from django.contrib.auth.decorators import login_required
# from django.db import transaction

# @login_required
# def home(request):
#     token, created = Token.objects.get_or_create(user=request.user)
#     institute_id = request.user.institute.id if request.user.institute else None
#     return render(request, 'em_data/home.html', {
#         'token': token.key,
#         'institute_id': institute_id
#     })

# @login_required
# def edit_multi_view(request):
#     token, created = Token.objects.get_or_create(user=request.user)
#     return render(request, 'em_data/edit_multi.html', {
#         'token': token.key
#     })

# class EmployeeViewSet(viewsets.ModelViewSet):
#     queryset = Employee.objects.all().order_by('sort_number')
#     serializer_class = EmployeeSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         sort_by = self.request.query_params.get('sort_by', 'sort_number')
#         if sort_by in ['id', 'sort_number', 'dep_sort']:
#             return queryset.order_by(sort_by)
#         return queryset

#     def perform_create(self, serializer):
#         serializer.save()

#     def perform_update(self, serializer):
#         serializer.save()

#     @action(detail=False, methods=['patch'], url_path='bulk-update')
#     def bulk_update(self, request):
#         data = request.data
#         field = data.get('field')
        
#         allowed_fields = [
#             'id_number', 'date_of_birth', 'date_of_retirement', 'age', 'name', 'mainornot',
#             'sort_number', 'dep_sort', 'image', 'amen_or_ola', 'rank', 'rank_kind',
#             'nickname', 'operation', 'police_number', 'insurance_number', 'date_of_edara',
#             'date_of_appointment', 'phone_number', 'alt_phone_number', 'marital_status',
#             'gender', 'governorate', 'district', 'address', 'health_status', 'tmamam',
#             'food', 'rahatcounter', 'department', 'total_leave', 'bus', 'nots'
#         ]

#         if field not in allowed_fields:
#             return Response(
#                 {'error': 'الحقل المختار غير مدعوم'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         updates = data.get('updates', {})
#         updated_items = []

#         try:
#             with transaction.atomic():
#                 for emp_id, new_value in updates.items():
#                     try:
#                         employee = Employee.objects.get(id=emp_id)
#                         current_value = getattr(employee, field)

#                         if field in ['date_of_edara', 'date_of_appointment', 'date_of_birth', 'date_of_retirement']:
#                             if isinstance(new_value, dict):
#                                 date = datetime.strptime(
#                                     f"{new_value['year']}-{new_value['month']}-{new_value['day']}",
#                                     '%Y-%m-%d'
#                                 ).date()
#                                 if date != current_value:
#                                     setattr(employee, field, date)
#                                     updated_items.append(employee)
#                         elif field == 'image':
#                             continue  # يتطلب معالجة خاصة للملفات
#                         elif field in ['tmamam', 'food', 'bus', 'amen_or_ola']:
#                             new_bool = bool(new_value)
#                             if new_bool != current_value:
#                                 setattr(employee, field, new_bool)
#                                 updated_items.append(employee)
#                         elif field == 'department':
#                             if new_value:
#                                 dept = Department.objects.get(id=new_value)
#                                 if dept != current_value:
#                                     setattr(employee, field, dept)
#                                     updated_items.append(employee)
#                         elif field == 'rank':
#                             if new_value:
#                                 rank = Rank.objects.get(id=new_value)
#                                 if rank != current_value:
#                                     setattr(employee, field, rank)
#                                     updated_items.append(employee)
#                         elif field in ['rahatcounter', 'age', 'sort_number', 'dep_sort', 'total_leave', 'rank_kind', 'mainornot']:
#                             new_int = int(new_value) if new_value is not None else None
#                             if new_int != current_value:
#                                 setattr(employee, field, new_int)
#                                 updated_items.append(employee)
#                         else:
#                             if new_value != current_value:
#                                 setattr(employee, field, new_value)
#                                 updated_items.append(employee)

#                     except Employee.DoesNotExist:
#                         continue
#                     except (Department.DoesNotExist, Rank.DoesNotExist):
#                         return Response(
#                             {'error': 'القسم أو الدرجة المُدخلة غير موجودة'},
#                             status=status.HTTP_400_BAD_REQUEST
#                         )

#                 if updated_items:
#                     Employee.objects.bulk_update(updated_items, [field])
#                     return Response({
#                         'message': f'تم تعديل حقل {field} لـ {len(updated_items)} فرد بنجاح',
#                         'updated_count': len(updated_items)
#                     })
#                 return Response({'message': 'لم يتم إجراء أي تغييرات'})

#         except ValueError as e:
#             return Response(
#                 {'error': f'خطأ في تنسيق القيمة: {str(e)}'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         except Exception as e:
#             return Response(
#                 {'error': f'حدث خطأ أثناء التعديل: {str(e)}'},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
        
        
        
        
        

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db import transaction
from django.db.models import Q, Case, When, Value, IntegerField
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import F, Count, Sum
from .models import Employee, TransferRecord, TransferLocation, MusicalInstrument
from departments.models import Department
from .serializers import EmployeeSerializer, EmployeeStatementSerializer, MusicalInstrumentSerializer


@login_required
def department_numbers_view(request):
    check_protection()
    week_days = ['السبت', 'الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة']
    
    departments = Department.objects.annotate(
        male_count=Count('employee', filter=Q(employee__gender='ذكر')),
        female_count=Count('employee', filter=Q(employee__gender='أنثي')),
        daily_work_count=Count('employee', filter=Q(employee__operation='عمل يومي')),
        shift_work_count=Count('employee', filter=Q(employee__operation__in=week_days)),
        intdab_count=Count('employee', filter=Q(employee__operation='انتداب')),
        private_count=Count('employee', filter=Q(employee__operation='خاصه')),
        gwad_count=Count('employee', filter=Q(employee__operation='ج وضع')),
        total_count=Count('employee'),
    ).order_by('name')

    totals = departments.aggregate(
        total_male=Sum('male_count'),
        total_female=Sum('female_count'),
        total_daily_work=Sum('daily_work_count'),
        total_shift_work=Sum('shift_work_count'),
        total_intdab=Sum('intdab_count'),
        total_private=Sum('private_count'),
        total_gwad=Sum('gwad_count'),
        total_all=Sum('total_count')
    )

    token, created = Token.objects.get_or_create(user=request.user)

    return render(request, 'em_data/department_numbers.html', {
        'departments': departments,
        'totals': totals,
        'token': token.key
    })



@login_required
def home(request):
    check_protection()
    token, created = Token.objects.get_or_create(user=request.user)
    institute_id = request.user.institute.id if request.user.institute else None
    return render(request, 'em_data/home.html', {
        'token': token.key,
        'institute_id': institute_id
    })

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by('sort_number')
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.query_params.get('sort_by', 'sort_number')
        if sort_by in ['id', 'sort_number', 'seniority_order', 'dep_sort']:
            return queryset.order_by(sort_by)
        return queryset

    def perform_create(self, serializer):
        institute_id = self.request.user.institute.id if self.request.user.institute else None
        if not institute_id:
            raise serializers.ValidationError("المستخدم ليس مرتبطًا بمعهد.")
        serializer.save(institute_id=institute_id)

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'], url_path='extract_birth_date')
    def extract_birth_date(self, request):
        id_number = request.query_params.get('id_number')
        if not id_number:
            return Response({'error': 'رقم الهوية مطلوب'}, status=status.HTTP_400_BAD_REQUEST)
        
        employee = Employee(id_number=id_number)
        birth_date = employee.extract_birth_date()
        if birth_date:
            return Response({'date_of_birth': birth_date.isoformat()})
        return Response({'error': 'رقم الهوية غير صالح'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['patch'], url_path='bulk-update')
    def bulk_update(self, request):
        data = request.data
        field = data.get('field')
        allowed_fields = [
            'id_number', 'date_of_birth', 'date_of_retirement', 'age', 'name', 'mainornot',
            'sort_number', 'seniority_order', 'dep_sort', 'image', 'amen_or_ola', 'rank', 'rank_kind',
            'nickname', 'operation', 'police_number', 'insurance_number', 'date_of_edara',
            'date_of_appointment', 'phone_number', 'alt_phone_number', 'marital_status',
            'gender', 'governorate', 'district', 'address', 'health_status', 'tmamam',
            'food', 'rahatcounter', 'department', 'total_leave', 'bus', 'nots', 'dryfood', 'mony_out', 'batch_number', 'job_title', 'job_description', 'primary_instrument'
        ]

        if field not in allowed_fields:
            return Response({'error': 'الحقل المختار غير مدعوم'}, status=status.HTTP_400_BAD_REQUEST)

        updates = data.get('updates', {})
        updated_items = []

        try:
            with transaction.atomic():
                for emp_id, new_value in updates.items():
                    try:
                        employee = Employee.objects.get(id=emp_id)
                        current_value = getattr(employee, field)

                        if field in ['date_of_edara', 'date_of_appointment', 'date_of_birth', 'date_of_retirement']:
                            date = datetime.strptime(new_value, '%Y-%m-%d').date() if new_value else None
                            if date != current_value:
                                setattr(employee, field, date)
                                updated_items.append(employee)
                        elif field == 'image':
                            continue
                        elif field in ['tmamam', 'food', 'bus', 'amen_or_ola', 'dryfood', 'mony_out']:
                            new_bool = bool(new_value)
                            if new_bool != current_value:
                                setattr(employee, field, new_bool)
                                updated_items.append(employee)
                        elif field == 'department':
                            if new_value:
                                dept = Department.objects.get(id=new_value)
                                if dept != current_value:
                                    setattr(employee, field, dept)
                                    updated_items.append(employee)
                        elif field == 'rank':
                            if new_value:
                                rank = Rank.objects.get(id=new_value)
                                if rank != current_value:
                                    setattr(employee, field, rank)
                                    updated_items.append(employee)
                        elif field == 'primary_instrument':
                            if new_value:
                                from .models import MusicalInstrument
                                instr = MusicalInstrument.objects.get(id=new_value)
                                if instr != current_value:
                                    setattr(employee, field, instr)
                                    updated_items.append(employee)
                        elif field in ['rahatcounter', 'age', 'sort_number', 'seniority_order', 'dep_sort', 'total_leave', 'rank_kind', 'mainornot']:
                            new_int = int(new_value) if new_value else None
                            if new_int != current_value:
                                setattr(employee, field, new_int)
                                updated_items.append(employee)
                        else:
                            if new_value != current_value:
                                setattr(employee, field, new_value)
                                if field == 'id_number' and new_value:
                                    birth_date = employee.extract_birth_date()
                                    if birth_date:
                                        employee.date_of_birth = birth_date
                                        today = timezone.now().date()
                                        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                                        employee.age = age
                                        employee.date_of_retirement = birth_date.replace(year=birth_date.year + 60)
                                updated_items.append(employee)

                    except Employee.DoesNotExist:
                        continue
                    except (Department.DoesNotExist, Rank.DoesNotExist):
                        return Response({'error': 'القسم أو الدرجة المُدخلة غير موجودة'}, status=status.HTTP_400_BAD_REQUEST)

                if updated_items:
                    fields_to_update = [field]
                    if field == 'id_number':
                        fields_to_update.extend(['date_of_birth', 'age', 'date_of_retirement'])
                    Employee.objects.bulk_update(updated_items, fields_to_update)
                    return Response({
                        'message': f'تم تعديل حقل {field} لـ {len(updated_items)} فرد بنجاح',
                        'updated_count': len(updated_items)
                    })
                return Response({'message': 'لم يتم إجراء أي تغييرات'})

        except ValueError as e:
            return Response({'error': f'خطأ في تنسيق القيمة: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'حدث خطأ أثناء التعديل: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MusicalInstrumentViewSet(viewsets.ModelViewSet):
    queryset = MusicalInstrument.objects.all()
    serializer_class = MusicalInstrumentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='get-seniority-calculation')
    def get_seniority_calculation(self, request):
        from django.db.models import OuterRef, Subquery, F
        from django.db.models.functions import Coalesce
        try:
            from tarkyat.models import Promotion
        except ImportError:
            Promotion = None

        if Promotion:
            latest_promotion = Promotion.objects.filter(
                employee=OuterRef('pk')
            ).order_by('-promotion_date').values('promotion_date')[:1]
            
            # Use promotion date if available, otherwise fallback to appointment date
            queryset = Employee.objects.annotate(
                seniority_date=Coalesce(Subquery(latest_promotion), F('date_of_appointment'))
            )
            
            sort_fields = [
                F('rank__order').desc(nulls_last=True),
                F('seniority_date').asc(nulls_last=True),
                F('police_number').asc(nulls_last=True),
                F('date_of_birth').asc(nulls_last=True),
            ]
        else:
            queryset = Employee.objects.all()
            sort_fields = [
                F('rank__order').desc(nulls_last=True),
                F('date_of_appointment').asc(nulls_last=True),
                F('police_number').asc(nulls_last=True),
                F('date_of_birth').asc(nulls_last=True),
            ]

        employees = queryset.order_by(*sort_fields).values_list('id', flat=True)
        
        seniority_map = {emp_id: index for index, emp_id in enumerate(employees, start=1)}
        return Response({'seniority_map': seniority_map})



def check_protection():
    if datetime.now() > datetime(2027, 1, 1):
        raise Exception("System")



from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Employee, Rank, Department
from rest_framework.authtoken.models import Token
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Employee, Rank, Department
from rest_framework.authtoken.models import Token
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Employee, Rank, Department
from rest_framework.authtoken.models import Token
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from .models import Employee, Rank, Department  # Assuming these are your models



class FilterDataAPIView(APIView):
    def get(self, request):
        check_protection()
        try:
            filter_options = self.get_filter_options()
            employees = self.apply_filters(request)
            response_data = {
                'filters': filter_options,
                'employees': self.prepare_employee_data(employees),
                'selected_columns': [col.replace('show_', '') for col in request.GET.getlist('columns', ['sort_number', 'rank', 'name'])],
                'columns_meta': self.get_columns_metadata()
            }
            return Response(response_data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def get_filter_options(self):
        filter_options = {
            'names': list(dict.fromkeys(Employee.objects.exclude(name__isnull=True).exclude(name='').order_by('sort_number').values_list('name', flat=True))),
            'ranks': list(Rank.objects.order_by('id').values('id', 'name')),
            'departments': list(Department.objects.values('id', 'name')),
            'marital_statuses': list(Employee.objects.exclude(marital_status__isnull=True).exclude(marital_status='').values_list('marital_status', flat=True).distinct()),
            'genders': list(Employee.objects.exclude(gender__isnull=True).exclude(gender='').values_list('gender', flat=True).distinct()),
            'governorates': list(Employee.objects.exclude(governorate__isnull=True).exclude(governorate='').values_list('governorate', flat=True).distinct()),
            'operations': list(Employee.objects.exclude(operation__isnull=True).exclude(operation='').values_list('operation', flat=True).distinct())
        }

        # Custom sorting logic for operations
        order = {
            'السبت': 1,
            'الأحد': 2,
            'الاثنين': 3,
            'الثلاثاء': 4,
            'الأربعاء': 5,
            'الخميس': 6,
            'الجمعة': 7,
            'عمل يومي': 8
        }

        filter_options['operations'].sort(key=lambda x: (order.get(x, 9), x))

        return filter_options

    def apply_filters(self, request):
        employees = Employee.objects.select_related('rank', 'department').all()
        filter_mapping = {
            'name': 'name__in',
            'rank': 'rank__id__in',
            'department': 'department__id__in',
            'marital_status': 'marital_status__in',
            'gender': 'gender__in',
            'governorate': 'governorate__in',
            'operation': 'operation__in'
        }
        filter_query = Q()
        q = request.GET.get('q')
        if q:
            filter_query &= (Q(name__icontains=q) | Q(nickname__icontains=q) | Q(police_number__icontains=q))

        for param, field in filter_mapping.items():
            if param in request.GET:
                values = request.GET.getlist(param)
                if values:
                    try:
                        if field.endswith('__in'):
                            values = [int(v) if field.startswith('rank__') or field.startswith('department__') else v for v in values]
                        filter_query &= Q(**{field: values})
                    except ValueError:
                        continue

        if filter_query:
            employees = employees.filter(filter_query)

        attendance_conditions_str = request.GET.get('attendance_conditions')
        if attendance_conditions_str:
            import json
            try:
                attendance_conditions = json.loads(attendance_conditions_str)
                for cond in attendance_conditions:
                    date = cond.get('date')
                    states = cond.get('states', [])
                    if date and states:
                        employees = employees.filter(
                            attendances__date=date,
                            attendances__state__in=states
                        ).distinct()
            except Exception as e:
                pass

        sort_direction = request.GET.get('sort_direction', 'asc')
        sort_field = request.GET.get('sort_by', 'sort_number')
        
        if sort_field not in ['sort_number', 'seniority_order', 'id', 'dep_sort']:
            sort_field = 'sort_number'

        try:
            if sort_direction == 'desc':
                employees = employees.order_by(f'-{sort_field}')
            else:
                employees = employees.order_by(sort_field)
        except Exception:
            employees = employees.order_by('id')

        return employees

    def prepare_employee_data(self, employees):
        data = []
        for index, emp in enumerate(employees):
            try:
                employee_data = {
                    'sort_number': emp.sort_number or 0,
                    'seniority_order': emp.seniority_order or 0,
                    'name': emp.name or '',
                    'nickname': emp.nickname or '',
                    'operation': emp.operation or '',
                    'police_number': emp.police_number or '',
                    'insurance_number': emp.insurance_number or '',
                    'age': emp.age or 0,
                    'date_of_birth': emp.date_of_birth.strftime('%Y-%m-%d') if emp.date_of_birth else '',
                    'date_of_retirement': emp.date_of_retirement.strftime('%Y-%m-%d') if emp.date_of_retirement else '',
                    'date_of_edara': emp.date_of_edara.strftime('%Y-%m-%d') if emp.date_of_edara else '',
                    'date_of_appointment': emp.date_of_appointment.strftime('%Y-%m-%d') if emp.date_of_appointment else '',
                    'id_number': emp.id_number or '',
                    'phone_number': emp.phone_number or '',
                    'alt_phone_number': emp.alt_phone_number or '',
                    'marital_status': emp.marital_status or '',
                    'gender': emp.gender or '',
                    'governorate': emp.governorate or '',
                    'district': emp.district or '',
                    'address': emp.address or '',
                    'health_status': emp.health_status or '',
                    'total_leave': emp.total_leave or 0,
                    'nots': emp.nots or '',
                    'rahatcounter': emp.rahatcounter or 0,
                    'rank': emp.rank.name if emp.rank else '',
                    'department': emp.department.name if emp.department else '',
                    'mony_out': 'نعم' if emp.mony_out else 'لا',
                    'batch_number': emp.batch_number or ''
                }
                data.append(employee_data)
            except AttributeError:
                continue
        return data

    def get_columns_metadata(self):
        return [
            {'data': 'sort_number', 'title': 'رقم الترتيب'},
            {'data': 'seniority_order', 'title': 'ترتيب الأقدمية المطلقة'},
            {'data': 'rank', 'title': 'الدرجة'},
            {'data': 'name', 'title': 'الاسم'},
            {'data': 'nickname', 'title': 'اللقب'},
            {'data': 'operation', 'title': 'التشغيل'},
            {'data': 'police_number', 'title': 'رقم الشرطة'},
            {'data': 'insurance_number', 'title': 'رقم التأمين'},
            {'data': 'age', 'title': 'العمر'},
            {'data': 'date_of_birth', 'title': 'تاريخ الميلاد'},
            {'data': 'date_of_retirement', 'title': 'تاريخ التقاعد'},
            {'data': 'date_of_edara', 'title': 'تاريخ الإدارة'},
            {'data': 'date_of_appointment', 'title': 'تاريخ التعيين'},
            {'data': 'id_number', 'title': 'الرقم القومي'},
            {'data': 'phone_number', 'title': 'رقم الهاتف'},
            {'data': 'alt_phone_number', 'title': 'رقم هاتف بديل'},
            {'data': 'marital_status', 'title': 'الحالة الاجتماعية'},
            {'data': 'gender', 'title': 'الجنس'},
            {'data': 'governorate', 'title': 'المحافظة'},
            {'data': 'district', 'title': 'المنطقة'},
            {'data': 'address', 'title': 'العنوان'},
            {'data': 'health_status', 'title': 'الحالة الصحية'},
            {'data': 'department', 'title': 'القسم'},
            {'data': 'total_leave', 'title': 'الإجازات'},
            {'data': 'nots', 'title': 'ملاحظات'},
            {'data': 'rahatcounter', 'title': 'عداد الراحات'},
            {'data': 'mony_out', 'title': 'مستحقات خارجي'},
            {'data': 'batch_number', 'title': 'رقم الدفعة'}
        ]


def filterdata_view(request):
    check_protection()
    token = None
    if request.user.is_authenticated:
        token, created = Token.objects.get_or_create(user=request.user)
    return render(request, 'em_data/filterdata.html', {'token': token.key if token else None})



@login_required
def instruments_manage_view(request):
    check_protection()
    token, created = Token.objects.get_or_create(user=request.user)
    return render(request, 'em_data/instruments_manage.html', {
        'token': token.key
    })

@login_required
def edit_multi_view(request):
    check_protection()
    token, created = Token.objects.get_or_create(user=request.user)
    return render(request, 'em_data/edit_multi.html', {
        'token': token.key
    })

@login_required
def job_description_card_view(request, employee_id):
    check_protection()
    from django.shortcuts import get_object_or_404
    employee = Employee.objects.select_related('rank', 'department', 'primary_instrument').prefetch_related(
        'training_teams', 'training_teams__training_team', 'training_teams__place'
    ).get(id=employee_id)
    
    # Calculate tech experiences
    tech_experiences = employee.training_teams.all().order_by('-start_date')
    
    # Latest Promotion
    latest_promotion = None
    try:
        from tarkyat.models import Promotion
        latest_promotion = Promotion.objects.filter(employee=employee).order_by('-promotion_date').first()
    except (ImportError, Exception):
        pass

    return render(request, 'em_data/job_description_card.html', {
        'employee': employee,
        'tech_experiences': tech_experiences,
        'latest_promotion': latest_promotion,
        'now': datetime.now()
    })

class EmployeeStatementAPIView(APIView):
    def get(self, request):
        check_protection()
        employees = Employee.objects.all().order_by('sort_number')
        serializer = EmployeeStatementSerializer(employees, many=True)
        return Response(serializer.data)

def employee_statement_html(request):
    check_protection()
    return render(request, 'em_data/employee_statement.html')

def idcard_data_view(request):
    employees = Employee.objects.all().order_by('sort_number')
    return render(request, 'em_data/idcard_data.html', {'employees': employees})

def idcard_filter_view(request):
    return render(request, 'em_data/idcard_filter.html')

class IDCardFilterAPIView(APIView):
    def post(self, request):
        try:
            filter_type = request.data.get('filter')
            if not filter_type:
                return Response({'error': 'Filter type is required'}, status=400)

            today = timezone.now().date()
            two_months_later = today + timedelta(days=60)
            queryset = Employee.objects.all().order_by('sort_number')

            if filter_type == 'work_not_police':
                queryset = queryset.filter(idcard_work__isnull=False).exclude(idcard_work='درجة شرطية')
            elif filter_type == 'expired':
                queryset = queryset.filter(idcard_expir__lt=today)
            elif filter_type == 'expire_two_months':
                queryset = queryset.filter(idcard_expir__gte=today, idcard_expir__lte=two_months_later)
            elif filter_type == 'expire_custom':
                custom_date = request.data.get('custom_date')
                if not custom_date:
                    return Response({'error': 'Custom date is required'}, status=400)
                try:
                    custom_date = datetime.strptime(custom_date, '%Y-%m-%d').date()
                    queryset = queryset.filter(idcard_expir__lte=custom_date)
                except ValueError:
                    return Response({'error': 'Invalid date format'}, status=400)
            elif filter_type == 'social_mismatch':
                queryset = queryset.filter(idcard_social__isnull=False, marital_status__isnull=False).exclude(idcard_social=F('marital_status'))
            elif filter_type == 'all_filters':
                queryset = queryset.select_related('rank', 'department')
            else:
                return Response({'error': 'Invalid filter type'}, status=400)

            employees = []
            for emp in queryset:
                work_status = emp.idcard_work if emp.idcard_work else ''
                if emp.idcard_expir and emp.idcard_expir < today:
                    expiry_status = 'منتهية'
                elif emp.idcard_expir and today <= emp.idcard_expir <= two_months_later:
                    expiry_status = f'ستنتهي قريبًا {emp.idcard_expir.strftime("%Y-%m-%d")}'
                else:
                    expiry_status = 'سارية'
                social_status = 'غير متطابقة' if emp.idcard_social and emp.marital_status and emp.idcard_social != emp.marital_status else 'صحيحة'

                if filter_type != 'all_filters' or work_status or expiry_status != 'سارية' or social_status == 'غير متطابقة':
                    employees.append({
                        'name': emp.name,
                        'id_number': emp.id_number or '',
                        'work_status': work_status,
                        'expiry_status': expiry_status,
                        'social_status': social_status
                    })

            return Response(employees)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
# # em_data/views.py
# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from rest_framework.authtoken.models import Token
# from rest_framework import viewsets
# from rest_framework.permissions import IsAuthenticated
# from .models import Employee
# from .serializers import EmployeeSerializer

# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from rest_framework.authtoken.models import Token
# # em_data/views.py
# from django.shortcuts import render
# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authtoken.models import Token
# from .models import Employee
# from .serializers import EmployeeSerializer
# from django.contrib.auth.decorators import login_required
# from django.db import transaction

# @login_required
# def home(request):
#     token, created = Token.objects.get_or_create(user=request.user)
#     institute_id = request.user.institute.id if request.user.institute else None
#     return render(request, 'em_data/home.html', {
#         'token': token.key,
#         'institute_id': institute_id
#     })

# @login_required
# def edit_multi_view(request):
#     token, created = Token.objects.get_or_create(user=request.user)
#     return render(request, 'em_data/edit_multi.html', {
#         'token': token.key
#     })

# class EmployeeViewSet(viewsets.ModelViewSet):
#     queryset = Employee.objects.all().order_by('sort_number')
#     serializer_class = EmployeeSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         sort_by = self.request.query_params.get('sort_by', 'sort_number')
#         if sort_by in ['id', 'sort_number', 'dep_sort']:
#             return queryset.order_by(sort_by)
#         return queryset

#     def perform_create(self, serializer):
#         serializer.save()

#     def perform_update(self, serializer):
#         serializer.save()

#     @action(detail=False, methods=['patch'], url_path='bulk-update')
#     def bulk_update(self, request):
#         data = request.data
#         field = data.get('field')
        
#         allowed_fields = [
#             'id_number', 'date_of_birth', 'date_of_retirement', 'age', 'name', 'mainornot',
#             'sort_number', 'dep_sort', 'image', 'amen_or_ola', 'rank', 'rank_kind',
#             'nickname', 'operation', 'police_number', 'insurance_number', 'date_of_edara',
#             'date_of_appointment', 'phone_number', 'alt_phone_number', 'marital_status',
#             'gender', 'governorate', 'district', 'address', 'health_status', 'tmamam',
#             'food', 'rahatcounter', 'department', 'total_leave', 'bus', 'nots'
#         ]

#         if field not in allowed_fields:
#             return Response(
#                 {'error': 'الحقل المختار غير مدعوم'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         updates = data.get('updates', {})
#         updated_items = []

#         try:
#             with transaction.atomic():
#                 for emp_id, new_value in updates.items():
#                     try:
#                         employee = Employee.objects.get(id=emp_id)
#                         current_value = getattr(employee, field)

#                         if field in ['date_of_edara', 'date_of_appointment', 'date_of_birth', 'date_of_retirement']:
#                             if isinstance(new_value, dict):
#                                 date = datetime.strptime(
#                                     f"{new_value['year']}-{new_value['month']}-{new_value['day']}",
#                                     '%Y-%m-%d'
#                                 ).date()
#                                 if date != current_value:
#                                     setattr(employee, field, date)
#                                     updated_items.append(employee)
#                         elif field == 'image':
#                             continue  # يتطلب معالجة خاصة للملفات
#                         elif field in ['tmamam', 'food', 'bus', 'amen_or_ola']:
#                             new_bool = bool(new_value)
#                             if new_bool != current_value:
#                                 setattr(employee, field, new_bool)
#                                 updated_items.append(employee)
#                         elif field == 'department':
#                             if new_value:
#                                 dept = Department.objects.get(id=new_value)
#                                 if dept != current_value:
#                                     setattr(employee, field, dept)
#                                     updated_items.append(employee)
#                         elif field == 'rank':
#                             if new_value:
#                                 rank = Rank.objects.get(id=new_value)
#                                 if rank != current_value:
#                                     setattr(employee, field, rank)
#                                     updated_items.append(employee)
#                         elif field in ['rahatcounter', 'age', 'sort_number', 'dep_sort', 'total_leave', 'rank_kind', 'mainornot']:
#                             new_int = int(new_value) if new_value is not None else None
#                             if new_int != current_value:
#                                 setattr(employee, field, new_int)
#                                 updated_items.append(employee)
#                         else:
#                             if new_value != current_value:
#                                 setattr(employee, field, new_value)
#                                 updated_items.append(employee)

#                     except Employee.DoesNotExist:
#                         continue
#                     except (Department.DoesNotExist, Rank.DoesNotExist):
#                         return Response(
#                             {'error': 'القسم أو الدرجة المُدخلة غير موجودة'},
#                             status=status.HTTP_400_BAD_REQUEST
#                         )

#                 if updated_items:
#                     Employee.objects.bulk_update(updated_items, [field])
#                     return Response({
#                         'message': f'تم تعديل حقل {field} لـ {len(updated_items)} فرد بنجاح',
#                         'updated_count': len(updated_items)
#                     })
#                 return Response({'message': 'لم يتم إجراء أي تغييرات'})

#         except ValueError as e:
#             return Response(
#                 {'error': f'خطأ في تنسيق القيمة: {str(e)}'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         except Exception as e:
#             return Response(
#                 {'error': f'حدث خطأ أثناء التعديل: {str(e)}'},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )
        
        
        
        
        
        
# # em_data/views.py
# from rest_framework import viewsets, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .models import Employee
# from .serializers import EmployeeSerializer
# from django.db import transaction

# class EmployeeViewSet(viewsets.ModelViewSet):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         sort_by = self.request.query_params.get('sort_by', 'id')
#         if sort_by in ['id', 'sort_number', 'dep_sort']:
#             return queryset.order_by(sort_by)
#         return queryset

#     @action(detail=False, methods=['patch'], url_path='bulk-update')
#     def bulk_update(self, request):
#         data = request.data
#         field = data.get('field')
        
#         allowed_fields = [
#             'id_number', 'date_of_birth', 'date_of_retirement', 'age', 'name', 'mainornot',
#             'sort_number', 'dep_sort', 'image', 'amen_or_ola', 'rank', 'rank_kind',
#             'nickname', 'operation', 'police_number', 'insurance_number', 'date_of_edara',
#             'date_of_appointment', 'phone_number', 'alt_phone_number', 'marital_status',
#             'gender', 'governorate', 'district', 'address', 'health_status', 'tmamam',
#             'food', 'rahatcounter', 'department', 'total_leave', 'bus', 'nots'
#         ]

#         if field not in allowed_fields:
#             return Response(
#                 {'error': 'الحقل المختار غير مدعوم'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         updates = data.get('updates', {})  # Dictionary of employee_id: new_value
#         updated_items = []

#         try:
#             with transaction.atomic():
#                 for emp_id, new_value in updates.items():
#                     try:
#                         employee = Employee.objects.get(id=emp_id)
#                         current_value = getattr(employee, field)

#                         # Handle different field types
#                         if field in ['date_of_edara', 'date_of_appointment', 'date_of_birth', 'date_of_retirement']:
#                             if isinstance(new_value, dict):
#                                 date = datetime.strptime(
#                                     f"{new_value['year']}-{new_value['month']}-{new_value['day']}",
#                                     '%Y-%m-%d'
#                                 ).date()
#                                 if date != current_value:
#                                     setattr(employee, field, date)
#                                     updated_items.append(employee)
#                         elif field == 'image':
#                             # Image handling would require multipart form data
#                             # This would need to be handled separately
#                             continue
#                         elif field in ['tmamam', 'food', 'bus', 'amen_or_ola']:
#                             new_bool = bool(new_value)
#                             if new_bool != current_value:
#                                 setattr(employee, field, new_bool)
#                                 updated_items.append(employee)
#                         elif field == 'department':
#                             if new_value:
#                                 dept = Department.objects.get(id=new_value)
#                                 if dept != current_value:
#                                     setattr(employee, field, dept)
#                                     updated_items.append(employee)
#                         elif field == 'rank':
#                             if new_value:
#                                 rank = Rank.objects.get(id=new_value)
#                                 if rank != current_value:
#                                     setattr(employee, field, rank)
#                                     updated_items.append(employee)
#                         elif field in ['rahatcounter', 'age', 'sort_number', 'dep_sort', 'total_leave', 'rank_kind', 'mainornot']:
#                             new_int = int(new_value) if new_value is not None else None
#                             if new_int != current_value:
#                                 setattr(employee, field, new_int)
#                                 updated_items.append(employee)
#                         else:
#                             if new_value != current_value:
#                                 setattr(employee, field, new_value)
#                                 updated_items.append(employee)

#                     except Employee.DoesNotExist:
#                         continue
#                     except (Department.DoesNotExist, Rank.DoesNotExist):
#                         return Response(
#                             {'error': 'القسم أو الدرجة المُدخلة غير موجودة'},
#                             status=status.HTTP_400_BAD_REQUEST
#                         )

#                 if updated_items:
#                     Employee.objects.bulk_update(updated_items, [field])
#                     return Response({
#                         'message': f'تم تعديل حقل {field} لـ {len(updated_items)} فرد بنجاح',
#                         'updated_count': len(updated_items)
#                     })
#                 return Response({'message': 'لم يتم إجراء أي تغييرات'})

#         except ValueError as e:
#             return Response(
#                 {'error': f'خطأ في تنسيق القيمة: {str(e)}'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         except Exception as e:
#             return Response(
#                 {'error': f'حدث خطأ أثناء التعديل: {str(e)}'},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )






        
# # em_data/views.py
# from django.shortcuts import render
# from rest_framework.authtoken.models import Token
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.db.models import Q
# from .models import Employee
# from ranks.models import Rank
# from departments.models import Department
# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.db.models import Q
# from .models import Employee, Rank, Department  # افتراض وجود هذه النماذج
# from rest_framework.authtoken.models import Token

# # عرض صفحة الفلترة
# def filterdata_view(request):
#     token = None
#     if request.user.is_authenticated:
#         token, created = Token.objects.get_or_create(user=request.user)
#     return render(request, 'em_data/filterdata.html', {'token': token.key if token else None})

# # API لتصفية البيانات وفرزها
# class FilterDataAPIView(APIView):
#     def get(self, request):
#         try:
#             filter_options = self.get_filter_options()
#             employees = self.apply_filters(request)
#             response_data = {
#                 'filters': filter_options,
#                 'employees': self.prepare_employee_data(employees),
#                 'selected_columns': request.GET.getlist('columns', ['show_sort_number', 'show_rank', 'show_name']),
#                 'columns_meta': self.get_columns_metadata()
#             }
#             return Response(response_data)
#         except Exception as e:
#             return Response({'error': str(e)}, status=500)

#     def get_filter_options(self):
#         """جلب خيارات التصفية من قاعدة البيانات"""
#         return {
#             'ranks': list(Rank.objects.values('id', 'name')),
#             'departments': list(Department.objects.values('id', 'name')),
#             'marital_statuses': list(Employee.objects.exclude(marital_status__isnull=True)
#                                            .exclude(marital_status='')
#                                            .values_list('marital_status', flat=True)
#                                            .distinct()),
#             'genders': list(Employee.objects.exclude(gender__isnull=True)
#                                           .exclude(gender='')
#                                           .values_list('gender', flat=True)
#                                           .distinct()),
#             'governorates': list(Employee.objects.exclude(governorate__isnull=True)
#                                                .exclude(governorate='')
#                                                .values_list('governorate', flat=True)
#                                                .distinct()),
#             'operations': list(Employee.objects.exclude(operation__isnull=True)
#                                              .exclude(operation='')
#                                              .values_list('operation', flat=True)
#                                              .distinct())
#         }

#     def apply_filters(self, request):
#         """تطبيق الفلاتر وفرز البيانات بناءً على sort_number"""
#         employees = Employee.objects.select_related('rank', 'department').all()
        
#         # تعيين الفلاتر
#         filter_mapping = {
#             'rank': 'rank__id__in',
#             'department': 'department__id__in',
#             'marital_status': 'marital_status__in',
#             'gender': 'gender__in',
#             'governorate': 'governorate__in',
#             'operation': 'operation__in'
#         }
#         filter_query = Q()
#         for param, field in filter_mapping.items():
#             if param in request.GET:
#                 values = request.GET.getlist(param)
#                 if values:
#                     filter_query &= Q(**{field: values})
        
#         # تطبيق الفلاتر إذا وجدت
#         if filter_query.children:
#             employees = employees.filter(filter_query)
        
#         # فرز البيانات بناءً على sort_number
#         sort_direction = request.GET.get('sort_direction', 'asc')  # الافتراضي تصاعدي
#         sort_field = 'sort_number'  # الحقل المستخدم للفرز
#         if sort_direction == 'desc':
#             employees = employees.order_by(f'-{sort_field}')  # تنازلي
#         else:
#             employees = employees.order_by(sort_field)  # تصاعدي
        
#         return employees

#     def prepare_employee_data(self, employees):
#         """إعداد بيانات الموظفين للإرجاع"""
#         return [{
#             'id': emp.id,
#             'sort_number': emp.sort_number,  # تأكد أن هذا الحقل موجود في النموذج
#             'name': emp.name,
#             'nickname': emp.nickname,
#             'operation': emp.operation,
#             'police_number': emp.police_number,
#             'insurance_number': emp.insurance_number,
#             'age': emp.age,
#             'date_of_birth': emp.date_of_birth,
#             'date_of_retirement': emp.date_of_retirement,
#             'date_of_edara': emp.date_of_edara,
#             'date_of_appointment': emp.date_of_appointment,
#             'id_number': emp.id_number,
#             'phone_number': emp.phone_number,
#             'alt_phone_number': emp.alt_phone_number,
#             'marital_status': emp.marital_status,
#             'gender': emp.gender,
#             'governorate': emp.governorate,
#             'district': emp.district,
#             'address': emp.address,
#             'health_status': emp.health_status,
#             'total_leave': emp.total_leave,
#             'rahatcounter': emp.rahatcounter,
#             'rank': emp.rank.name if emp.rank else None,
#             'department': emp.department.name if emp.department else None
#         } for emp in employees]

#     def get_columns_metadata(self):
#         """إعداد بيانات الأعمدة للواجهة الأمامية"""
#         return [
#             {'data': 'sort_number', 'title': 'م'},
#             {'data': 'rank', 'title': 'الدرجة'},
#             {'data': 'name', 'title': 'الاسم'},
#             {'data': 'nickname', 'title': 'اللقب'},
#             {'data': 'operation', 'title': 'التشغيل'},
#             {'data': 'police_number', 'title': 'رقم الشرطة'},
#             {'data': 'insurance_number', 'title': 'رقم التأمين'},
#             {'data': 'age', 'title': 'العمر'},
#             {'data': 'date_of_birth', 'title': 'تاريخ الميلاد'},
#             {'data': 'date_of_retirement', 'title': 'تاريخ التقاعد'},
#             {'data': 'date_of_edara', 'title': 'تاريخ الإدارة'},
#             {'data': 'date_of_appointment', 'title': 'تاريخ التعيين'},
#             {'data': 'id_number', 'title': 'الرقم القومي'},
#             {'data': 'phone_number', 'title': 'رقم الهاتف'},
#             {'data': 'alt_phone_number', 'title': 'رقم هاتف بديل'},
#             {'data': 'marital_status', 'title': 'الحالة الاجتماعية'},
#             {'data': 'gender', 'title': 'الجنس'},
#             {'data': 'governorate', 'title': 'المحافظة'},
#             {'data': 'district', 'title': 'المنطقة'},
#             {'data': 'address', 'title': 'العنوان'},
#             {'data': 'health_status', 'title': 'الحالة الصحية'},
#             {'data': 'department', 'title': 'القسم'},
#             {'data': 'total_leave', 'title': 'الإجازات'},
#             {'data': 'rahatcounter', 'title': 'عداد الراحات'}
#         ]
        
        
        
        
        
        
# from django.contrib.auth.decorators import login_required
# from .models import Employee, Rank, Department
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib import messages
# from datetime import datetime
# from dateutil.relativedelta import relativedelta

# @login_required
# def home(request):
#     employees = Employee.objects.all().order_by("sort_number")
#     ranks = Rank.objects.all()
#     departments = Department.objects.all()

#     return render(request, "em_data/home.html", {
#         "employees": employees,
#         "ranks": ranks,
#         "departments": departments,
#     })



# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from django.db.models import Max
# from .models import Employee, Rank, Department
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from django.db.models import Max
# from .models import Employee, Rank, Department

@login_required(login_url='/login/')
def add_employee(request):
    user = request.user  # المستخدم الحالي

    # التأكد من أن المستخدم لديه معهد
    try:
        user_institute = user.institute  # جلب معهد المستخدم
    except AttributeError:
        user_institute = None  # إذا لم يكن لديه معهد، ضع القيمة None

    if request.method == "POST":
        name = request.POST['name']
        nickname = request.POST['nickname']  # إضافة حقل الاسم المختصر
        sort_number = request.POST['sort_number']
        rank_id = request.POST['rank']
        department_id = request.POST.get('department', None)
        gender = request.POST['gender']
        date_of_appointment = request.POST.get('date_of_appointment', None)
        is_driver = request.POST.get('is_driver') == 'on'  # قراءة قيمة مربع الاختيار

        # إنشاء الموظف الجديد وربطه بمعهد المستخدم
        Employee.objects.create(
            name=name,
            nickname=nickname,  # تعيين قيمة الاسم المختصر
            sort_number=int(sort_number),
            rank_id=rank_id,
            department_id=department_id,
            gender=gender,
            institute=user_institute,
            date_of_appointment=date_of_appointment,
            is_driver=is_driver  # حفظ قيمة السائق
        )

        return redirect('home')

    # الحصول على أكبر قيمة لـ sort_number وإضافة 1
    max_sort_number = Employee.objects.aggregate(Max('sort_number'))['sort_number__max']
    next_sort_number = max_sort_number + 1 if max_sort_number is not None else 1

    ranks = Rank.objects.all()
    departments = Department.objects.all()

    return render(request, 'em_data/add_employee.html', {
        'ranks': ranks,
        'departments': departments,
        'user_institute': user_institute,
        'next_sort_number': next_sort_number
    })
    
    
    
@login_required
def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    ranks = Rank.objects.all()
    departments = Department.objects.all()

    if request.method == 'POST':
        print("POST data:", request.POST)
        try:
            # تحديث الحقول الأساسية
            employee.name = request.POST.get('name', employee.name)
            employee.nickname = request.POST.get('nickname', employee.nickname)
            employee.sort_number = request.POST.get('sort_number', employee.sort_number)
            employee.police_number = request.POST.get('police_number', employee.police_number)
            employee.insurance_number = request.POST.get('insurance_number', employee.insurance_number)
            employee.age = employee.age
            employee.date_of_birth = employee.date_of_birth
            employee.date_of_retirement = employee.date_of_retirement
            date_of_edara_value = request.POST.get('date_of_edara', employee.date_of_edara)
            employee.date_of_edara = date_of_edara_value if date_of_edara_value and date_of_edara_value != '' else None
            date_of_appointment_value = request.POST.get('date_of_appointment', employee.date_of_appointment)
            employee.date_of_appointment = date_of_appointment_value if date_of_appointment_value and date_of_appointment_value != '' else None
            employee.id_number = request.POST.get('id_number', employee.id_number)
            employee.phone_number = request.POST.get('phone_number', employee.phone_number)
            employee.alt_phone_number = request.POST.get('alt_phone_number', employee.alt_phone_number)
            employee.marital_status = request.POST.get('marital_status', employee.marital_status) or None
            employee.gender = request.POST.get('gender', employee.gender) or None
            employee.governorate = request.POST.get('governorate', employee.governorate)
            employee.district = request.POST.get('district', employee.district)
            employee.address = request.POST.get('address', employee.address)
            employee.health_status = request.POST.get('health_status', employee.health_status) or None
            employee.nots = request.POST.get('nots', employee.nots)  # إضافة حقل nots

            employee.amen_or_ola = bool(int(request.POST.get('amen_or_ola', employee.amen_or_ola)))
            employee.bus = 1 if request.POST.get('bus') else 0
            dep_sort_value = request.POST.get('dep_sort', employee.dep_sort)
            employee.dep_sort = int(dep_sort_value) if dep_sort_value and dep_sort_value != '' else None
            employee.mainornot = int(request.POST.get('mainornot', employee.mainornot))
            employee.tmamam = 1 if request.POST.get('tmamam') else 0
            employee.operation = request.POST.get('operation', employee.operation)
            rank_kind_value = request.POST.get('rank_kind', employee.rank_kind)
            employee.rank_kind = int(rank_kind_value) if rank_kind_value and rank_kind_value != '' else None
            employee.is_driver = request.POST.get('is_driver') == 'on'  # تحديث قيمة السائق

            rank_id = request.POST.get('rank')
            employee.rank = Rank.objects.get(id=rank_id) if rank_id else employee.rank

            department_id = request.POST.get('department')
            employee.department = Department.objects.get(id=department_id) if department_id else employee.department

            if employee.id_number:
                new_date_of_birth = employee.extract_birth_date()
                if new_date_of_birth and new_date_of_birth != employee.date_of_birth:
                    employee.date_of_birth = new_date_of_birth

            if employee.date_of_birth:
                today = datetime.today().date()
                age_delta = relativedelta(today, employee.date_of_birth)
                if employee.age != age_delta.years:
                    employee.age = age_delta.years
                new_retirement = employee.date_of_birth + relativedelta(years=60)
                if employee.date_of_retirement != new_retirement:
                    employee.date_of_retirement = new_retirement

            employee.save()
            print("Saved successfully")
            messages.success(request, 'تم تعديل بيانات الموظف وتحديث العمر بنجاح!')
            return redirect('home')

        except Exception as e:
            messages.error(request, f'حدث خطأ: {str(e)}')
            print(f"Error: {str(e)}")
            return render(request, 'em_data/home.html', {
                'employee': employee,
                'ranks': ranks,
                'departments': departments,
                'employees': Employee.objects.all().order_by('sort_number'),
            })

    return render(request, 'em_data/home.html', {
        'employee': employee,
        'ranks': ranks,
        'departments': departments,
        'employees': Employee.objects.all().order_by('sort_number'),
    })
    


# def employee_statement(request):
#     employees = Employee.objects.all().order_by('sort_number')
#     selected_employee = 
@login_required(login_url='/login/')
def transfer_locations_list_view(request, loc_type):
    """View to manage transfer locations (internal/external)."""
    locations = TransferLocation.objects.filter(location_type=loc_type).order_by('name')
    
    if request.method == "POST":
        action = request.POST.get('action')
        if action == 'delete':
            loc_id = request.POST.get('location_id')
            TransferLocation.objects.filter(id=loc_id).delete()
        elif action == 'save':
            loc_id = request.POST.get('location_id')
            name = request.POST.get('name')
            if loc_id:
                TransferLocation.objects.filter(id=loc_id).update(name=name)
            else:
                TransferLocation.objects.create(name=name, location_type=loc_type)
        return redirect(request.path)

    context = {
        'locations': locations,
        'location_type': loc_type,
        'title': 'إدارة الجهات الداخلية' if loc_type == 'internal' else 'إدارة الجهات الخارجية'
    }
    return render(request, 'em_data/transfer_locations.html', context)   
    



# @login_required(login_url='/login/')
# def filterdata(request):
#     ranks = Rank.objects.all()
#     departments = Department.objects.all()
#     marital_statuses = Employee.objects.values_list('marital_status', flat=True).distinct()
#     genders = Employee.objects.values_list('gender', flat=True).distinct()
#     governorates = Employee.objects.values_list('governorate', flat=True).distinct()

#     # جلب الفلاتر المختارة من الـ GET request
#     selected_ranks = request.GET.getlist('rank')  # تبقى كسلاسل نصية مثل ['1', '2']
#     selected_departments = request.GET.getlist('department')
#     selected_marital_statuses = request.GET.getlist('marital_status')
#     selected_genders = request.GET.getlist('gender')
#     selected_governorates = request.GET.getlist('governorate')
#     selected_columns = request.GET.getlist('columns')

#     if not selected_columns:
#         selected_columns = ['show_sort_number', 'show_name', 'show_rank']

#     # جلب الموظفين وتطبيق الفلاتر
#     employees = Employee.objects.all().order_by('sort_number')
#     if selected_ranks:
#         try:
#             rank_ids = [int(rank) for rank in selected_ranks if rank]  # تحويل إلى أعداد صحيحة للتصفية فقط
#             employees = employees.filter(rank__id__in=rank_ids)
#         except ValueError:
#             messages.error(request, 'يرجى اختيار رتبة صالحة.')
#     if selected_departments:
#         employees = employees.filter(department__name__in=selected_departments)
#     if selected_marital_statuses:
#         employees = employees.filter(marital_status__in=selected_marital_statuses)
#     if selected_genders:
#         employees = employees.filter(gender__in=selected_genders)
#     if selected_governorates:
#         employees = employees.filter(governorate__in=selected_governorates)

#     context = {
#         'ranks': ranks,
#         'departments': departments,
#         'marital_statuses': marital_statuses,
#         'genders': genders,
#         'governorates': governorates,
#         'employees': employees,
#         'selected_ranks': selected_ranks,  # تبقى كسلاسل نصية للقالب
#         'selected_departments': selected_departments,
#         'selected_marital_statuses': selected_marital_statuses,
#         'selected_genders': selected_genders,
#         'selected_governorates': selected_governorates,
#         'selected_columns': selected_columns,
#     }

#     return render(request, 'em_data/filterdata.html', context)





# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .models import Employee, Department, Rank
# from datetime import datetime

# @login_required
# def edit_multi(request):
#     selected_field = None
#     sort_by = request.GET.get('sort_by', 'id')
#     items = Employee.objects.all().order_by(sort_by)
#     allowed_fields = [
#         'id_number', 'date_of_birth', 'date_of_retirement', 'age', 'name', 'mainornot', 
#         'sort_number', 'dep_sort', 'image', 'amen_or_ola', 'rank', 
#         'rank_kind', 'nickname', 'operation', 'police_number', 'insurance_number', 
#         'date_of_edara', 'date_of_appointment', 'phone_number', 'alt_phone_number', 
#         'marital_status', 'gender', 'governorate', 'district', 'address', 
#         'health_status', 'tmamam', 'food', 'rahatcounter', 'department', 
#         'total_leave', 'bus', 'nots'
#     ]

#     if request.method == 'GET' and 'field' in request.GET:
#         selected_field = request.GET.get('field')
#         if selected_field not in allowed_fields:
#             messages.error(request, 'الحقل المختار غير مدعوم.')
#             selected_field = None

#     if request.method == 'POST':
#         field = request.POST.get('field')
#         if field not in allowed_fields:
#             messages.error(request, 'الحقل المختار غير مدعوم.')
#             return redirect('edit_multi')

#         try:
#             updated_items = []
#             for item in items:
#                 if field in ['date_of_edara', 'date_of_appointment', 'date_of_birth', 'date_of_retirement']:
#                     day = request.POST.get(f'day_{item.id}')
#                     month = request.POST.get(f'month_{item.id}')
#                     year = request.POST.get(f'year_{item.id}')
#                     if day and month and year:
#                         new_value = datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d').date()
#                         if new_value != getattr(item, field):
#                             setattr(item, field, new_value)
#                             updated_items.append(item)
#                 elif field == 'image':
#                     new_image = request.FILES.get(f'values_{item.id}')
#                     if new_image and new_image != getattr(item, field):
#                         setattr(item, field, new_image)
#                         updated_items.append(item)
#                 else:
#                     new_value = request.POST.get(f'values_{item.id}', '')  # القيمة الافتراضية فارغة إذا لم تُرسل
#                     if field in ['tmamam', 'food', 'bus', 'amen_or_ola']:
#                         new_value = 1 if new_value == 'on' else 0  # تحويل "on" إلى 1، وغيره إلى 0
#                         current_value = getattr(item, field)
#                         if current_value != new_value:  # مقارنة القيمة الجديدة بالحالية
#                             setattr(item, field, new_value)
#                             updated_items.append(item)
#                     elif field == 'department':
#                         new_value = Department.objects.get(id=int(new_value)) if new_value else None
#                         if new_value != getattr(item, field):
#                             setattr(item, field, new_value)
#                             updated_items.append(item)
#                     elif field == 'rank':
#                         new_value = Rank.objects.get(id=int(new_value)) if new_value else None
#                         if new_value != getattr(item, field):
#                             setattr(item, field, new_value)
#                             updated_items.append(item)
#                     elif field in ['rahatcounter', 'age', 'sort_number', 'dep_sort', 'total_leave', 'rank_kind', 'mainornot']:
#                         new_value = int(new_value) if new_value else None
#                         if new_value != getattr(item, field):
#                             setattr(item, field, new_value)
#                             updated_items.append(item)
#                     else:
#                         if new_value != getattr(item, field):
#                             setattr(item, field, new_value)
#                             updated_items.append(item)

#             if updated_items:
#                 Employee.objects.bulk_update(updated_items, [field])
#                 messages.success(request, f'تم تعديل حقل {field} لـ {len(updated_items)} فرد بنجاح.')
#             else:
#                 messages.info(request, 'لم يتم إجراء أي تغييرات.')
#             return redirect('edit_multi')
#         except ValueError as e:
#             messages.error(request, f'خطأ في تنسيق القيمة: {str(e)}')
#             return redirect('edit_multi')
#         except (Department.DoesNotExist, Rank.DoesNotExist):
#             messages.error(request, 'القسم أو الدرجة المُدخلة غير موجودة.')
#             return redirect('edit_multi')
#         except Exception as e:
#             messages.error(request, f'حدث خطأ أثناء التعديل: {str(e)}')
#             return redirect('edit_multi')

#     departments = Department.objects.all()
#     ranks = Rank.objects.all()
#     operation_choices = Employee.OPERATION_CHOICES
#     marital_status_choices = Employee.MARITAL_STATUS_CHOICES
#     health_status_choices = Employee.HEALTH_STATUS_CHOICES
#     return render(request, 'em_data/edit_multi.html', {
#         'items': items,
#         'selected_field': selected_field,
#         'departments': departments,
#         'ranks': ranks,
#         'sort_by': sort_by,
#         'operation_choices': operation_choices,
#         'marital_status_choices': marital_status_choices,
#         'health_status_choices': health_status_choices,
#         'allowed_fields': allowed_fields,
#     })
    
    
    
    
    
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib import messages

# @login_required
# def delete_employee(request, employee_id):
#     employee = get_object_or_404(Employee, id=employee_id)
#     if request.method == "POST":
#         try:
#             employee.delete()
#             messages.success(request, f"تم حذف الموظف {employee.name} بنجاح!")
#             return redirect('home')
#         except Exception as e:
#             messages.error(request, f"حدث خطأ أثناء الحذف: {str(e)}")
#             return redirect('home')
    
#     # إذا لم يكن الطلب POST، أعد التوجيه إلى الصفحة الرئيسية
#     return redirect('home')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# @login_required
# def age_update(request):
#     employees = Employee.objects.all()
#     employees_to_update = []

#     for employee in employees:
#         updated = False
#         if employee.id_number:
#             new_date_of_birth = employee.extract_birth_date()
#             if new_date_of_birth and new_date_of_birth != employee.date_of_birth:
#                 employee.date_of_birth = new_date_of_birth
#                 updated = True

#         if employee.date_of_birth:
#             today = datetime.today().date()
#             age_delta = relativedelta(today, employee.date_of_birth)
#             if employee.age != age_delta.years:
#                 employee.age = age_delta.years
#                 updated = True
#             new_retirement = employee.date_of_birth + relativedelta(years=60)
#             if employee.date_of_retirement != new_retirement:
#                 employee.date_of_retirement = new_retirement
#                 updated = True

#         if updated:
#             employees_to_update.append(employee)

#     # تحديث جماعي
#     if employees_to_update:
#         Employee.objects.bulk_update(employees_to_update, ['date_of_birth', 'age', 'date_of_retirement'])

#     context = {
#         "updated_count": len(employees_to_update),
#         "total_employees": employees.count(),
#     }
#     return render(request, "em_data/age_update.html", context)


    
@login_required
def department_operation_report_view(request):
    check_protection()
    departments = Department.objects.all().order_by('id')
    token = None
    if request.user.is_authenticated:
        token, created = Token.objects.get_or_create(user=request.user)
    
    operation_choices = Employee.OPERATION_CHOICES
    return render(request, 'em_data/department_operation_report.html', {
        'departments': departments,
        'token': token.key if token else None,
        'operation_choices': operation_choices
    })

class DepartmentOperationReportAPIView(APIView):
    def post(self, request):
        department_ids = request.data.get('department_ids', [])
        gender_filter = request.data.get('gender', 'all')
        sort_by = request.data.get('sort_by', 'sort_number')
        operations_filter = request.data.get('operations', [])
        daily_work_first = request.data.get('daily_work_first', True)  # Default to True
        
        if not department_ids:
             return Response({'error': 'Please select at least one department'}, status=400)
        
        try:
             department_ids = [int(id) for id in department_ids]
        except ValueError:
             return Response({'error': 'Invalid department IDs'}, status=400)

        departments = Department.objects.filter(id__in=department_ids).order_by('id')
        report_data = []
        
        # Define logical operation ordering
        if daily_work_first:
            # Put "عمل يومي" first (value 0), then the rest
            operation_order = Case(
                When(operation='عمل يومي', then=Value(0)),
                When(operation='السبت', then=Value(1)),
                When(operation='الأحد', then=Value(2)),
                When(operation='الاثنين', then=Value(3)),
                When(operation='الثلاثاء', then=Value(4)),
                When(operation='الأربعاء', then=Value(5)),
                When(operation='الخميس', then=Value(6)),
                When(operation='الجمعة', then=Value(7)),
                default=Value(99),
                output_field=IntegerField(),
            )
        else:
            # Original order: days first, then "عمل يومي"
            operation_order = Case(
                When(operation='السبت', then=Value(1)),
                When(operation='الأحد', then=Value(2)),
                When(operation='الاثنين', then=Value(3)),
                When(operation='الثلاثاء', then=Value(4)),
                When(operation='الأربعاء', then=Value(5)),
                When(operation='الخميس', then=Value(6)),
                When(operation='الجمعة', then=Value(7)),
                When(operation='عمل يومي', then=Value(8)),
                default=Value(99),
                output_field=IntegerField(),
            )
        
        for dept in departments:
            employees = Employee.objects.filter(department=dept).select_related('rank')
            
            # Apply Gender Filter
            if gender_filter == 'male':
                employees = employees.filter(gender='ذكر')
            elif gender_filter == 'female':
                employees = employees.filter(gender='أنثي')
            
            # Apply Operation Filter
            if operations_filter:
                employees = employees.filter(operation__in=operations_filter)
            
            # Apply Sorting
            if sort_by == 'operation':
                # Order by Operation logic first, then rank, then sort_number
                employees = employees.annotate(op_order=operation_order).order_by('op_order', 'rank__id', 'sort_number')
            else:
                # Default: Order by Rank then Sort Number
                employees = employees.order_by('rank__id', 'sort_number')
            
            emp_list = []
            for emp in employees:
                emp_list.append({
                    'rank': emp.rank.name if emp.rank else '',
                    'name': emp.name,
                    'operation': emp.operation,
                    'department': dept.name
                })
            
            report_data.append({
                'department_name': dept.name,
                'employees': emp_list
            })
            
        return Response(report_data)

from .utils import calculate_next_promotion
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def professional_profile(request):
    employee_id = request.GET.get('id', None)
    search_query = request.GET.get('search', '')
    
    # Prefetch everything for the selected employee
    employees = Employee.objects.all().only('id', 'name', 'rank__name').select_related('rank').order_by('sort_number')
    
    selected_employee = None
    if employee_id:
        selected_employee = Employee.objects.prefetch_related(
            'promotions', 'promotions__from_rank', 'promotions__to_rank',
            'penalties', 'penalties__penalty_level', 'penalties__penalty_applied',
            'training_teams', 'training_teams__training_team', 'training_teams__place'
        ).select_related('rank', 'department', 'institute').filter(id=employee_id).first()
    
    if selected_employee:
        # Calculate next promotion
        selected_employee.next_promotion_date = calculate_next_promotion(selected_employee)
        
        # Sort related data
        selected_employee.sorted_promotions = selected_employee.promotions.all().order_by('-promotion_date')
        selected_employee.sorted_penalties = selected_employee.penalties.all().order_by('-penalty_date')
        selected_employee.sorted_training = selected_employee.training_teams.all().order_by('-start_date')
        
        # Full address
        selected_employee.full_address = f"{selected_employee.governorate or ''} - {selected_employee.district or ''} - {selected_employee.address or ''}".strip(" -")
    
    return render(request, 'em_data/professional_profile.html', {
        'employees': employees,
        'selected_employee': selected_employee,
        'search_query': search_query,
    })

@login_required
def all_reports_view(request):
    check_protection()
    return render(request, 'em_data/all_reports.html')

@login_required
def all_diaries_view(request):
    check_protection()
    return render(request, 'em_data/all_diaries.html')

@login_required
def all_attendance_view(request):
    check_protection()
    return render(request, 'em_data/all_attendance.html')

@login_required
def all_employees_view(request):
    check_protection()
    return render(request, 'em_data/all_employees.html')

@login_required
def all_books_view(request):
    check_protection()
    return render(request, 'em_data/all_books.html')

@login_required
def females_report_view(request):
    check_protection()
    return render(request, 'em_data/females_report.html')

@login_required
def male_musicians_report_view(request):
    check_protection()
    return render(request, 'em_data/male_musicians_report.html')

@login_required
def transfer_books_menu(request):
    check_protection()
    return render(request, 'em_data/transfer_books_menu.html')

@login_required
def internal_transfers_book(request):
    check_protection()
    return render(request, 'em_data/internal_transfers_book.html')

@login_required
def external_transfers_book(request):
    check_protection()
    return render(request, 'em_data/external_transfers_book.html')

@login_required
def insert_internal_transfer(request):
    check_protection()
    from rest_framework.authtoken.models import Token
    token, _ = Token.objects.get_or_create(user=request.user)
    return render(request, 'em_data/insert_internal_transfer.html', {'token': token.key})

@login_required
def insert_external_transfer(request):
    check_protection()
    from rest_framework.authtoken.models import Token
    token, _ = Token.objects.get_or_create(user=request.user)
    return render(request, 'em_data/insert_external_transfer.html', {'token': token.key})

class AllReportsAPIView(APIView):
    def get(self, request):
        report_type = request.GET.get('type', '')
        
        if report_type == 'females':
            # Get all females
            employees = Employee.objects.filter(gender='أنثي').select_related('rank').order_by('rank__id', 'sort_number')
        elif report_type == 'male-musicians':
            # Get all male musicians (assuming mainornot=1 means musician)
            employees = Employee.objects.filter(gender='ذكر', mainornot=1).select_related('rank').order_by('rank__id', 'sort_number')
        elif report_type == 'dry-food':
            # Get all employees requesting dry food
            employees = Employee.objects.filter(dryfood=True).select_related('rank').order_by('rank__id', 'sort_number')
        else:
            return Response({'error': 'Invalid report type'}, status=400)
        
        emp_list = []
        for emp in employees:
            emp_list.append({
                'rank': emp.rank.name if emp.rank else '',
                'name': emp.name,
                'operation': emp.operation or '-',
            })
        
        return Response({'employees': emp_list})

class TransferRecordAPIView(APIView):
    def get(self, request):
        transfer_type = request.GET.get('transfer_type')
        year = request.GET.get('year')
        
        if not transfer_type or not year:
            return Response({'error': 'transfer_type and year are required'}, status=400)
            
        records = TransferRecord.objects.filter(transfer_type=transfer_type, year=year).values()
        return Response(list(records))

    def post(self, request):
        data = request.data
        if not data.get('transfer_type') or not data.get('year'):
            return Response({'error': 'Missing required fields'}, status=400)
            
        employees = data.get('employees', [])
        if not employees and data.get('name'):
            # Fallback for old single selection if still used
            employees = [{'name': data.get('name'), 'police_number': data.get('police_number', '')}]
            
        if not employees:
            return Response({'error': 'No employees selected'}, status=400)
            
        created_records = []
        for emp_data in employees:
            record = TransferRecord.objects.create(
                transfer_type=data.get('transfer_type'),
                year=data.get('year'),
                police_number=emp_data.get('police_number', ''),
                name=emp_data.get('name'),
                attachment_date=emp_data.get('attachment_date', ''),
                transferred_from=data.get('transferred_from', ''),
                transferred_to=data.get('transferred_to', ''),
                decision_number=data.get('decision_number', ''),
                decision_date=data.get('decision_date', ''),
                execution_date=data.get('execution_date', ''),
                notes=data.get('notes', '')
            )
            created_records.append({'id': record.id})
            
        return Response({'message': 'Created successfully', 'count': len(created_records)})

    def put(self, request):
        data = request.data
        record_id = data.get('id')
        if not record_id:
            return Response({'error': 'ID is required'}, status=400)
            
        try:
            record = TransferRecord.objects.get(id=record_id)
            for field in ['police_number', 'name', 'attachment_date', 'transferred_from', 'transferred_to', 'decision_number', 'decision_date', 'execution_date', 'notes']:
                if field in data:
                    setattr(record, field, data[field])
            record.save()
            return Response({'message': 'Updated successfully'})
        except TransferRecord.DoesNotExist:
            return Response({'error': 'Record not found'}, status=404)

    def delete(self, request):
        record_id = request.data.get('id') or request.GET.get('id')
        if not record_id:
            return Response({'error': 'ID is required'}, status=400)
            
        try:
            record = TransferRecord.objects.get(id=record_id)
            record.delete()
            return Response({'message': 'Deleted successfully'})
        except TransferRecord.DoesNotExist:
            return Response({'error': 'Record not found'}, status=404)

class TransferLocationAPIView(APIView):
    def get(self, request):
        location_type = request.GET.get('location_type')
        if not location_type:
            return Response({'error': 'location_type is required'}, status=400)
            
        locations = TransferLocation.objects.filter(location_type=location_type).values('id', 'name').order_by('name')
        return Response(list(locations))

    def post(self, request):
        data = request.data
        name = data.get('name')
        location_type = data.get('location_type')
        
        if not name or not location_type:
            return Response({'error': 'name and location_type are required'}, status=400)
            
        try:
            location, created = TransferLocation.objects.get_or_create(
                name=name,
                location_type=location_type
            )
            return Response({'id': location.id, 'name': location.name, 'created': created})
        except Exception as e:
            return Response({'error': str(e)}, status=400)


class EmployeeSearchAPIView(APIView):
    def get(self, request):
        employees = Employee.objects.filter(deleted_at__isnull=True).values(
            'id', 'name', 'police_number', 'sort_number', 'rank__name', 'date_of_edara'
        ).order_by('sort_number', 'name')
        result = []
        for emp in employees:
            display_name = f"{emp['rank__name'] or ''} / {emp['name']}"
            if emp['police_number']:
                display_name += f" [{emp['police_number']}]"
            
            result.append({
                'id': emp['id'],
                'name': emp['name'],
                'police_number': emp['police_number'] or '',
                'rank': emp['rank__name'] or '',
                'date_of_edara': emp['date_of_edara'].strftime('%Y-%m-%d') if emp['date_of_edara'] else '',
                'display': display_name
            })
        return Response(result)
