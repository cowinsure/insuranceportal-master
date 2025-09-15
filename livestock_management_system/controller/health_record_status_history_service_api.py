from django.http import JsonResponse
from pydantic import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apiservice.utils import handle_serializer_error, success_response
from rest_framework.response import Response
from rest_framework import status

from common.common_class.has_module_access import HasModuleAccess
from common.common_class.util import build_request_with_user
from livestock_management_system.helper.livestock_management_helper_class import update_assets_health_record_status
from livestock_management_system.helper.model_class import HealthRecordRequest

class HealthRecordStatusHistoryServiceAPIView(APIView):
    #permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated, HasModuleAccess]
    required_module = "FARM"
    """
    @ Author: AUTHOR
    @ Create Time: 2025-07-12 4:00 PM
    @ Modified by: 
    @ Modified time: 
    @ Description: API to handle health_record_status_history_service insert operations
    """

    # def post(self, request):
    #     # Your logic here
    #     return Response({})

    """
    @ Author: AUTHOR
    @ Create Time: 2025-07-12 4:00 PM
    @ Modified by: 
    @ Modified time: 
    @ Description: API to handle health_record_status_history_service get operations
    """

    # def get(self, request):
    #     # Your logic here
    #     return Response({})        

    """
    @ Author: AUTHOR
    @ Create Time: 2025-07-12 4:00 PM
    @ Modified by: 
    @ Modified time: 
    @ Description: API to handle health_record_status_history_service update operations
    """

    def put(self, request):
        try:
            record = build_request_with_user(HealthRecordRequest, request, method='PUT')
            #record = HealthRecordRequest(**request.data)  # validation happens here        
            result = update_assets_health_record_status(record)  # validation happens here
            return JsonResponse(result)
        except ValidationError as e:
            return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)
        
    """
    @ Author: AUTHOR
    @ Create Time: 2025-07-12 4:00 PM
    @ Modified by: 
    @ Modified time: 
    @ Description: API to handle health_record_status_history_service delete operations
    """

    # def delete(self, request):
    #     # Your logic here
    #     return Response({})
