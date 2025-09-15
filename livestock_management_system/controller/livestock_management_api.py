import json
from django.http import JsonResponse
from livestock_management_system.helper.livestock_management_helper_class import *
from django.views.decorators.http import require_GET
from pydantic import ValidationError
from livestock_management_system.helper.model_class import *
'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 2025-06-11 15:00:13
 # @ Modified by: -
 # @ Modified time: -
 # @ Description: APi For Getting Asset List
'''
@require_GET
def fetch_assets(request):
     try:
        data = json.loads(request.body)
        record = AssetInfoRequest(**data)  # validation happens here        
        result = get_assets_list(record)  # validation happens here
        return JsonResponse(result)
     except ValidationError as e:
         return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)

'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 2025-06-12 12:44:24
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 
 # @ Description: Api For Inserting Livestock Health records 
 '''
def create_health_record(request):
     try:
        data = json.loads(request.body)
        record = HealthRecordRequest(**data)  # validation happens here        
        result = add_assets_health_record(record)  # validation happens here
        return JsonResponse(result)
     except ValidationError as e:
         return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)

'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 2025-06-11 15:01:24
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 2025-06-12 17:44:57
 # @ Description: To get Live stock's health records
 '''
def get_health_record(request):
     try:
        data = json.loads(request.body)
        record = HealthRecordRequest(**data)  # validation happens here        
        result = get_assets_health_record(record)  # validation happens here
        return JsonResponse(result)
     except ValidationError as e:
         return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)   
     
'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 2025-06-11 15:00:13
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 2025-06-15 11:04:31
 # @ Description: This api will get the list of vaccine
 '''
def get_vaccine_list(request):
     try:
        data = json.loads(request.body)
        record = VaccineRequest(**data)  # validation happens here        
        result = get_asset_vaccine_list(record)  # validation happens here
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
def create_asset_vaccination_schedule(request):
     try:
        data = json.loads(request.body)
        record = VaccinationScheduleRequest(**data)  # validation happens here        
        result = add_asset_vaccination_schedule(record)  # validation happens here
        return JsonResponse(result)
     except ValidationError as e:
         return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)

'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 2025-06-11 15:00:13
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 2025-06-15 11:04:31
 # @ Description: This api will get the schedule of vaccine
 '''
def get_vaccination_schedule(request):
     try:
        data = json.loads(request.body)
        record = VaccinationScheduleRequest(**data)  # validation happens here        
        result = get_asset_vaccination_schedule(record)  # validation happens here
        return JsonResponse(result)
     except ValidationError as e:
         return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)          



'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 2025-06-11 15:00:13
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 2025-06-15 11:04:31
 # @ Description: This api will get the medical condition types
 '''
def get_medical_condition(request):
     try:
        data = json.loads(request.body)
        record = AssetMedicalConditionRequest(**data)  # validation happens here        
        result = get_asset_medical_condition(record)  # validation happens here
        return JsonResponse(result)
     except ValidationError as e:
         return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)    

'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 2025-06-11 15:00:13
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 2025-06-15 11:04:31
 # @ Description: This api will get the medical condition severity types
 '''
def get_medical_condition_severity(request):
     try:
        data = json.loads(request.body)
        record = AssetMedicalConditionSeverityRequest(**data)  # validation happens here        
        result = get_asset_medical_condition_severity(record)  # validation happens here
        return JsonResponse(result)
     except ValidationError as e:
         return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)            
             