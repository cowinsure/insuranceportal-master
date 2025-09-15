from django.urls import path

from farm_management_system.controller.farm_org_users_service_api import  FarmOrgUsersServiceAPIView
from farm_management_system.controller.farm_org_service_api import FarmOrgServiceAPIView


urlpatterns = [
    path('farm-org-service/', FarmOrgServiceAPIView.as_view(), name='farm-org-service'), 
    path('farm-org-users-service/', FarmOrgUsersServiceAPIView.as_view(), name='farm-org-users-service'),
]