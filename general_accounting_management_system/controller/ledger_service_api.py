from django.http import JsonResponse
from pydantic import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apiservice.utils import handle_serializer_error, success_response
from rest_framework import status

from common.common_class.has_module_access import HasModuleAccess
from common.common_class.util import build_request_with_user
from general_accounting_management_system.helper.general_accounting_management_helper_class import get_gls_ledger_list
from general_accounting_management_system.helper.model_class import GlsLedgersRequest

class LedgerServiceAPIView(APIView):
    #permission_classes = [IsAuthenticated] # For Validating Token
    permission_classes = [IsAuthenticated, HasModuleAccess]
    required_module = "FARM"
    '''
    # @ Author: Tanmay Anthony Gomes
    # @ Create Time: 2025-06-11 15:00:13
    # @ Modified by: Tanmay Anthony Gomes
    # @ Modified time: 2025-06-18 11:04:31
    # @ Description: This api will get ledger list
    '''
    def get(self, request):
        try:
            record = build_request_with_user(GlsLedgersRequest, request, method='GET')
            #record = GlsLedgersRequest(**request.data)
            result = get_gls_ledger_list(record)
            return JsonResponse(result)
        except ValidationError as e:
            return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)