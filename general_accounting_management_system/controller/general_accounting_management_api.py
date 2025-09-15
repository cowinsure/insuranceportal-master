import json

from django.http import JsonResponse
from pydantic import ValidationError

from general_accounting_management_system.helper.general_accounting_management_helper_class import *
from general_accounting_management_system.helper.model_class import *


'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 2025-06-11 15:00:13
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 2025-06-16 11:04:31
 # @ Description: This api will get the List of incomes and expenses
 '''
def get_income_expense_list(request):
     try:
        data = json.loads(request.body)
        record = IncomeExpenseRequest(**data)  # validation happens here        
        result = get_gls_income_expense_list(record)  # validation happens here
        return JsonResponse(result)
     except ValidationError as e:
         return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)                

'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 2025-06-11 15:00:13
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 2025-06-16 11:04:31
 # @ Description: This api will add the incomes and expenses
 '''
def create_income_expense(request):
     try:
        data = json.loads(request.body)
        record = IncomeExpenseRequest(**data)  # validation happens here        
        result = add_gls_income_expense(record)  # validation happens here
        return JsonResponse(result)
     except ValidationError as e:
         return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)    


'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 2025-06-11 15:00:13
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 2025-06-18 11:04:31
 # @ Description: This api will get ledger list
 '''
def get_ledger_list(request):
     try:
        data = json.loads(request.body)
        record = GlsLedgersRequest(**data)  # validation happens here        
        result = get_gls_ledger_list(record)  # validation happens here
        return JsonResponse(result)
     except ValidationError as e:
         return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)      