from django.db import models
from django.utils import timezone

currentTime = timezone.datetime.now

class Subject(models.Model):
    subject_code = models.CharField(max_length=255, primary_key=True)
    subject_name = models.CharField(max_length=255)
    credit = models.IntegerField(default=1)
    coef = models.FloatField(default=1.0)
    created_at = models.DateTimeField(default=currentTime)
    updated_at = models.DateTimeField(default=currentTime)

    class Meta:
        db_table = 'subjects'
