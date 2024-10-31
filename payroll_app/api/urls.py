from django.urls import path
from . import views

urlpatterns = [
    path('payslip/list/', views.Payslip_list.as_view()),
]
