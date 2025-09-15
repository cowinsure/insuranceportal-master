import json
from django.http import JsonResponse
from pydantic import ValidationError
from sms_management_system.helper.model_class import SendSMSRequest
from sms_management_system.helper.sms_management_helper_class import send_sms_request

'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 2025-06-11 15:00:13
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 2025-06-18 11:04:31
 # @ Description: This a fucntion will Send The Request to the providers server to send SMS. This is not an APi Function
 '''
# def send_sms(request):
#      try:
#         #data = json.loads(request.body)
#         record = SendSMSRequest(**request)  # validation happens here       
#         result = send_sms_request(record)  # calling function to send SMS via gateway
#         print(result)
#         return JsonResponse(result)
#      except ValidationError as e:
#          return JsonResponse({"status": "failed", "errors": e.errors()}, status=400)

def send_sms(request_data: dict) -> dict:
    try:
        record = SendSMSRequest(**request_data)  # validate
        return send_sms_request(record)  # returns dict
    except ValidationError as e:
        return {"status": "failed", "errors": e.errors()}         