from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
# accounts એપમાંથી Profile વાપરીશું જેથી ડુપ્લીકેટ ના થાય
from accounts.models import Profile

# 1. COMPANY MODEL
class Company(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    def __str__(self):
        return self.name
# --- Aa code attendance/models.py ni niche add karo ---

class Branch(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True, null=True)
    
    # 🌍 NEW: GPS Geofencing Fields
    latitude = models.FloatField(null=True, blank=True, help_text="Branch GPS Latitude")
    longitude = models.FloatField(null=True, blank=True, help_text="Branch GPS Longitude")
    radius = models.IntegerField(default=50, help_text="Allowed check-in radius in meters")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.company.name}"


# 2. SHIFT MODEL
class Shift(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
    break_minutes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.start_time} - {self.end_time})"

# 3. ATTENDANCE POLICY
class AttendancePolicy(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    work_hours_required = models.FloatField(default=8.0)
    late_after_minutes = models.IntegerField(default=15)
    grace_time_minutes = models.IntegerField(default=0)
    week_off_days = models.CharField(max_length=50, default="6")

    def __str__(self):
        return f"Policy for {self.company.name}"

# 4. HOLIDAY MODEL
class Holiday(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.date}"


# 6. ATTENDANCE MODEL
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Absent')

    def __str__(self):
        return f"{self.user.username} - {self.date}"

# 7. LEAVE MODEL
class Leave(models.Model):
    STATUS_CHOICES = [('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

# 8. CORRECTION MODEL
class AttendanceCorrection(models.Model):
    STATUS_CHOICES = [('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField() 
    old_check_in = models.TimeField(null=True, blank=True)
    old_check_out = models.TimeField(null=True, blank=True)
    
    new_check_in = models.TimeField(null=True, blank=True)
    new_check_out = models.TimeField(null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

# 9. TASK MODEL
# class Task(models.Model):
#     STATUS_CHOICES = [('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed')]
#     title = models.CharField(max_length=200)
#     description = models.TextField(blank=True)
#     assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_assigned')
#     assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks_created')
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
#     due_date = models.DateField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

# 10. NOTIFICATION MODEL
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    link = models.CharField(max_length=255, default="#")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"
    
# attendance/models.py na ant ma aa umeiro

# attendance/models.py

# attendance/models.py
from django.contrib.auth.models import Group

class RolePermission(models.Model):
    # This MUST be 'group' to match your latest database structure
    group = models.OneToOneField(Group, on_delete=models.CASCADE, related_name='role_permissions', null=True, blank=True)
    
    # These are your 7 standard permissions from the old project
    can_manage_users = models.BooleanField(default=False)
    can_approve_attendance = models.BooleanField(default=False)
    can_approve_leave = models.BooleanField(default=False)
    can_manage_shifts = models.BooleanField(default=False)
    can_view_reports = models.BooleanField(default=False)
    can_view_team = models.BooleanField(default=False)
    can_self_access = models.BooleanField(default=False)


# models.py
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Submitted'), # Employee સબમિટ કરે ત્યારે
        ('Verified', 'Verified'),   # TL અપ્રૂવ કરે ત્યારે
        ('Rejected', 'Rejected'),   # TL રિજેક્ટ કરે ત્યારે
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_tasks')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Pending')
    due_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0) # 0 to 100%
    completion_file = models.FileField(upload_to='task_submissions/', null=True, blank=True)
    completion_note = models.TextField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    rejection_note = models.TextField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    
# models.py
class TaskAttachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='task_submissions/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File for {self.task.title}"