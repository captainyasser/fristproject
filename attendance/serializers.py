from rest_framework import serializers
from .models import Attendance
from em_data.models import Employee
from departments.models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

class EmployeeSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), source='department', write_only=True, required=False
    )
    serial_number = serializers.IntegerField(read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'name', 'nickname','nots', 'department', 'department_id', 'rahatcounter', 'operation', 'serial_number']
        extra_kwargs = {
            'department_id': {'allow_null': True}
        }

class AttendanceSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), source='employee', write_only=True
    )

    class Meta:
        model = Attendance
        fields = [
            'id', 'employee', 'employee_id', 'date', 'state', 'food',
            'comfort_adjustment', 'in_or_out', 'created_at', 'updated_at'
        ]
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def validate(self, data):
        valid_states = [choice[0] for choice in Attendance._meta.get_field('state').choices]
        if data['state'] not in valid_states:
            raise serializers.ValidationError({"state": "حالة الحضور غير صالحة"})
        return data

class KashftmamResponseSerializer(serializers.Serializer):
    attendance_data = AttendanceSerializer(many=True)
    selected_date = serializers.DateField(allow_null=True)
    date_range = serializers.ListField(child=serializers.DateField())
    filtered_employees = EmployeeSerializer(many=True)
    first_number = serializers.IntegerField()
    last_number = serializers.IntegerField()
    padding_size = serializers.IntegerField()

class FoodListSerializer(serializers.Serializer):
    serial_number = serializers.IntegerField()
    name = serializers.CharField(max_length=255)

class FoodListResponseSerializer(serializers.Serializer):
    selected_date = serializers.DateField()
    formatted_date = serializers.CharField(max_length=100)
    names_with_serials = FoodListSerializer(many=True)
    columns = serializers.ListField(child=FoodListSerializer(many=True))
    num_rows = serializers.IntegerField()
    
    
    
    
# employees/serializers.py
from rest_framework import serializers
from .models import Employee

class MonthlyDiscountSerializer(serializers.ModelSerializer):
    rank_name = serializers.CharField(source='rank.name', allow_null=True, default='غير محدد')
    total_d_t = serializers.IntegerField()
    total_rahat = serializers.IntegerField()
    total_food = serializers.IntegerField()
    total_maradi = serializers.IntegerField()
    total_discount = serializers.IntegerField()
    total_eligible = serializers.IntegerField()

    class Meta:
        model = Employee
        fields = ['name', 'nots', 'rank_name', 'dep_sort', 'total_d_t', 'total_rahat', 'total_food', 'total_maradi', 'total_discount', 'total_eligible']









from rest_framework import serializers
from .models import Attendance
from em_data.models import Employee


class BulkAttendanceSerializer(serializers.Serializer):
    from_date = serializers.DateField()
    to_date = serializers.DateField()
    employee_ids = serializers.ListField(child=serializers.IntegerField())
    state = serializers.CharField()

    def validate(self, data):
        from_date = data['from_date']
        to_date = data['to_date']
        if from_date > to_date:
            raise serializers.ValidationError("نطاق التاريخ غير صالح")
        return data