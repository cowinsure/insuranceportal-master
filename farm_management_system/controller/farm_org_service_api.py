from django.http import JsonResponse
from pydantic import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apiservice.utils import handle_serializer_error, success_response
from rest_framework.response import Response
from rest_framework import status

from common.common_class.util import build_request_with_user
from farm_management_system.helper.insurance_management_helper_class import get_farm_organization_list, insert_farm_organizations, update_farm_organizations
from farm_management_system.helper.model_class import FarmOrgInfoRequest

class FarmOrgServiceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    """
    @ Author: Tanmay Anthony Gomes
    @ Create Time: 01-09-2025
    @ Modified by: 
    @ Modified time: 
    @ Description: API to insert farm organizations
    """

    def post(self, request):
        try:
            record = build_request_with_user(FarmOrgInfoRequest, request, method='POST')
            #record = AssetInfoRequest(**request.data)
            result = insert_farm_organizations(record)
            return JsonResponse(result)
        except ValidationError as e:
            return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)       

    """
    @ Author: Tanmay Anthony Gomes
    @ Create Time: 01-09-2025
    @ Modified by: 
    @ Modified time: 
    @ Description: API to update farm organizations
    """

    def put(self, request):
        try:
            record = build_request_with_user(FarmOrgInfoRequest, request, method='PUT')
            #record = AssetInfoRequest(**request.data)
            result = update_farm_organizations(record)
            return JsonResponse(result)
        except ValidationError as e:
            return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)   
        
    """
    @ Author: Tanmay Anthony Gomes
    @ Create Time: 01-09-2025
    @ Modified by: 
    @ Modified time: 
    @ Description: API to get farm organizations
    """

    def get(self, request):
        try:
            record = build_request_with_user(FarmOrgInfoRequest, request, method='GET')
            #record = AssetInfoRequest(**request.data)
            result = get_farm_organization_list(record)
            return JsonResponse(result)
        except ValidationError as e:
            return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)          
