from django.db import models
    
# Create your models here.
class Departments(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    code_name = models.CharField(max_length=10, null=False, unique=True, blank=False)
    found_date = models.DateField(null=False, blank=False)

    def lower_codeName(self):
        self.code_name = self.code_name.lower()

    def save(self, *args, **kwargs):
        self.lower_codeName()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code_name

class EmployeeType(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50, null=False, unique=True, blank=False)

    def __str__(self):
        return self.type_name

type_choices = [
    ('tax', 'Tax'),
    ('insurance', 'Insurance'),
    ('loan', 'Loan')
]
class Deductions(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    type = models.CharField(max_length=20, null=False, blank=False, choices=type_choices)
    received_money = models.IntegerField(default=-1)
    give_money = models.IntegerField(default=-1)
    deduct_per_payslip = models.CharField(max_length=20, null=False, blank=False)
    desc = models.TextField(null=True, default=None)

    def __str__(self):
        return self.name

class Compensations(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    money_per_payslip = models.CharField(max_length=20, null=False, blank=False)
    minimun_money = models.IntegerField(default=-1)
    desc = models.TextField(null=True, default=None)

    def __str__(self):
        return self.name

gender_choices = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]
relegion_choices = [
    ('islam', 'Islam'),
    ('hindu', 'Hindu'),
    ('christian', 'Christian'),
    ('other', 'Other'),
]
class Employees(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20, null=False, blank=False)
    last_name = models.CharField(max_length=20, null=False, blank=False)
    phone_num = models.CharField(max_length=14, null=False, blank=False)
    email = models.EmailField(max_length=200, null=False, blank=False)
    age = models.CharField(max_length=3, null=False, blank=False)
    gender = models.CharField(max_length=10, null=False, blank=False, choices=gender_choices)
    relegion = models.CharField(max_length=50, null=False, blank=False, choices=relegion_choices)
    joined_date = models.DateField(null=False, blank=False)
    photo_url = models.URLField(max_length=200, null=True, blank=True, default=None)
    faculty = models.CharField(max_length=20, null=False, blank=False)
    dept_id = models.ForeignKey(Departments, on_delete=models.CASCADE, related_name='employees')
    type_id = models.ForeignKey(EmployeeType, on_delete=models.CASCADE)
    allowed_leaves = models.SmallIntegerField(null=False, default=0)
    main_payscale = models.IntegerField(null=False, default=0)
    deductions = models.ManyToManyField(Deductions, through='EmployeeDeductions')
    compensations = models.ManyToManyField(Compensations, through='EmployeeCompensations')

    def __str__(self):
        return (self.first_name + ' ' + self.last_name)   

class EmployeeDeductions(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE, related_name='allDeductions')
    deduction_id = models.ForeignKey(Deductions, on_delete=models.CASCADE)
    remaining_money = models.IntegerField(default=-1)
    status = models.CharField(max_length=10, default='active')
    request_date = models.DateField(auto_now_add=True)

    def set_remainingMoney(self):
        self.remaining_money = self.deduction_id.give_money
    
    def save(self, *args, **kwargs):
        if self.id is None:
            self.set_remainingMoney()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.employee_id.first_name+self.employee_id.last_name+'=>'+self.deduction_id.name


class EmployeeCompensations(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE, related_name='allCompensations')
    compensation_id = models.ForeignKey(Compensations, on_delete=models.CASCADE)


    def __str__(self):
        return self.employee_id.first_name+self.employee_id.last_name+'=>'+self.compensation_id.name