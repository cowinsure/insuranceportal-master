from django.urls import path

from .views import *

app_name = 'auth_service'
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', user_logout, name='logout'),

    path('registration/step-01/', registration_step_01, name='registration-step-01'),
    path('registration/step-02/<str:mobile_number>/<str:role>/', registration_step_02, name='registration-step-02'),
    path('registration/step-02/<str:mobile_number>/', registration_step_03, name='registration-step-03'),

]
