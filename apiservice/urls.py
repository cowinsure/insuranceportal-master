from django.urls import path

from .views import *

urlpatterns = [
    path('auth/public/register/step1/', RegisterStep1.as_view(), name='register-step1'),
    path('auth/public/register/verify-otp/', VerifyOTP.as_view(), name='verify-otp'),
    path('auth/public/register/set-password/', SetPassword.as_view(), name='set-password'),

    path('auth/public/forgot-password/request/', ForgotPasswordRequestView.as_view(), name='forgot-password-request'),
    path('auth/public/forgot-password/verify/', ForgotPasswordVerifyOTPView.as_view(), name='forgot-password-verify'),
    path('auth/public/forgot-password/set/', ForgotPasswordSetView.as_view(), name='forgot-password-set'),


    path('auth/public/login/', Login.as_view(), name='login'),

    path('auth/user/personal-info/', SetPersonalInfo.as_view(), name='personal-info'),
    path('auth/user/financial-info/', SetFinancialInfo.as_view(), name='financial-info'),
    path('auth/user/nominee-info/', SetNomineeInfo.as_view(), name='nominee-info'),
    path('auth/user/organization-info/', SetOrganizationInfo.as_view(), name='organization-info'),

    path('auth/public/token/verify/', VerifyTokenView.as_view(), name='verify-token'),

    path('auth/public/role-list/', RoleListAPIView.as_view(), name='role-list'),
    path('auth/admin/role/', RoleListCreateAPIView.as_view(), name='role-list-create'),
    path('auth/admin/role/<int:pk>/', RoleRetrieveUpdateDestroyAPIView.as_view(), name='role-detail'),
    path('auth/user/sub-users/', SubUsersAPIView.as_view(), name='sub-users'),
    path('auth/user/change-password/', ChangePasswordAPIView.as_view(), name='change-password'),

    path('assets-type/', AssetTypeListAPIView.as_view(), name='asset-type-list'),
    path('breeds/', BreedListAPIView.as_view(), name='breed-list'),
    path('colors/', ColorListAPIView.as_view(), name='color-list'),
    path('vaccination-status/', VaccinationStatusListAPIView.as_view(), name='vaccination-status-list'),
    path('deworming-status/', DewormingStatusListAPIView.as_view(), name='deworming-status-list'),

    path('asset-list/', AssetListAPIView.as_view(), name='asset-list'),
    path('create-asset/', AssetCreateAPIView.as_view(), name='asset-create'),
    path('assets/<int:pk>/', AssetDetailAPIView.as_view(), name='asset-detail'),
    path('get-cow/', get_cow_by_reference, name='get_cow_by_reference'),
    path('insurance-product/', CompanyWiseInsuranceAPIView.as_view(), name='nominee-info'),
    path('insurance-apply/', AssetInsuranceCreateAPIView.as_view(), name='asset-insurance-apply'),
    path('insurance-claim/', InsuranceClaimCreateAPIView.as_view(), name='insurance-claim'),
    path('insurance-list/', InsurancelistAPIView.as_view(), name='insurance-claim'),

    path('payments/create/', PaymentInformationCreateView, name='payment-create'),
    path('payments/<int:pk>/', PaymentInformationDetailView.as_view(), name='payment-detail'),

    path('payments/by-insurance/<str:insurance_id>/', PaymentByInsuranceAPIView.as_view(), name='payments-by-insurance'),

]
