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

class IncomeExpenseBreakdownServiceAPIView(APIView):
    #permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated, HasModuleAccess]
    required_module = "FARM"
    '''
    # @ Author: Tanmay Anthony Gomes
    # @ Create Time: 14-Jul-2025 12:09:24 PM
    # @ Modified by: -
    # @ Modified time: 14-Jul-2025 12:12:23 PM
    # @ Description: Api for getting income and expense breakdown
    '''

    def get(self, request):
        try:
            record = build_request_with_user(IncomeExpenseRequest, request, method='GET')
            #record = IncomeExpenseRequest(**request.data)
            result = get_gls_income_expense_breakdown_list(record)
            return JsonResponse(result)
        except ValidationError as e:
            return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)        

