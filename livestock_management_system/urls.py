# user_management_system/urls.py
from django.urls import path
from livestock_management_system.controller import livestock_management_api
from livestock_management_system.controller.asset_production_record_service_api import AssetProductionRecordServiceAPIView
from livestock_management_system.controller.assets_service_api import AssetsServiceAPIView
from livestock_management_system.controller.health_record_service_api import HealthRecordServiceAPIView
from livestock_management_system.controller.health_record_status_history_service_api import HealthRecordStatusHistoryServiceAPIView
from livestock_management_system.controller.health_status_service_api import HealthStatusServiceAPIView
from livestock_management_system.controller.medical_condition_service_api import MedicalConditionServiceAPIView
from livestock_management_system.controller.medical_condition_severity_service_api import MedicalConditionSeverityServiceAPIView
from livestock_management_system.controller.vaccination_schedule_service_api import VaccinationScheduleServiceAPIView
from livestock_management_system.controller.vaccine_service_api import VaccineServiceAPIView

urlpatterns = [
    # path('get-assets/', livestock_management_api.fetch_assets, name='fetch_assets'),
    # path('add-health-record/', livestock_management_api.create_health_record, name='create_health_record'),
    # path('get-health-record/', livestock_management_api.get_health_record, name='get_health_record'),
    # path('get-vaccine-list/', livestock_management_api.get_vaccine_list, name='get_vaccine_list'),
    # path('add-asset-vaccination-schedule/', livestock_management_api.create_asset_vaccination_schedule, name='create_asset_vaccination_schedule'),    
    # path('get-vaccination-schedule/', livestock_management_api.get_vaccination_schedule, name='get_vaccination_schedule'),  
    # path('get-medical-condition/', livestock_management_api.get_medical_condition, name='get_medical_condition'),     
    # path('get-medical-condition-severity/', livestock_management_api.get_medical_condition_severity, name='get_medical_condition_severity'),
    path('assets-service/', AssetsServiceAPIView.as_view(), name='assets-service'),
    path('health-record-service/', HealthRecordServiceAPIView.as_view(), name='health-record-service'), 
    path('medical-condition-service/', MedicalConditionServiceAPIView.as_view(), name='medical-condition-service'),
    path('medical-condition-severity-service/', MedicalConditionSeverityServiceAPIView.as_view(), name='medical-condition-severity-service'),   
    path('vaccination-schedule-service/', VaccinationScheduleServiceAPIView.as_view(), name='vaccination-schedule-service'),   
    path('vaccine-service/', VaccineServiceAPIView.as_view(), name='vaccine-service'),    
    path('health-record-status-history-service/', HealthRecordStatusHistoryServiceAPIView.as_view(), name='health-record-status-history-service'),
    path('health-status-service/', HealthStatusServiceAPIView.as_view(), name='health-status-service'),         
    path('production-record-service/', AssetProductionRecordServiceAPIView.as_view(), name='production-record-service'),     
]
