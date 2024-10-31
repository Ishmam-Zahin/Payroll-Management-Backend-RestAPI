from django.db import models
    
# Create your models here.
class Departments(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    code_name = models.CharField(max_length=10, null=False, unique=True, blank=False)
    found_date = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.code_name

class EmployeeType(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50, null=False, unique=True, blank=False)

    def __str__(self):
        return self.type_name

class Deductions(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    type = models.CharField(max_length=20, null=False, blank=False)
    received_money = models.IntegerField(default=-1)
    give_money = models.IntegerField(default=-1)
    deduct_per_payslip = models.IntegerField(null=False, blank=False)
    desc = models.TextField(null=False, blank=False)
    eligible_employee_type_ids = models.ManyToManyField(EmployeeType, through='DeductionEligibility')

    def __str__(self):
        return self.name

class Compensations(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    money_per_payslip = models.IntegerField(default=0)
    eligible_employee_type_id = models.ManyToManyField(EmployeeType, through='CompensationEligibility')

    def __str__(self):
        return self.name

class Employees(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20, null=False, blank=False)
    last_name = models.CharField(max_length=20, null=False, blank=False)
    phone_num = models.CharField(max_length=14, null=False, blank=False)
    email = models.EmailField(max_length=200, null=False, blank=False)
    age = models.CharField(max_length=3, null=False, blank=False)
    gender = models.CharField(max_length=10, null=False, blank=False)
    joined_date = models.DateField(null=False, blank=False)
    photo_url = models.URLField(max_length=200, null=True, blank=True, default=None)
    faculty = models.CharField(max_length=20, null=False, blank=False)
    dept = models.ForeignKey(Departments, on_delete=models.CASCADE, related_name='employees')
    type = models.ForeignKey(EmployeeType, on_delete=models.CASCADE)
    allowed_leaves = models.SmallIntegerField(null=False, default=0)
    main_payscale = models.IntegerField(null=False, default=0)
    deductions = models.ManyToManyField(Deductions, through='EmployeeDeductions')
    compensations = models.ManyToManyField(Compensations, through='EmployeeCompensations')

    def __str__(self):
        return (self.first_name + ' ' + self.last_name)
    
class DeductionEligibility(models.Model):
    id = models.AutoField(primary_key=True)
    employee_type = models.ForeignKey(EmployeeType, on_delete=models.CASCADE)
    deduction = models.ForeignKey(Deductions, on_delete=models.CASCADE)

class EmployeeDeductions(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, related_name='allDeductions')
    deduction = models.ForeignKey(Deductions, on_delete=models.CASCADE)
    remaining_money = models.IntegerField(default=-1)
    status = models.CharField(max_length=10, default='pending')
    request_date = models.DateField(auto_now_add=True)
    approved_date = models.DateField(null=True, blank=True, default=None)


class CompensationEligibility(models.Model):
    id = models.AutoField(primary_key=True)
    comp_id = models.ForeignKey(Compensations, on_delete=models.CASCADE)
    employee_type_id = models.ForeignKey(EmployeeType, on_delete=models.CASCADE)

class EmployeeCompensations(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE, related_name='allCompensations')
    comp_id = models.ForeignKey(Compensations, on_delete=models.CASCADE)