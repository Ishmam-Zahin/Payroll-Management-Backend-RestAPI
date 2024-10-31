from payroll_app.models import Payslips
from employeeManagement_app.models import Employees, EmployeeDeductions

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404, HttpResponse

from .serializers import PayslipSerializer

class Payslip_list(APIView):
    def get(self, request):
        payslips  = Payslips.objects.all()
        serializer = PayslipSerializer(payslips, many = True)
        return Response(serializer.data)

    def post(self, request):

        try:
            employee = Employees.objects.get(id = request.data['employee_id'])
        except:
            raise Http404

        data = {}
        data['employee_id']  = request.data['employee_id']
        data['dept_id'] = request.data['dept_id']
        data['details'] = {}
        data['details']['main_payscale'] = employee.main_payscale

        deductions = employee.allDeductions.all()
        compensations = employee.allCompensations.all()

        tmp = {}
        for d in deductions:
            if d.deduction.type == 'tax' or d.deduction.type == 'insurance':
                tmp[d.deduction.name] = d.deduction.deduct_per_payslip
            else:
                if d.deduction.deduction.deduct_per_payslip <= d.remaining_money:
                    tmp[d.deduction.name] = d.deduction.deduct_per_payslip
                    d.remaining_money = d.remaining_money - d.deduction.deduction.deduct_per_payslip
                else:
                    tmp[d.deduction.name] = d.remaining_money
                    d.remaining_money = 0
        
        data['details']['deductions'] = tmp

        tmp = {}
        for c in compensations:
            tmp[c.comp_id.name] = c.comp_id.money_per_payslip
        
        data['details']['compensations'] = tmp


        serializer = PayslipSerializer(data = data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)
