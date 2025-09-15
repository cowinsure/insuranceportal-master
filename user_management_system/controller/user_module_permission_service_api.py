

from django.http import JsonResponse
from pydantic import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apiservice.utils import handle_serializer_error, success_response
from rest_framework.response import Response
from rest_framework import status

from common.common_class.has_module_access import HasModuleAccess
from common.common_class.util import build_request_with_user
from general_accounting_management_system.helper.general_accounting_management_helper_class import get_fms_dashboard_summery
from general_accounting_management_system.helper.model_class import FMSDashboardRequest

class FMSDashboardServiceAPIView(APIView):
    #permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated, HasModuleAccess]
    required_module = "FARM"
    '''
    # @ Author: Tanmay Anthony Gomes
    # @ Create Time: 14-Jul-2025 01:12:39 PM
    # @ Modified by: -
    # @ Modified time: 14-Jul-2025 01:16:17 PM
    # @ Description: gettting dashboard data for farm management system
    '''

    # def get(self, request):
    #     try:
    #         record = build_request_with_user(FMSDashboardRequest, request, method='GET')
    #         #record = IncomeExpenseRequest(**request.data)
    #         result = get_fms_dashboard_summery(record)
    #         return JsonResponse(result)
    #     except ValidationError as e:
    #         return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)        

