from django.urls import path

from .views import *

app_name = 'insurecow_agent_service'
urlpatterns = [

    path('dashboard/', dashboard, name='dashboard'),
]
