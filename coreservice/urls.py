from django.urls import path

from .views import *

app_name = 'core_service'
urlpatterns = [
    path('', entry_view, name='entry_view'),

    path('dashboard/', dashboard, name='dashboard'),
]
