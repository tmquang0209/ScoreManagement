from django.db import models
from django.utils import timezone  # Import timezone module

from subject.models import Subject
from student.models import Student
from teacher.models import Teacher

def currentTime():
    return timezone.now()

class Year(models.Model):
    year_code = models.CharField(max_length=255, primary_key=True)
    year_name = models.CharField(max_length=255)
    start_date = models.DateField(default=currentTime)
    end_date = models.DateField()
    tuition_fee = models.FloatField(default=100000)
    created_at = models.DateTimeField(default=currentTime)
    updated_at = models.DateTimeField(default=currentTime)

    class Meta:
        db_table = 'years'

class Semester(models.Model):
    semester_code = models.CharField(max_length=255, primary_key=True)
    semester_name = models.CharField(max_length=255)
    year_code = models.ForeignKey(Year, on_delete=models.CASCADE)
    start_date = models.DateField(default=currentTime)
    end_date = models.DateField()
    score_date = models.DateField()
    created_at = models.DateTimeField(default=currentTime)
    updated_at = models.DateTimeField(default=currentTime)

    class Meta:
        db_table = 'semesters'

class Schedule(models.Model):
    semester_code = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject_code = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher_code = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    classroom_code = models.CharField(max_length=255, primary_key=True)
    classroom_name = models.CharField(max_length=255)
    day = models.CharField(max_length=255)
    shift = models.CharField(max_length=255)
    capacity = models.IntegerField(default=10)
    room_number = models.CharField(max_length=255)
    available_seats = models.IntegerField(default=10)
    created_at = models.DateTimeField(default=currentTime)
    updated_at = models.DateTimeField(default=currentTime)

    class Meta:
        db_table = 'schedules'

class Enrollment(models.Model):
    student_code = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom_code = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=currentTime)
    updated_at = models.DateTimeField(default=currentTime)

    class Meta:
        db_table = 'enrollments'
