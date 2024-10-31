from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.http import Http404, HttpResponse

from .serializers import DepartmentSerializer, EmployeeTypeSerializer, EmployeeSerializer, DeductionSerializer, EmployeeDeductionSerializer, CompensationSerializer, EmployeeCompensationSerializer
from employeeManagement_app.models import Departments, EmployeeType, Employees, Deductions, EmployeeDeductions, Compensations, EmployeeCompensations

class DepartmentsList_API(APIView):
    def get(self, request):
        depts = Departments.objects.all()
        serializer = DepartmentSerializer(depts, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DepartmentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data = serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)



class DepartmentsIndividual_API(APIView):
    def get_dept(self, pk):
            try:
                return Departments.objects.get(id=pk)
            except:
                raise Http404
        
    def get(self, request, pk):
        dept = self.get_dept(pk)
        print(request.GET)
        
        serializer = DepartmentSerializer(dept)
        return Response(serializer.data)

    def put(self, request, pk):
        dept = self.get_dept(pk)
        serializer = DepartmentSerializer(dept, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data = serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
    
    def delete(self, request, pk):
        dept = self.get_dept(pk)
        code_name = dept.code_name
        dept.delete()
        return Response(status=status.HTTP_200_OK, data = {'message': 'deleted'})


class EmployeeTypeList_API(APIView):
    def get(self, request):
        etypes = EmployeeType.objects.all()
        serializer = EmployeeTypeSerializer(etypes, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = EmployeeTypeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

class EmployeeTypeDetails_API(APIView):
    def get_type(self, pk):
        try:
            return EmployeeType.objects.get(id = pk)
        except:
            raise Http404
        
    def get(self, request, pk):
        etype = self.get_type(pk)
        serializer = EmployeeTypeSerializer(etype)
        return Response(serializer.data)

    def put(self, request, pk):
        etype = self.get_type(pk)
        serializer = EmployeeTypeSerializer(etype, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def delete(self, request, pk):
        etype = self.get_type(pk)
        etype.delete()
        return Response(status=status.HTTP_200_OK, data={'message': 'deleted'})

class Employees_list(APIView):
    def get(self, request, dptName):
        dptName = dptName.lower()
        try:
            dpt = Departments.objects.get(code_name = dptName)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND, data={'message': 'not found'})
        employees = dpt.employees.all()
        serializer = EmployeeSerializer(employees, many = True)
        return Response(serializer.data)

    
    def post(self, request, dptName):
        serializer = EmployeeSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)

class Employee_details(APIView):
    def get_employee(self, dptName, pk):
        dptName = dptName.lower()
        try:
            dpt = Departments.objects.get(code_name = dptName)
            return dpt.employees.get(id = pk)
        except:
            raise Http404
        
    def get(self, request, dptName, pk):
        employee = self.get_employee(dptName, pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    
    def put(self, request, dptName, pk):
        employee = self.get_employee(dptName, pk)
        serializer = EmployeeSerializer(employee, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
    
    def delete(self, request, dptName, pk):
        employee = self.get_employee(dptName, pk)
        employee.delete()
        return Response(status=status.HTTP_200_OK, data={'message': 'deleted'})

class Deduction_list(APIView):
    def get(self, request):
        deductions = Deductions.objects.all()
        serializer = DeductionSerializer(deductions, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = DeductionSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

class Deduction_details(APIView):
    def get_deduction(self, pk):
        try:
            return Deductions.objects.get(id = pk)
        except:
            raise Http404

    def get(self, request, pk):
        d = self.get_deduction(pk=pk)
        serializer = DeductionSerializer(d)
        return Response(serializer.data)

    def put(self, request, pk):
        d = self.get_deduction(pk=pk)
        serializer = DeductionSerializer(d, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def delete(self, request, pk):
        d = self.get_deduction(pk=pk)
        d.delete()
        return Response(status=status.HTTP_200_OK, data={'message': 'deleted'})

class EmployeeDeduction_list(APIView):
    def post(self, request):
        serializer = EmployeeDeductionSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'ok':'ok'})
        else:
            return Response(serializer.errors)

class EmployeeDeduction_detail(APIView):
    def put(self, request, pk):
        try:
            obj = EmployeeDeductions.objects.get(id = pk)
        except:
            raise Http404
        
        serializer = EmployeeDeductionSerializer(obj, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)
    
    def delete(self, request, pk):
        try:
            obj = EmployeeDeductions.objects.get(id = pk)
        except:
            raise Http404
        
        obj.delete()
        return Response(status=status.HTTP_200_OK, data={'message': 'deleted'})

class Compensation_list(APIView):
    def get(self, request):
        comps = Compensations.objects.all()
        serializer = CompensationSerializer(comps, many = True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CompensationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)

class Compensation_details(APIView):
    def get_comp(self, pk):
        try:
            return Compensations.objects.get(id = pk)
        except:
            raise Http404
        
    def get(self, request, pk):
        comp = self.get_comp(pk)
        serializer = CompensationSerializer(comp)
        return Response(serializer.data)

    def put(self, request, pk):
        comp = self.get_comp(pk)
        serializer = CompensationSerializer(comp, data = request.data)  
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)  
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)
    
    def delete(self, request, pk):
        comp = self.get_comp(pk)
        comp.delete()
        return Response(status=status.HTTP_200_OK, data = {'message': 'deleted'})

class EmployeeCompensation_list(APIView):
    def post(self, request):
        serializer = EmployeeCompensationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'ok':'ok'})
        else:
            return Response(serializer.errors)

class EmployeeCompensation_detail(APIView):
    def put(self, request, pk):
        try:
            obj = EmployeeCompensations.objects.get(id = pk)
        except:
            raise Http404
        
        serializer = EmployeeCompensationSerializer(obj, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)
    
    def delete(self, request, pk):
        try:
            obj = EmployeeCompensations.objects.get(id = pk)
        except:
            raise Http404
        
        obj.delete()
        return Response(status=status.HTTP_200_OK, data={'message': 'deleted'})