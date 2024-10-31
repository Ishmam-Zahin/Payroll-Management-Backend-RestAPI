# Generated by Django 5.1.2 on 2024-10-31 15:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employeeManagement_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payslips',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(default='pending', max_length=20)),
                ('details', models.JSONField()),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employeeManagement_app.employees')),
            ],
        ),
    ]
