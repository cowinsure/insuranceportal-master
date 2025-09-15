from django.urls import path

from .views import *

app_name = 'insurance_company_service'
urlpatterns = [

    path('dashboard/', dashboard, name='dashboard'),

    path('InsuranceCategory/', insurance_category_list, name='InsuranceCategory_list'),
    path('InsuranceCategory/create/', create_insurance_category, name='create_InsuranceCategory'),

    path('insurance-types/', insurance_type_list, name='insurance_type_list'),
    path('insurance-types/create/', create_insurance_type, name='create_insurance_type'),

    path('insurance-periods/', insurance_period_list, name='insurance_period_list'),
    path('insurance-periods/create/', create_insurance_period, name='create_insurance_period'),

    path('insurance-premium-percentage/', insurance_premium_percentage_list, name='insurance_premium_percentage_list'),
    path('insurance-premium-percentage/create/', create_insurance_premium_percentage,
         name='create_insurance_premium_percentage'),


    path('insurance/view/<int:pk>/', view_insurance_application, name='view_insurance_application'),

    path('insurance-application/', insurance_application_list, name='insurance_application_list'),
    path('insurance/detail/<int:pk>/', insurance_application_detail, name='insurance_application_detail'),
    path('insurance/<int:pk>/update-status/', update_insurance_status, name='update_insurance_status'),

    path('payments/by-insurance/<str:insurance_id>/', payment_info_by_insurance, name='payments_by_insurance'),

]
