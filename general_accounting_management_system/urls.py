from django.urls import path
from general_accounting_management_system.controller import general_accounting_management_api
from general_accounting_management_system.controller.fms_dashboard_service_api import FMSDashboardServiceAPIView
from general_accounting_management_system.controller.income_expense_brakdown_service_api import IncomeExpenseBreakdownServiceAPIView
from general_accounting_management_system.controller.income_expense_service_api import IncomeExpenseServiceAPIView
from general_accounting_management_system.controller.ledger_service_api import LedgerServiceAPIView

urlpatterns = [    
    # path('get-income-expense-list/', general_accounting_management_api.get_income_expense_list, name='get_income_expense_list'),  
    # path('add-income-expense/', general_accounting_management_api.create_income_expense, name='create_income_expense'),         
    # path('get-ledger-list/', general_accounting_management_api.get_ledger_list, name='get_ledger_list'),
    path('ledger-service/', LedgerServiceAPIView.as_view(), name='ledger-service'),  
    path('income-expense-service/', IncomeExpenseServiceAPIView.as_view(), name='income-expense-service'),    
    path('income-expense-breakdown-service/', IncomeExpenseBreakdownServiceAPIView.as_view(), name='income-expense-breakdown-service'), 
    path('fms-dashboard-service/', FMSDashboardServiceAPIView.as_view(), name='fms-dashboard-service'), 
     
]
