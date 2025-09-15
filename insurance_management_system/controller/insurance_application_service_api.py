from django.http import JsonResponse
from pydantic import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apiservice.utils import handle_serializer_error, success_response
from common.common_class.has_module_access import HasModuleAccess
from common.common_class.util import build_request_with_user
from rest_framework import status
from insurance_management_system.helper.insurance_management_helper_class import get_insurance_insurance_application_list
from insurance_management_system.helper.model_class import  InsuranceApplicationRequest

class InsuranceApplicationServiceAPIView(APIView):
    #permission_classes = [IsAuthenticated] # For Validating Token
    permission_classes = [IsAuthenticated, HasModuleAccess]
    required_module = "FARM"
    '''
    # @ Author: Tanmay Anthony Gomes
    # @ Create Time: 2025-06-11 15:00:13
    # @ Modified by: -
    # @ Modified time: -
    # @ Description: APi For Getting Insurance Application List
    '''
    def get(self, request):
        try:
            record = build_request_with_user(InsuranceApplicationRequest, request, method='GET')
            #record = AssetInfoRequest(**request.data)
            result = get_insurance_insurance_application_list(record)
            return JsonResponse(result)
        except ValidationError as e:
            return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)