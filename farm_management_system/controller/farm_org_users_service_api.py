from django.http import JsonResponse
from pydantic import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apiservice.utils import handle_serializer_error, success_response
from rest_framework.response import Response
from rest_framework import status

from common.common_class.util import build_request_with_user
from farm_management_system.helper.insurance_management_helper_class import  get_farm_org_user_list,  insert_farm_org_users,  update_farm_org_users
from farm_management_system.helper.model_class import FarmOrgUserInfoRequest

class FarmOrgUsersServiceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    """
    @ Author: Tanmay Anthony Gomes
    @ Create Time: 02-Sep-2025 12:03 PM
    @ Modified by: 
    @ Modified time: 
    @ Description: API to handle farm_org_farmers_service_api insert operations
    """

    def post(self, request):
        try:
            record = build_request_with_user(FarmOrgUserInfoRequest, request, method='POST')
            #record = AssetInfoRequest(**request.data)
            result = insert_farm_org_users(record)
            return JsonResponse(result)
        except ValidationError as e:
            return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)    

    """
    @ Author: Tanmay Anthony Gomes
    @ Create Time: 02-Sep-2025 12:03 PM
    @ Modified by: 
    @ Modified time: 
    @ Description: API to handle farm_org_farmers_service_api get operations
    """

    def get(self, request):
        try:
            record = build_request_with_user(FarmOrgUserInfoRequest, request, method='GET')
            #record = AssetInfoRequest(**request.data)
            result = get_farm_org_user_list(record)
            return JsonResponse(result)
        except ValidationError as e:
            return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)       

    """
    @ Author: Tanmay Anthony Gomes
    @ Create Time: 02-Sep-2025 12:03 PM
    @ Modified by: 
    @ Modified time: 
    @ Description: API to handle farm_org_farmers_service_api update operations
    """

    def put(self, request):
        try:
            record = build_request_with_user(FarmOrgUserInfoRequest, request, method='PUT')
            #record = AssetInfoRequest(**request.data)
            result = update_farm_org_users(record)
            return JsonResponse(result)
        except ValidationError as e:
            return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)  

