from django.http import JsonResponse
from pydantic import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apiservice.utils import handle_serializer_error, success_response
from rest_framework.response import Response
from rest_framework import status

from common.common_class.has_module_access import HasModuleAccess
from common.common_class.util import build_request_with_user
from general_accounting_management_system.helper.general_accounting_management_helper_class import *
from general_accounting_management_system.helper.model_class import IncomeExpenseRequest

class IncomeExpenseServiceAPIView(APIView):
    #permission_classes = [IsAuthenticated] # Token Validation
    permission_classes = [IsAuthenticated, HasModuleAccess]
    required_module = "FARM"
    '''
    # @ Author: Tanmay Anthony Gomes
    # @ Create Time: 2025-06-11 15:00:13
    # @ Modified by: Tanmay Anthony Gomes
    # @ Modified time: 2025-06-16 11:04:31
    # @ Description: This api will add the incomes and expenses
    '''

    def post(self, request):
        try:
            record = build_request_with_user(IncomeExpenseRequest, request, method='POST')
            #record = IncomeExpenseRequest(**request.data)
            result = add_gls_income_expense(record)
            return JsonResponse(result)
        except ValidationError as e:
            return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)

    '''
    # @ Author: Tanmay Anthony Gomes
    # @ Create Time: 2025-06-11 15:00:13
    # @ Modified by: Tanmay Anthony Gomes
    # @ Modified time: 2025-06-16 11:04:31
    # @ Description: This api will get the List of incomes and expenses
    '''

    def get(self, request):
        try:
            record = build_request_with_user(IncomeExpenseRequest, request, method='GET')
            #record = IncomeExpenseRequest(**request.data)
            result = get_gls_income_expense_list(record)
            return JsonResponse(result)
        except ValidationError as e:
            return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)        

