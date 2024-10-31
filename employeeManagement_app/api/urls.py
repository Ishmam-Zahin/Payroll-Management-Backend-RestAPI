from django.urls import path
from . import views

urlpatterns = [
    path('departments/list/', views.DepartmentsList_API.as_view(), name='department_list'),
    path('departments/<int:pk>/', views.DepartmentsIndividual_API.as_view(), name='department_individual'),
    path('employeeType/list/', views.EmployeeTypeList_API.as_view(), name='employeeTypeList'),
    path('employeeType/<int:pk>/', views.EmployeeTypeDetails_API.as_view(), name='EmployeeTypeDetails'),
    path('<str:dptName>/employees/list/', views.Employees_list.as_view(), name='employees_list'),
    path('<str:dptName>/employees/<int:pk>/', views.Employee_details.as_view(), name='employee_details'),
    path('deduction/list/', views.Deduction_list.as_view(), name='deduction_list'),
    path('deduction/<int:pk>/', views.Deduction_details.as_view(), name='deduction_details'),
    path('employeeDeduction/list/', views.EmployeeDeduction_list.as_view()),
    path('employeeDeduction/<int:pk>/', views.EmployeeDeduction_detail.as_view()),
    path('compensation/list/', views.Compensation_list.as_view()),
    path('compensation/<int:pk>/', views.Compensation_details.as_view()),
    path('employeeCompensation/list/', views.EmployeeCompensation_list.as_view()),
    path('employeeCompensation/<int:pk>/', views.EmployeeCompensation_detail.as_view()),
]