from django.contrib import admin
from .models import Year, Semester, Schedule, Enrollment

admin.site.register(Year)
admin.site.register(Semester)
admin.site.register(Schedule)
admin.site.register(Enrollment)