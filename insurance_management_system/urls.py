from django.urls import path

from insurance_management_system.controller.insurance_application_service_api import InsuranceApplicationServiceAPIView
from insurance_management_system.controller.insurance_claim_service_api import InsuranceClaimServiceAPIView
from insurance_management_system.controller.insurance_payment_service_api import InsurancePaymentServiceAPIView
from insurance_management_system.controller.insurance_product_service_api import InsuranceProductServiceAPIView
from insurance_management_system.controller.farmer_service_api import FarmerServiceAPIView
from insurance_management_system.controller.insurance_status_history_service_api import InsuranceStatusHistoryServiceAPIView
from insurance_management_system.controller.insurance_status_service_api import InsuranceStatusServiceAPIView
urlpatterns = [
    path('insurance-application-service/', InsuranceApplicationServiceAPIView.as_view(), name='insurance-application-service'),
    path('insurance-product-service/', InsuranceProductServiceAPIView.as_view(), name='insurance-product-service'), 
    path('farmer-service/', FarmerServiceAPIView.as_view(), name='farmer-service'),
    path('insurance-status-history-service/', InsuranceStatusHistoryServiceAPIView.as_view(), name='insurance-status-history-service'),
    path('insurance-status-service/', InsuranceStatusServiceAPIView.as_view(), name='insurance-status-service'),   
    path('insurance-payment-service/', InsurancePaymentServiceAPIView.as_view(), name='insurance-payment-service'), 
    path('insurance-claim-service/', InsuranceClaimServiceAPIView.as_view(), name='insurance-claim-service'), 
]
