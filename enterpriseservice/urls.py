from django.urls import path

from .views import *

app_name = 'enterprise_service'
urlpatterns = [

    path('dashboard/', dashboard, name='dashboard'),
    path('agent-dashboard/', agent_dashboard, name='agent_dashboard'),
    path('users/', users_list, name='users_list'),
    path('users/create-farmer/', create_farmer, name='create_farmer'),
    path('users/create-staff/', create_staff, name='create_staff'),
]
