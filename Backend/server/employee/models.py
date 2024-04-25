from django.db import models
from django.utils import timezone
from department.models import Department, Role

currentTime = timezone.datetime.now

class Employee(models.Model):
    employee_code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birthdate = models.DateField()
    gender = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    department_code = models.ForeignKey(Department, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=currentTime)
    updated_at = models.DateTimeField(default=currentTime)

    class Meta:
        db_table = 'employees'