# smsapi/class/sms_client.py
import json
from django.conf import settings
import requests


from common.common_class.util import _response
from db import *
from sms_management_system.helper.model_class import *

API_URL = "https://corpsms.banglalink.net/bl/api/v1/smsapigw/"
HEADERS = {"Content-Type": "application/json"}

def send_sms_request(request: SendSMSRequest):
    try:
        payload = {
            "username": settings.BULKSMS_CONFIG["USERNAME"],
            "password": settings.BULKSMS_CONFIG["PASSWORD"],
            "apicode": settings.BULKSMS_CONFIG["APICODE"],
            "msisdn": request.msisdn,
            "countrycode": settings.BULKSMS_CONFIG["COUNTRY_CODE"],
            "cli": settings.BULKSMS_CONFIG["CLI"],
            "messagetype": "1",
            "message": request.message,
            "clienttransid": request.clienttransid,
            "bill_msisdn": settings.BULKSMS_CONFIG["BILL_MSISDN"],
            "tran_type": settings.BULKSMS_CONFIG["TRAN_TYPE"],
            "request_type": settings.BULKSMS_CONFIG["REQUEST_TYPE"],
            "rn_code": settings.BULKSMS_CONFIG["RN_CODE"],
        }

        response = requests.post(API_URL, json=payload, headers=HEADERS)

        if response.status_code == 200:
            resp_data = response.json()
            status_info = resp_data.get("statusInfo", {})
            
            # Prepare log record
            log_record = MsgSMSlogRequest(
                message_id=request.clienttransid,
                message_body=request.message,
                mobile_no=request.msisdn[0],
                person_id=0,
                amount=0,  # update if needed
                sms_flag=True,
                sms_type=1, # For OTP
                remarks=status_info.get("errordescription", "Sent"),
                created_by=2,
                client_ref_id=status_info.get("clienttransid"),
                server_ref_id=status_info.get("serverReferenceCode")
            )
            print("message_id:", request.clienttransid)
            print("message_body:", request.message)
            print("mobile_no:", request.msisdn[0])
            print("remarks:", status_info.get("errordescription", "Sent"))
            print("client_ref_id:", status_info.get("clienttransid"))
            print("client_ref_id:", status_info.get("serverReferenceCode"))

            # Save to DB
            add_msg_sms_log(log_record)
            return _response("success", "SMS sent successfully", resp_data)
        else:
            print("Payload:", json.dumps(payload, indent=2))
            return _response("failed", f"HTTP Error: {response.status_code}", response.text)

    except Exception as ex:
        return _response("error", str(ex))


def add_msg_sms_log(record: MsgSMSlogRequest):
    try:
        with get_db_connection() as conn: # calling get_db_connection for getting the connection string
            rows = call_db_function(conn, "public.fn_insert_sms_log", [record.json()]) # calling fn_get_assets_list function from DB  to get data.

            if not rows:
                return _response("failed", "Error Occured While Processing Request")

            result = rows[0]  
            data = result["data"]
            if isinstance(data, str):
                data = json.loads(data)

            return _response(result["status"], result["message"], data)

    except Exception as ex:
        return _response("error", str(ex))     