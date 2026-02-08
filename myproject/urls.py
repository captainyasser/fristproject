"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from em_data.views import EmployeeViewSet
from ranks.views import RankViewSet
from departments.views import DepartmentList, DepartmentDetail
from rest_framework.authtoken.views import obtain_auth_token
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(title="My API", default_version='v1'),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'ranks', RankViewSet, basename='rank')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('em_data/', include('em_data.urls')),  # مسارات em_data بدون API
    path('institutes/', include('institutes.urls')), 
    path('users/', include('users.urls')),
    path('ranks/', include('ranks.urls')),
    path('allowances/', include('periodic_allowances.urls')),  # هذا موجود بالفعل، تأكد منه
    path('departments/', include('departments.urls')),
    path('attendance/', include('attendance.urls')),
    path('files/', include('file_sharing.urls')),
    path('backups/', include('backup_manager.urls')),
    path('tasks/', include('tasks.urls')),
    path('training/', include('training_teams.urls')), 
    path('tarkyat/', include('tarkyat.urls')),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),    
    path('api/em_data/', include('em_data.urls')),  # مسارات em_data تحت API
    path('api/', include(router.urls)),  # لـ employees و ranks فقط
    path('api/departments/', DepartmentList.as_view(), name='department-list'),
    path('api/departments/<int:id>/', DepartmentDetail.as_view(), name='department-detail'),
    path('secret-reports/', include('secret_reports.urls')),
    path('elawat-tashgeea/', include('elawat_tashgeea.urls', namespace='elawat_tashgeea')),
    path('education/', include('education.urls', namespace='education')),
    path('agaza-khasa/', include('agaza_khasa_app.urls', namespace='agaza_khasa_app')),
    path(    'hasr/', include('hasr_app.urls')),
    path('penalties/', include('penalties.urls')),
    path('settings/', include('system_settings.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
