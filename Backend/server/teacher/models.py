from django.db import models
import django.utils.timezone
from major.models import Major

currentTime = django.utils.timezone.now

class Teacher(models.Model):
    teacher_code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.TextField()
    birthdate = models.DateField()
    major_code = models.ForeignKey(Major, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=currentTime)
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'teachers'
