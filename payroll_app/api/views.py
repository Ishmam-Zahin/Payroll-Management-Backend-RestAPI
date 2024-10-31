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
        data['details'] = {}
        data['details']['name'] = employee.first_name + ' ' + employee.last_name
        data['details']['department'] = employee.dept_id.name
        data['details']['main_payscale'] = employee.main_payscale

        deductions = employee.allDeductions.all()
        compensations = employee.allCompensations.all()

        tmp = {}
        for d in deductions:
            if d.deduction_id.type == 'tax' or d.deduction_id.type == 'insurance':
                tmp[d.deduction_id.name] = d.deduction_id.deduct_per_payslip
            else:
                if d.deduction_id.deduct_per_payslip <= d.remaining_money:
                    tmp[d.deduction_id.name] = d.deduction_id.deduct_per_payslip
                    d.remaining_money = d.remaining_money - d.deduction_id.deduct_per_payslip
                else:
                    tmp[d.deduction_id.name] = d.remaining_money
                    d.remaining_money = 0
        
        data['details']['deductions'] = tmp

        tmp = {}
        for c in compensations:
            if c.compensation_id.name == '':
                ...
            else:
                tmp[c.compensation_id.name] = c.compensation_id.money_per_payslip
        
        data['details']['compensations'] = tmp

        if request.data['isEid'] == 'true':
            data['details']['compensations']['eidBonus'] = 50000
        
        if request.data['isDurgaPuja'] == 'true':
            data['details']['compensations']['durgaPuja'] = 50000
        
        if request.data['isChristmas'] == 'true':
            data['details']['compensations']['christmas'] = 50000
        
        if request.data['isNewYear'] == 'true':
            data['details']['compensations']['newYear'] = 50000


        serializer = PayslipSerializer(data = data)
        print(request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)


class Payslip_Details(APIView):
    def get(self, request, id):
        try:
            payslip = Payslips.objects.filter(employee_id = id).order_by('-id')[:1]
        except:
            raise Http404
        
        serializer = PayslipSerializer(payslip, many = True)
        return Response(serializer.data)
