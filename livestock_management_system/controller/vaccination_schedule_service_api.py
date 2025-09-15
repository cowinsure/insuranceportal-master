from django.http import JsonResponse
from pydantic import ValidationError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apiservice.utils import handle_serializer_error, success_response
from common.common_class.has_module_access import HasModuleAccess
from common.common_class.util import build_request_with_user
from livestock_management_system.helper.livestock_management_helper_class import *
from livestock_management_system.helper.model_class import AssetInfoRequest
from rest_framework import status

class VaccinationScheduleServiceAPIView(APIView):

    #permission_classes = [IsAuthenticated] # For Validating Token
    permission_classes = [IsAuthenticated, HasModuleAccess]
    required_module = "FARM"

    def dispatch(self, request, *args, **kwargs):
        print(f"🔥 Dispatch received {request.method} request")
        return super().dispatch(request, *args, **kwargs)


    '''
    # @ Author: Tanmay Anthony Gomes
    # @ Create Time: 2025-06-11 15:00:13
    # @ Modified by: Tanmay Anthony Gomes
    # @ Modified time: 2025-06-15 11:04:31
    # @ Description: This api will add the schedule of vaccine
    '''
    def post(self, request):
        try:
            #data = request.data
            record = build_request_with_user(VaccinationScheduleRequest, request, method='POST')
            #record = VaccinationScheduleRequest(**request.data)  # validation happens here        
            result = add_asset_vaccination_schedule(record)  # validation happens here
            return JsonResponse(result)
        except ValidationError as e:
            return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)  

    '''
    # @ Author: Tanmay Anthony Gomes
    # @ Create Time: 2025-06-11 15:00:13
    # @ Modified by: Tanmay Anthony Gomes
    # @ Modified time: 2025-06-15 11:04:31
    # @ Description: This api will add the schedule of vaccine
    '''
    def get(self, request):
        try:
            #record = VaccinationScheduleRequest(**request.query_params.dict())  # validation happens here 
            record = build_request_with_user(VaccinationScheduleRequest, request, method='GET')   
            #record = VaccinationScheduleRequest(**request.data)  # validation happens here                
            result = get_asset_vaccination_schedule(record)  # validation happens here
            return JsonResponse(result)
        except ValidationError as e:
            return JsonResponse({"status": "failed", "errors": e.errors()}, status=400) 
    
        