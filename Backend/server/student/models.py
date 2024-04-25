from django.db import models
import django.utils.timezone as timezone
from major.models import Major

currentTime = timezone.datetime.now

class Student(models.Model):
    student_code = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.TextField()
    birthdate = models.DateField
    gender = models.CharField(max_length=255)
    major_code = models.ForeignKey(Major, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=currentTime)
    updated_at = models.DateTimeField(default=currentTime)

    class Meta:
        db_table = 'students'

class StudentScore(models.Model):
    student_code = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject_code = models.CharField(max_length=255)
    score = models.FloatField()
    created_at = models.DateTimeField(default=currentTime)
    updated_at = models.DateTimeField(default=currentTime)

    class Meta:
        db_table = 'student_scores'