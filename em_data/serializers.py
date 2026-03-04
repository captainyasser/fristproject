
from rest_framework import serializers
from .models import Employee
from ranks.models import Rank
from departments.models import Department
from datetime import datetime

class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = ['id', 'name']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

class EmployeeSerializer(serializers.ModelSerializer):
    rank = RankSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    rank_id = serializers.PrimaryKeyRelatedField(
        queryset=Rank.objects.all(), 
        source='rank', 
        write_only=True, 
        allow_null=True, 
        required=False
    )
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), 
        source='department', 
        write_only=True, 
        allow_null=True, 
        required=False
    )

    date_of_birth = serializers.DateField(required=False, allow_null=True)
    date_of_retirement = serializers.DateField(required=False, allow_null=True)
    date_of_edara = serializers.DateField(required=False, allow_null=True)
    date_of_appointment = serializers.DateField(required=False, allow_null=True)
    image = serializers.ImageField(required=False, allow_null=True)
    amen_or_ola = serializers.BooleanField(required=False, allow_null=True, default=False)
    rank_kind = serializers.IntegerField(required=False, allow_null=True)
    dep_sort = serializers.IntegerField(required=False, allow_null=True)
    seniority_order = serializers.IntegerField(required=False, allow_null=True)
    mainornot = serializers.IntegerField(required=False, allow_null=True)
    bus = serializers.IntegerField(required=False, allow_null=True)
    tmamam = serializers.IntegerField(required=False, allow_null=True)
    food = serializers.IntegerField(required=False, allow_null=True)
    nickname = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    id_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    gender = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    marital_status = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    alt_phone_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    governorate = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    district = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    address = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    police_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    total_leave = serializers.IntegerField(required=False, allow_null=True)
    rahatcounter = serializers.IntegerField(required=False, allow_null=True)
    insurance_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    health_status = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    operation = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    idcard_expir = serializers.DateField(required=False, allow_null=True)
    idcard_work = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    idcard_social = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    is_driver = serializers.BooleanField(required=False, default=False, allow_null=True)
    dryfood = serializers.BooleanField(required=False, allow_null=True, default=False)
    mony_out = serializers.BooleanField(required=False, allow_null=True, default=False)

    class Meta:
        model = Employee
        fields = [
            'id', 'sort_number', 'seniority_order', 'name', 'nickname', 'id_number', 'gender', 
            'marital_status', 'phone_number', 'alt_phone_number', 'governorate', 
            'district', 'address', 'age', 'date_of_birth', 'date_of_retirement', 
            'date_of_edara', 'date_of_appointment', 'police_number', 
            'insurance_number', 'health_status', 'rank', 'department', 
            'operation', 'image', 'amen_or_ola', 'rank_kind', 
            'dep_sort', 'mainornot', 'bus', 'tmamam', 'food', 'rahatcounter', 'institute_id',
            'total_leave', 'rank_id', 'nots', 'department_id', 'idcard_expir', 'idcard_work', 'idcard_social', 'is_driver', 'dryfood', 'mony_out'
        ]
        read_only_fields = []

    def validate_id_number(self, value):
        if value == '' or value is None:
            return None
        return value

    def validate_amen_or_ola(self, value):
        if value is None:
            return False
        return value

    def validate_tmamam(self, value):
        if value is None:
            return 0
        return value

    def validate_food(self, value):
        if value is None:
            return 0
        return value

    def validate_bus(self, value):
        if value is None:
            return 0
        return value

    def validate_dryfood(self, value):
        if value is None:
            return False
        return value

    def validate_is_driver(self, value):
        if value is None:
            return False
        return value

    def validate_mony_out(self, value):
        if value is None:
            return False
        return value

    def validate_mainornot(self, value):
        if value is None:
            return 1
        return value

    def validate_rank_kind(self, value):
        if value == '' or value is None:
            return None
        return value

    def validate_dep_sort(self, value):
        if value == '' or value is None:
            return None
        return value

    def validate_rahatcounter(self, value):
        if value == '' or value is None:
            return 0
        return value

    def validate_total_leave(self, value):
        if value == '' or value is None:
            return 0
        return value

    def validate(self, data):
        id_number = data.get('id_number')
        instance = self.instance
        if id_number == '' or id_number is None:
            data['id_number'] = None
        elif instance and id_number != instance.id_number:
            if Employee.objects.filter(id_number=id_number).exclude(id=instance.id).exists():
                raise serializers.ValidationError("رقم الهوية هذا موجود بالفعل.")

        if 'id_number' in data and data['id_number']:
            birth_date = self.extract_birth_date(data['id_number'])
            if birth_date:
                data['date_of_birth'] = birth_date
                today = datetime.today().date()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                data['age'] = age
                data['date_of_retirement'] = birth_date.replace(year=birth_date.year + 60)
        return data

    def extract_birth_date(self, id_number):
        if not id_number or len(id_number) != 14 or not id_number.isdigit():
            return None
        
        century_digit = id_number[0]
        year = id_number[1:3]
        month = id_number[3:5]
        day = id_number[5:7]

        if century_digit == '2':
            full_year = f"19{year}"
        elif century_digit == '3':
            full_year = f"20{year}"
        else:
            return None

        try:
            return datetime.strptime(f"{full_year}-{month}-{day}", "%Y-%m-%d").date()
        except ValueError:
            return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        context = self.context
        if 'selected_columns' in context:
            selected_columns = context['selected_columns']
            for field in list(representation.keys()):
                if f"show_{field}" not in selected_columns and field != 'id':
                    representation.pop(field, None)
        return representation

    def __init__(self, *args, **kwargs):
        selected_columns = kwargs.pop('context', {}).get('selected_columns', None)
        super().__init__(*args, **kwargs)
        
        if selected_columns:
            allowed = {col.replace('show_', '') for col in selected_columns}
            allowed.add('id')
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)

class EmployeeStatementSerializer(serializers.ModelSerializer):
    rank = RankSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id', 'name', 'police_number', 'date_of_birth', 'date_of_appointment',
            'seniority_order',
            'address', 'district', 'governorate', 'rank', 'idcard_expir',
            'idcard_work', 'idcard_social', 'id_number', 'marital_status'
        ]