from django.contrib import admin
from .models import Company,AttendancePolicy,AttendanceCorrection,Shift

admin.site.register(Company)
admin.site.register(AttendancePolicy)
admin.site.register(AttendanceCorrection)
admin.site.register(Shift)


# attendance/admin.py
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_to', 'priority', 'status', 'due_date')
    list_filter = ('status', 'priority')
    search_fields = ('title', 'description')
