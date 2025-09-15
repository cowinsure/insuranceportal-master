from django.http import JsonResponse
from pydantic import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apiservice.utils import handle_serializer_error, success_response
from common.common_class.has_module_access import HasModuleAccess
from common.common_class.util import build_request_with_user
from livestock_management_system.helper.livestock_management_helper_class import get_assets_list
from livestock_management_system.helper.model_class import AssetInfoRequest
from rest_framework import status

class AssetsServiceAPIView(APIView):

    #permission_classes = [IsAuthenticated] # For Validating Token
    permission_classes = [IsAuthenticated, HasModuleAccess]
    required_module = "FARM"
    '''
    # @ Author: Tanmay Anthony Gomes
    # @ Create Time: 2025-06-11 15:00:13
    # @ Modified by: -
    # @ Modified time: -
    # @ Description: APi For Getting Asset List
    '''
    def get(self, request):
        try:
            record = build_request_with_user(AssetInfoRequest, request, method='GET')
            print (record)
            #record = AssetInfoRequest(**request.data)
            result = get_assets_list(record)
            return JsonResponse(result)
        except ValidationError as e:
            return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)