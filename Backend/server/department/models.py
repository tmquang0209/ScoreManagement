from django.db import models
from django.utils import timezone

currentTime = timezone.datetime.now

class Department(models.Model):
    department_code = models.CharField(max_length=255, primary_key=True)
    department_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=currentTime)
    updated_at = models.DateTimeField(default=currentTime)

    class Meta:
        db_table = 'departments'

class Role(models.Model):
    role_code = models.CharField(max_length=255, primary_key=True)
    role_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=currentTime)
    updated_at = models.DateTimeField(default=currentTime)

    class Meta:
        db_table = 'roles'