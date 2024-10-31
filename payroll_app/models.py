from django.db import models
from employeeManagement_app.models import Employees, Departments

# Create your models here.
class Payslips(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employees, on_delete=models.CASCADE)
    dept_id = models.ForeignKey(Departments, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')
    details = models.JSONField(null=False)

    def __str__(self):
        return self.employee_id