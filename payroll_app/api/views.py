from payroll_app.models import Payslips
from employeeManagement_app.models import Employees

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from django.db import transaction

from .serializers import PayslipSerializer

class Payslip_list(APIView):
    def get(self, request):
        payslips  = Payslips.objects.all()
        serializer = PayslipSerializer(payslips, many = True)
        return Response(serializer.data)

    @transaction.atomic
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
            if '%' in d.deduction_id.deduct_per_payslip:
                money = round(((int(d.deduction_id.deduct_per_payslip[:-1]) * employee.main_payscale) / 100), 2)
            else:
                money = float(d.deduction_id.deduct_per_payslip)
            
            name = d.deduction_id.name.split('$')[0]

            if d.deduction_id.type == 'tax' or d.deduction_id.type == 'insurance':
                tmp[name] = money
            else:
                if money <= d.remaining_money:
                    tmp[name] = money
                    d.remaining_money = d.remaining_money - money
                else:
                    tmp[name] = d.remaining_money
                    d.remaining_money = 0
                d.save()
        
        data['details']['deductions'] = tmp

        tmp = {}
        for c in compensations:
            if '%' in c.compensation_id.money_per_payslip:
                money = round(((int(c.compensation_id.money_per_payslip[:-1]) * employee.main_payscale) / 100), 2)
            else:
                money = float(c.compensation_id.money_per_payslip)
            
            name = c.compensation_id.name.split('$')[0]

            if money < c.compensation_id.minimun_money:
                tmp[name] = float(c.compensation_id.minimun_money)
            else:
                tmp[name] = money
        
        data['details']['compensations'] = tmp

        if request.data['isEid'] == 'true':
            data['details']['compensations']['eidBonus'] = employee.main_payscale
        
        if request.data['isDurgaPuja'] == 'true':
            data['details']['compensations']['durgaPuja'] = employee.main_payscale
        
        if request.data['isChristmas'] == 'true':
            data['details']['compensations']['christmas'] = employee.main_payscale
        
        if request.data['isNewYear'] == 'true':
            data['details']['compensations']['newYear'] = round(((employee.main_payscale * 30) / 100), 2)


        serializer = PayslipSerializer(data = data)

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
