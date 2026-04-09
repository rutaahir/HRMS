"""
URL configuration for attendance_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("attendance/",include('attendance.urls')),  # it loads urls from attendence app 
    path('accounts/', include('accounts.urls')),
    # if we do not want to make seperate urls.py file , than this is master file and the code will be :
    # path('attendance/check-in/', views.check_in_view),

    path("accounts/",include('accounts.urls')),
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False), name='home-redirect'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


