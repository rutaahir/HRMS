from django.urls import path, include
from .import views
from django.conf import settings # 👈 આ ઉમેરો
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns=[
   #path('admin/', admin.site.urls),
   path('ajax/check-username/', views.ajax_check_username, name='ajax_check_username'),
   path('broadcast-task/', views.tl_broadcast_task, name='tl_broadcast_task'),
   path('task/action/<int:task_id>/', views.tl_task_action, name='tl_task_action'),
   path('accounts/', include('accounts.urls')),
    path('', views.home, name="home"),
    
    path('task/update/<int:task_id>/', views.update_task_status, name='update_task_status'),
   path('leave/manage/', views.admin_manager_leave_requests, name='admin_manager_leave_requests'),
   path('assign-task/', views.tl_assign_task, name='tl_assign_task'),
   path('ajax/check-password/', views.ajax_check_password, name='ajax_check_password'),
    path('',views.home, name="home"),
    path('check-in/<slug:company_slug>/',views.check_in_view, name="check_in"),
    path('check-out/<slug:company_slug>/',views.check_out_view, name="check_out"),
    path('dashboard/',views.dashboard_view, name="dashboard"),
    path(
    'superadmin/company/<int:id>/update-slug/',
    views.update_company_slug,
    name='update_company_slug'
),
   path('hr/assign-shift/<int:user_id>/', views.hr_assign_shift, name='hr_assign_shift'),
    #path('attendance/assign-shift/<int:user_id>/', views.assign_shift, name='assign_shift'),
    path('dashboard/admin/',views.admin_dashboard_view,name="admin_dashboard"),
    path('dashboard/employee/<slug:company_slug>/',views.employee_dashboard_view,name="employee_dashboard"),
    path('dashboard/hr/', views.hr_dashboard_view, name='hr_dashboard_view'),
    # attendance/urls.py

    #path('dashboard/hr/',views.hr_dashboard_view),
    #path('dashboard/manager/',views.manager_dashboard_view),
    
path('yearly/export/', views.export_yearly_attendance_excel, name='export_yearly_attendance_excel'),
path('hr/squad/remove/', views.hr_remove_member, name='hr_remove_member'),
    path('dashboard/manager/', views.manager_dashboard_view, name='manager_dashboard'),
    path('dashboard/hr/employees/',views.hr_employee_list,name="hr_employee_list"),
    #path('hr/pending-users/',views.hr_pending_users,name="hr_pending_users"),
    #path('hr/approve/<int:id>/',views.hr_approve_user,name="hr_approve_user"),
    path('hr/assign-manager/<int:user_id>/',views.hr_assign_manager,name="hr_assign_manager"),
    path('hr/reports/',views.hr_attendance_report,name="hr_attendance_report"),
    path('manager/team-attendance/',views.manager_team_attendance,name="manager_team_attendance"),
    path("leave/apply/", views.apply_leave_view,name="apply_leave"),
    path("manager/leave-requests/",views.manager_leave_requests, name="manager_leave_requests"),
    path('notifications/read/', views.mark_notifications_read, name='mark_notifications_read'),
    path("admin/pending-managers/", views.admin_pending_managers, name="admin_pending_managers"),
    path("admin/approve/<int:id>/", views.admin_approve_user),
    path("admin/reject/<int:id>/", views.admin_reject_user),
    path("leave/my-requests/",views.my_leave_requests,name="my_leave_requests"),
    path("admin/list/", views.admin_list_view, name="admin_list"),
    path("hr/list/", views.hr_list_view, name="hr_list"),
    path('branch/<int:branch_id>/details/', views.branch_detail_view, name='branch_detail'),
    path("manager/list/", views.manager_list_view, name="manager_list"),
    path("employee/list/", views.employee_list_view, name="employee_list"),
    path('admin/view-attendance/<int:user_id>/',views.admin_view_attendance,name="admin_view_attendance"),
    path('admin/check-in/', views.admin_check_in, name="admin_check_in"),
    path('admin/check-out/', views.admin_check_out, name="admin_check_out"),
    path('dashboard/superadmin/',views.superadmin_dashboard_view,name="superadmin_dashboard"),
    path('superadmin/company/delete/<int:id>/',views.delete_company,name="delete_company"),
    path('superadmin/company/edit/<int:id>/',views.edit_company,name="edit_company"),
    path('superadmin/policy/delete/<int:id>/', views.company_delete_policy, name='company_delete_policy'),
    #path('superadmin/policy/delete/<int:id>/', views.delete_policy, name="delete_policy"),
    #path('superadmin/policy/edit/<int:id>/', views.edit_policy, name="edit_policy"),
    path('superadmin/company/<slug:company_slug>/add-policy/', views.company_add_policy, name='company_add_policy'),
    path('hr/policies/', views.hr_policy_list, name="hr_policy_list"),
    path('hr/today-attendance/', views.hr_today_attendance, name="hr_today_attendance"),
    path('correction/request/', views.request_correction, name="request_correction"),
    path('hr/correction/approve/<int:pk>/', views.hr_approve_correction),
    path('hr/correction/reject/<int:pk>/', views.hr_reject_correction),
    path('hr/correction-requests/', views.hr_correction_requests, name="hr_correction_requests"),
    path(
 'hr/daily-attendance/',
 views.hr_daily_attendance,
 name="hr_daily_attendance"
),
path('monthly/', views.monthly_attendance, name="monthly_attendance"),
path('hr/holidays/', views.holiday_list, name="holiday_list"),
path('superadmin/company/<slug:company_slug>/add-holiday/', views.company_add_holiday, name='company_add_holiday'),

#path('hr/holidays/edit/<int:pk>/', views.edit_holiday, name="edit_holiday"),
#path('hr/holidays/delete/<int:pk>/', views.delete_holiday, name="delete_holiday"),
path('superadmin/holiday/delete/<int:id>/', views.company_delete_holiday, name='company_delete_holiday'),
path('shifts/', views.shift_list, name="shift_list"),
path('superadmin/company/<slug:company_slug>/add-shift/', views.company_add_shift, name='company_add_shift'),
path('superadmin/shift/edit/<int:id>/', views.company_edit_shift, name='company_edit_shift'),
path('superadmin/holiday/edit/<int:id>/', views.company_edit_holiday, name='company_edit_holiday'),
path('superadmin/policy/edit/<int:id>/', views.company_edit_policy, name='company_edit_policy'),
path('superadmin/shift/delete/<int:id>/', views.company_delete_shift, name='company_delete_shift'),
#path('shifts/delete/<int:id>/', views.delete_shift, name="delete_shift"),
#path('hr/assign-shift/<int:user_id>/', views.hr_assign_shift, name="hr_assign_shift"),
path("superadmin/users/admins/", views.superadmin_admin_list, name="superadmin_admin_list"),
path("superadmin/users/hr/", views.superadmin_hr_list, name="superadmin_hr_list"),
path("superadmin/users/managers/", views.superadmin_manager_list, name="superadmin_manager_list"),
path("superadmin/users/employees/", views.superadmin_employee_list, name="superadmin_employee_list"),
path(
 'superadmin/users/managers/',
 views.superadmin_manager_list,
 name="superadmin_manager_list"
),
path(
 'superadmin/manager/<int:manager_id>/team/',
 views.superadmin_manager_team,
 name="superadmin_manager_team"),
 path(
 'superadmin/companies/',
 views.superadmin_company_overview,
 name="superadmin_company_overview"
),
path(
 'superadmin/company/<int:company_id>/details/',
 views.superadmin_company_details,
 name="superadmin_company_details"
),
path(
 'superadmin/roles/',
 views.superadmin_role_list,
 name="superadmin_role_list"
),
path(
 'superadmin/roles/add/',
 views.superadmin_add_role,
 name="superadmin_add_role"
),
path(
 'superadmin/roles/delete/<int:id>/',
 views.superadmin_delete_role,
 name="superadmin_delete_role"
),
path(
 'superadmin/permissions/',
 views.superadmin_permissions,
 name="superadmin_permissions"
),
path('policy/delete/<int:policy_id>/', views.company_delete_policy, name='company_delete_policy'),
path('superadmin/company/<slug:company_slug>/manage-all-permissions/', views.manage_all_role_permissions, name='manage_all_role_permissions'),
path('superadmin/company/<slug:company_slug>/manage-perms/<int:group_id>/', views.manage_role_permissions, name='manage_role_permissions'),
path('superadmin/company/<slug:company_slug>/manage-permissions/', views.manage_all_role_permissions, name='manage_all_role_permissions'),
path("admin/assign-role/<int:user_id>/", views.admin_assign_role, name="admin_assign_role"),
path("superadmin/unassigned-users/", views.superadmin_unassigned_users, name="superadmin_unassigned_users"),
# attendance/urls.py
path('check-in/<slug:company_slug>/', views.check_in_view, name='check_in'),
path('check-out/<slug:company_slug>/', views.check_out_view, name='check_out'),
path("superadmin/assign-company/<int:user_id>/", views.superadmin_assign_company, name="superadmin_assign_company"),
path("hr/pending-users/", views.hr_pending_users, name="hr_pending_users"),

path("hr/approve-user/<int:user_id>/", views.hr_approve_user, name="hr_approve_user"),
path(
   "superadmin/company/<int:company_id>/dashboard/",
   views.superadmin_company_dashboard,
   name="superadmin_company_dashboard"
),
path('manager/staff/all/', views.manager_total_staff_view, name='manager_total_staff'),
    path('manager/staff/present/', views.manager_present_today_view, name='manager_present_today'),
path(
   "admin/pending-users/",
   views.company_admin_pending_users,
   name="company_admin_pending_users"
),
# attendance/urls.py
path(
   "admin/approve-user/<int:user_id>/",
   views.company_admin_approve_user,
   name="company_admin_approve_user"
),

path(
   "admin/reject-user/<int:user_id>/",
   views.company_admin_reject_user,
   name="company_admin_reject_user"
),
path(
   "superadmin/make-admin/<int:user_id>/",
   views.superadmin_make_admin,
   name="superadmin_make_admin"
),
path(
   "attendance/manage-roles/",
   views.admin_manage_roles,
   name="admin_manage_roles"
),
path("attendance/employees/", views.admin_employee_list, name="admin_employee_list"),
path("admin/attendance/<int:user_id>/", views.admin_view_attendance, name="admin_view_attendance"),
path(
    "attendance/users/<str:role>/",
    views.admin_user_list_by_role,
    name="admin_user_list_by_role"
),
path('user/safe-delete/<int:user_id>/', views.safe_delete_user, name='safe_delete_user'),
path('delete-owner/<int:company_id>/', views.delete_company_owner, name='delete_company_owner'),
path('branch/remove-user/<int:user_id>/', views.remove_from_branch, name='remove_from_branch'),
path('branch/delete/<int:branch_id>/', views.delete_branch, name='delete_branch'),
path('logout/', views.logout_view, name='logout'),
path(
 "superadmin/list/<str:type>/",
 views.superadmin_user_company_list,
 name="superadmin_user_company_list"
),
path("hr/managers/", views.hr_managers_list, name="hr_managers_list"),
path("manager/corrections/",views.manager_view_corrections),
path("hr/team-leaders/", views.hr_team_leader_list, name="hr_tl_list"),
path("hr/corrections/",views.hr_view_corrections),
path("hr/correction/approve/<int:id>/",views.approve_correction),
path("hr/correction/reject/<int:id>/",views.reject_correction),
path(
   "manager/correction/request/",
   views.manager_request_correction,
   name="manager_request_correction"
),
path('hr/correction/request/', views.hr_request_correction , name="hr_request_correction"),
path('monthly/export/', views.export_monthly_attendance_excel, name="export_monthly"),
path("accounts/leave-requests/", views.admin_manager_leave_requests,name="admin_manager_leave_requests"),
path(
    "my-correction-requests/",
    views.my_correction_requests,
    name="my_correction_requests"
),
path('leave/approve/<int:id>/', views.admin_approve_leave, name='admin_approve_leave'),
path('leave/reject/<int:id>/', views.admin_reject_leave, name='admin_reject_leave'),
path("hr/correction-requests/", views.hr_correction_requests),

path("attendance/correction-requests/", views.admin_correction_requests,name="admin_correction_requests"),
path("my-leave-requests/", views.my_leave_requests, name="my_leave_requests"),
path("notifications/", views.notifications_page,name="notifications"),

path("leave/update/<int:id>/", views.update_leave, name="update_leave"),

path('profile/', views.profile_view, name="profile"),
path('profile/change-password/send-otp/', views.profile_change_password_otp, name="profile_send_otp"),
path('profile/change-password/verify/', views.profile_verify_password_otp, name="profile_verify_otp"),
path('ajax/check-otp/', views.ajax_check_otp, name='ajax_check_otp'),
# Specific Company nu Dashboard
#path('superadmin/company/<slug:company_slug>/dashboard/', views.company_admin_dashboard, name='company_admin_dashboard'),


path('accounts/logout/', views.logout_view, name='logout') ,
# Te company ma Admin assign karva
path('superadmin/company/<slug:company_slug>/assign-admin/', views.company_assign_admin, name='company_assign_admin'),
# attendance/urls.py માં ઉમેરો



# attendance/urls.py ma umero

path("hr/team-leaders/", views.hr_team_leader_list, name="hr_tl_list"),
path("manager/team-leaders/", views.manager_team_leader_list, name="manager_tl_list"),
path("manager/squad/assign/", views.manager_assign_squad, name="manager_assign_squad"),
path("manager/squad/revoke/<int:member_id>/", views.manager_revoke_squad, name="manager_revoke_squad"),

path("hr/squad/assign/", views.hr_assign_member, name="hr_assign_member"), # NEW
path("hr/squad/revoke/<int:member_id>/", views.hr_revoke_member, name="hr_revoke_member"), # NEW
path('manager/revoke-team-leader/<int:user_id>/', views.revoke_team_leader, name='revoke_team_leader'),


path('superadmin/company/<slug:company_slug>/assign-role/<int:user_id>/', 
         views.company_assign_role, name='company_assign_role'),

# urls.py માં ઉમેરો
path('superadmin/company/<slug:company_slug>/manage-perms/<int:group_id>/', views.manage_role_permissions, name='manage_role_permissions'),
# અગાઉ જે 'company_assign_role' લાઇન છે તેને ચેક કરી લેજો
path('superadmin/company/<slug:company_slug>/manage-perms/<int:group_id>/', views.manage_role_permissions, name='manage_role_permissions'),
path('superadmin/company/<slug:company_slug>/make-admin/<int:user_id>/', views.company_make_admin, name='company_make_admin'),
# ચેક કરી લેજો કે assign-role વાળો પાથ પહેલેથી છે કે નહીં
path('superadmin/company/<slug:company_slug>/update-weekoff/', views.update_weekoff_policy, name='update_weekoff_policy'),

path('superadmin/company/<slug:company_slug>/create-role/', views.create_company_role, name='create_company_role'),
path('superadmin/role/delete/<int:role_id>/', views.delete_company_role, name='delete_company_role'),
path('superadmin/company/<slug:company_slug>/update-slug/', views.update_company_slug, name='update_company_slug'),
#path('superadmin/create-role/<slug:company_slug>/', views.create_company_role, name='create_company_role'),
path('superadmin/assign-admin/<slug:company_slug>/', views.assign_company_admin, name='assign_company_admin'),
path('attendance/assign-dynamic-role/', views.admin_assign_role_dynamic, name='admin_assign_role_dynamic'),
# attendance/urls.py

# ✅ KEEP THIS LINE (Ensure it is exactly like this)
# attendance/urls.py

# Use the function name exactly as it appears in your views.py
path('manager/make-team-leader/<int:user_id>/', views.make_team_leader, name='make_team_leader'),
# attendance/urls.py
path('dashboard/team-leader/<slug:company_slug>/', views.tl_dashboard_view, name='tl_dashboard'),
# Option 1: URL with company name (What you have now)
path('task/team-mission/delete/', views.delete_team_mission, name='delete_team_mission'),
path('task/single/delete/<int:task_id>/', views.delete_single_task, name='delete_single_task'),
# Option 2: URL without company name (This will stop the 404 error)
path('dashboard/team-leader/', views.tl_dashboard_view, name='tl_dashboard'),
 #path('dashboard/team-leader/', views.team_leader_dashboard, name='tl_dashboard'),
path('manager/assign-team/', views.assign_team_to_leader, name='assign_team_to_leader'),
# attendance/urls.py
path('check-in/<slug:company_slug>/', views.check_in_view, name='check_in'),
path('check-out/<slug:company_slug>/', views.check_out_view, name='check_out'),
#path('shifts/add/', views.add_shift, name='add_shift'),
path('dashboard/owner/<slug:company_slug>/', views.company_owner_dashboard, name='company_owner_dashboard'),
path('superadmin/assign-owner/<slug:company_slug>/', views.assign_company_owner, name='assign_company_owner'),
path('api/live-roles/<slug:company_slug>/', views.get_live_employee_roles, name='get_live_employee_roles'),
path('branch/remove-staff/<int:user_id>/', views.remove_from_branch, name='remove_from_branch'),
]

if settings.DEBUG: #
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #