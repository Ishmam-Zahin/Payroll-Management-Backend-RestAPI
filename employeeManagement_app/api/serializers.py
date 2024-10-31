from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from employeeManagement_app.models import Departments, EmployeeType, Employees, Deductions, DeductionEligibility, EmployeeDeductions, Compensations, CompensationEligibility, EmployeeCompensations

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = '__all__'
    
    def validate_code_name(self, value):
        return value.lower()

class EmployeeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeType
        fields = '__all__'

class DeductionEligibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeductionEligibility
        fields = '__all__'

class DeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deductions
        fields = '__all__'

class CompensationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compensations
        fields = '__all__'

class EmployeeDeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDeductions
        fields = '__all__'
    
    def create(self, validated_data):
        validated_data['remaining_money'] = validated_data['deduction'].give_money
        return EmployeeDeductions.objects.create(**validated_data)
    
    def validate(self, attrs):
        print(attrs)
        data = list(attrs['deduction'].eligible_employee_type_ids.values_list('id', flat=True))
        if attrs['employee'].type.id not in data:
            raise ValidationError('employee is not eligible')
        return attrs

class EmployeeSerializer(serializers.ModelSerializer):
    deductions = DeductionSerializer(many = True, read_only = True)
    compensations = CompensationSerializer(many = True, read_only = True)
    class Meta:
        model = Employees
        fields = '__all__'


class EmployeeSerializerDetail(EmployeeSerializer):
    ...

class CompensationEligibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompensationEligibility
        fields = '__all__'

class EmployeeCompensationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeCompensations
        fields = '__all__'
    
    def validate(self, attrs):
        print(attrs)
        data = list(attrs['comp_id'].eligible_employee_type_id.values_list('id', flat=True))
        if attrs['employee_id'].type.id not in data:
            raise ValidationError('employee is not eligible')
        return attrs

