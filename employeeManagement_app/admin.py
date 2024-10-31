from django.contrib import admin
from .models import Departments, EmployeeType, Employees, Deductions, Compensations, EmployeeCompensations, EmployeeDeductions

# Register your models here.
admin.site.register(Departments)
admin.site.register(EmployeeType)
admin.site.register(Employees)
admin.site.register(Deductions)
admin.site.register(Compensations)
admin.site.register(EmployeeCompensations)
admin.site.register(EmployeeDeductions)