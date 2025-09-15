from django.urls import path

from .views import *

app_name = 'administrator_service'
urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('otp/', otp_list, name='otp_list'),
    path('roles/', roles_list, name='roles_list'),
    path('roles/create/', create_roles, name='create_roles'),
    # path('roles/modify/<int:pk>/', update_roles, name='update_roles'),
    # path('roles/modify/<int:pk>/', delete_roles, name='delete_roles'),

    path('asset-type/', asset_type_list, name='asset_type_list'),
    path('asset-type/create/', create_asset_type, name='create_asset_type'),




    path('breed/', breed_list, name='breed_list'),
    path('breed/create/', create_breed, name='create_breed'),

    path('color/', color_list, name='color_list'),
    path('color/create/', create_color, name='create_color'),

    path('vaccination-status/', vaccination_status_list, name='vaccination_status_list'),
    path('vaccination-status/create/', create_vaccination_status, name='create_vaccination_status'),

    path('deworming-status/', deworming_status_list, name='deworming_status_list'),
    path('deworming-status/create/', create_deworming_status, name='create_deworming_status'),

    path('user-module-access/', user_module_access_list, name='user_module_access_list'),
    path('user-module-access/create/', create_user_module_access, name='create_user_module_access'),


    path('users/', users_list, name='users_list'),
    path('users/create/', create_user, name='create_users'),
    path('users/create-insurecow-agent/', create_insurecow_agent, name='create_insurecow_users'),
    # path('users/modify/<int:pk>/', users_roles, name='update_roles'),
    # path('users/modify/<int:pk>/', users_roles, name='delete_roles'),

]
