from django.http import JsonResponse
from pydantic import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apiservice.utils import handle_serializer_error, success_response
from rest_framework.response import Response
from rest_framework import status

from common.common_class.util import build_request_with_user
from livestock_management_system.helper.livestock_management_helper_class import add_asset_production_records, get_asset_production_records
from livestock_management_system.helper.model_class import AssetProductionRecordsRequest

class AssetProductionRecordServiceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    """
    @ Author: Tanmay Anthony Gomes
    @ Create Time: 14-Sep-2025 04:01 PM
    @ Modified by: 
    @ Modified time: 
    @ Description: API to Insert Asset's Production Records
    """

    def post(self, request):
        try:
            record = build_request_with_user(AssetProductionRecordsRequest, request, method='POST')
            print (record)
            #record = AssetInfoRequest(**request.data)
            result = add_asset_production_records(record)
            return JsonResponse(result)
        except ValidationError as e:
            return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)

    """
    @ Author: AUTHOR
    @ Create Time: 14-Sep-2025 04:01 PM
    @ Modified by: 
    @ Modified time: 
    @ Description: API to get Asset's Production Records
    """

    def get(self, request):
        try:
            record = get_asset_production_records(AssetProductionRecordsRequest, request, method='GET')
            print (record)
            #record = AssetInfoRequest(**request.data)
            result = add_asset_production_records(record)
            return JsonResponse(result)
        except ValidationError as e:
            return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)    

