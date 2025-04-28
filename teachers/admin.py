from django.contrib import admin

from .models import Assignment,Teacher,Attendance# Register your models here.


admin.site.register(Assignment)
admin.site.register(Teacher)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status')
    list_filter = ('date', 'status')