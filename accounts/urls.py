from django.urls import path
from .import views

urlpatterns= [
    #path('',RedirectView.as_view(url='/', permanent=False)),
    path('login/', views.login_view, name="login_no_slug"),
    path('<slug:company_slug>/register/', views.register_view, name='register'),
    path('<slug:company_slug>/verify/',views.verify_view, name="verify_otp"),
    path('<slug:company_slug>/login/', views.login_view, name="login"),
    path('<slug:company_slug>/resend-otp/',views.resend_otp_view, name="resend_otp"),
    path('/logout/',views.logout_view,name="logout"),
    path('<slug:company_slug>/forgot-password/', views.forgot_password_view, name='forgot_password'),
path('<slug:company_slug>/verify-reset-otp/', views.verify_reset_otp_view, name='verify_reset_otp'),
path('<slug:company_slug>/set-new-password/', views.set_new_password_view, name='set_new_password'),
path('ajax/check-username/', views.check_username_exists, name='check_username'),
   # path('dashboard/manager/',views.manager_dashboard_view),
  #  path('dashboard/employee/',views.employee_dashboard_view),
    
path('superadmin/create-role/', views.create_dynamic_role, name='create_role'),
]