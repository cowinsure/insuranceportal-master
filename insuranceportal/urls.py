from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('administrator/', include('administratorservice.urls')),
    path('insurecow-agent/', include('insurecowagentservice.urls')),
    path('insurance-company/', include('insurancecompanyservice.urls')),
    path('enterprise/', include('enterpriseservice.urls')),
    path('auth/', include('authservice.urls')),
    path('insurance/', include('insuranceservice.urls')),
    path('', include('coreservice.urls')),
    path('api/v1/', include('apiservice.urls')),
    path('api/lms/', include('livestock_management_system.urls')),
    path('api/gls/', include('general_accounting_management_system.urls')),  
    path('api/ims/', include('insurance_management_system.urls')), 
    path('api/fms/', include('farm_management_system.urls')),   
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
