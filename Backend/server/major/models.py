from django.db import models
from django.utils import timezone
from subject.models import Subject

currentTime = timezone.datetime.now

# Create your models here.
class Major(models.Model):
    major_code = models.CharField(max_length=255, primary_key=True)
    major_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=currentTime)
    updated_at = models.DateTimeField(default=currentTime)

    class Meta:
        db_table = 'majors'

class MajorSubject(models.Model):
    major_code = models.ForeignKey(Major, on_delete=models.CASCADE)
    subject_code = models.ForeignKey(Subject, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=currentTime)
    updated_at = models.DateTimeField(default=currentTime)

    class Meta:
        db_table = 'majors_subjects'