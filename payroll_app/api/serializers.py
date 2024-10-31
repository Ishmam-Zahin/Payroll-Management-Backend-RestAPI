from rest_framework import serializers
from payroll_app.models import Payslips

class PayslipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payslips
        fields = '__all__'