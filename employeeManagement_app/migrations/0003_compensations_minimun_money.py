# Generated by Django 5.1.2 on 2024-11-02 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeeManagement_app', '0002_alter_compensations_money_per_payslip_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='compensations',
            name='minimun_money',
            field=models.IntegerField(default=-1),
        ),
    ]
