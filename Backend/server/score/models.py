from django.db import models
from django.utils import timezone

from semester.models import Semester
from student.models import Student
from subject.models import Subject

def currentTime():
    return timezone.now()

class Score(models.Model):
    semester_code = models.ForeignKey(Semester, on_delete=models.CASCADE)
    student_code = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject_code = models.ForeignKey(Subject, on_delete=models.CASCADE)
    midterm_score = models.FloatField()
    final_score = models.FloatField()
    created_at = models.DateTimeField(default=currentTime)
    updated_at = models.DateTimeField(default=currentTime)

    class Meta:
        db_table = 'scores'