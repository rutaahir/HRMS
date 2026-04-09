from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import Group



ROLE_CHOICES = (
    ("ADMIN","Admin"),
    ("HR","HR"),
    ("MANAGER","Manager"),
    ("EMPLOYEE","Employee"),
    ("SUPERADMIN","Super Admin"),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #role = models.CharField(max_length=20,choices=ROLE_CHOICES,default="EMPLOYEE")
    is_verified = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    otp = models.CharField(max_length=6,null=True,blank=True)
    otp_created_at = models.DateTimeField(null=True,blank=True)
    team_leader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tl_team_members')
    branch = models.ForeignKey('attendance.Branch', on_delete=models.SET_NULL, null=True, blank=True, related_name='branch_staff')
    phone = models.CharField(max_length=10, unique=True, null=True, blank=True)

    
    @property
    def role(self):
        group = self.user.groups.first()
        if group:
        # 'technoadvisor_Manager' માંથી માત્ર 'Manager' કાઢવા માટે
            return group.name.split('_')[-1].upper()
        return "EMPLOYEE"

    manager = models.ForeignKey(
         User,
         on_delete=models.SET_NULL,
         null=True,
         blank=True,
         related_name="team_members"
    )
    shift = models.ForeignKey(
        'attendance.Shift',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    company = models.ForeignKey(
         'attendance.Company',
         on_delete=models.SET_NULL,
         null=True,
         blank=True,
    )
    
    def __str__(self):
        return self.user.username
    
# accounts/models.py માં આ મુજબ સુધારો

def is_superadmin(user):
    # ૧. Django નું ઇન-બિલ્ટ સુપરયુઝર ચેક કરો
    return user.is_authenticated and user.is_superuser

def is_admin(user):
    # ૨. યુઝરના ગ્રુપ નામમાં 'admin' શબ્દ છે કે નહીં તે ચેક કરો
    if not user.is_authenticated: return False
    if user.is_superuser: return True
    return user.groups.filter(name__icontains="admin").exists()
    
def is_hr(user):
    return user.profile.role == "HR"
    
def is_manager(user):
    return user.profile.role == "MANAGER"
    
def is_employee(user):
    return user.profile.role == "EMPLOYEE"



# class Role(models.Model):
#     name = models.CharField(max_length=50, unique=True)

#     def __str__(self):
#         return self.name
# class RolePermission(models.Model):
#     role = models.OneToOneField(Role, on_delete=models.CASCADE)

#     can_manage_users = models.BooleanField(default=False)
#     can_approve_attendance = models.BooleanField(default=False)
#     can_view_team = models.BooleanField(default=False)
#     can_view_reports = models.BooleanField(default=False)
#     can_self_access = models.BooleanField(default=True)

#     def __str__(self):
#         return f"Permissions for {self.role.name}"
