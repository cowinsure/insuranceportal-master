from django.http import JsonResponse
from pydantic import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apiservice.utils import handle_serializer_error, success_response
from rest_framework.response import Response
from rest_framework import status

from common.common_class.has_module_access import HasModuleAccess
from common.common_class.util import build_request_with_user
from livestock_management_system.helper.livestock_management_helper_class import get_asset_health_status
from livestock_management_system.helper.model_class import AssetHealthStatusRequest

class HealthStatusServiceAPIView(APIView):
    #permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated, HasModuleAccess]
    required_module = "FARM"
    '''
    # @ Author: Tanmay Anthony Gomes
    # @ Create Time: 2025-06-11 15:00:13
    # @ Modified by: Tanmay Anthony Gomes
    # @ Modified time: 2025-06-15 11:04:31
    # @ Description: This api will get the health status list
    '''
    def get(self, request):
        try:
            record = build_request_with_user(AssetHealthStatusRequest, request, method='GET')
            #record = AssetHealthStatusRequest(**request.data)  # validation happens here        
            result = get_asset_health_status(record)  # validation happens here
            return JsonResponse(result)
        except ValidationError as e:
            return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)   