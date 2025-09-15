# user_management_system/helper/user_management_helper_class.py
import psycopg2
from django.conf import settings
import json

from pydantic import ValidationError
from common.common_class.util import _response
from db import *
from insurance_management_system.helper.model_class import *

'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 2025-06-11 15:01:24
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 2025-06-11 15:58:18
 # @ Description: Function for getting asset list from DB
'''
def get_insurance_farmers_list(record: FarmersInfoRequest):
    try:
        with get_db_connection() as conn: # calling get_db_connection for getting the connection string
            rows = call_db_function(conn, "public.fn_get_insurance_farmers", [record.json()]) # calling fn_get_assets_list function from DB  to get data.

            if not rows:
                return _response("failed", "Error Occured While Processing Request")

            result = rows[0]  
            data = result["data"]
            if isinstance(data, str):
                data = json.loads(data)

            return _response(result["status"], result["message"], data)

    except Exception as ex:
        return _response("error", str(ex))
    

'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 2025-06-11 15:01:24
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 2025-06-11 15:58:18
 # @ Description: Function for getting Insurance Application list from DB
'''
def get_insurance_insurance_application_list(record: InsuranceApplicationRequest):
    try:
        with get_db_connection() as conn: # calling get_db_connection for getting the connection string
            rows = call_db_function(conn, "public.fn_get_insurance_application_list", [record.json()]) # calling fn_get_assets_list function from DB  to get data.

            if not rows:
                return _response("failed", "Error Occured While Processing Request")

            result = rows[0]  
            data = result["data"]
            if isinstance(data, str):
                data = json.loads(data)

            return _response(result["status"], result["message"], data)

    except Exception as ex:
        return _response("error", str(ex))
    

'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 2025-06-11 15:01:24
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 2025-06-11 15:58:18
 # @ Description: Function for getting Insurance Product list from DB
'''
def get_insurance_product_list(record: InsuranceProductRequest):
    try:
        with get_db_connection() as conn: # calling get_db_connection for getting the connection string
            rows = call_db_function(conn, "public.fn_get_insurance_product_list", [record.json()]) # calling fn_get_assets_list function from DB  to get data.

            if not rows:
                return _response("failed", "Error Occured While Processing Request")

            result = rows[0]  
            data = result["data"]
            if isinstance(data, str):
                data = json.loads(data)

            return _response(result["status"], result["message"], data)

    except Exception as ex:
        return _response("error", str(ex))


'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 2025-08-11 15:01:24
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 2025-08-11 15:58:18
 # @ Description: Function for Updating Insurance Status
'''
def update_insurance_status(record: InsuranceApplicationRequest):
    try:
        with get_db_connection() as conn: # calling get_db_connection for getting the connection string
            rows = call_db_function(conn, "public.fn_update_insurance_status", [record.json()]) # calling fn_get_assets_list function from DB  to get data.

            if not rows:
                return _response("failed", "Error Occured While Processing Request")

            result = rows[0]  
            data = result["data"]
            if isinstance(data, str):
                data = json.loads(data)

            return _response(result["status"], result["message"], data)

    except Exception as ex:
        return _response("error", str(ex))


'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 2025-08-11 15:01:24
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 2025-08-11 15:58:18
 # @ Description: Function for getting Insurance Status
'''
def get_insurance_status(record: InsuranceStatusRequest):
    try:
        with get_db_connection() as conn: # calling get_db_connection for getting the connection string
            rows = call_db_function(conn, "public.fn_get_insurance_status", [record.json()]) # calling fn_get_assets_list function from DB  to get data.

            if not rows:
                return _response("failed", "Error Occured While Processing Request")

            result = rows[0]  
            data = result["data"]
            if isinstance(data, str):
                data = json.loads(data)

            return _response(result["status"], result["message"], data)

    except Exception as ex:
        return _response("error", str(ex))
    
'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 2025-08-11 15:01:24
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 2025-08-11 15:58:18
 # @ Description: Function for getting Insurance Payment List
'''
def get_insurance_payment_list(record: InsurancePaymentInformationRequest):
    try:
        with get_db_connection() as conn: # calling get_db_connection for getting the connection string
            rows = call_db_function(conn, "public.fn_get_insurance_payment_list", [record.json()]) # calling fn_get_assets_list function from DB  to get data.

            if not rows:
                return _response("failed", "Error Occured While Processing Request")

            result = rows[0]  
            data = result["data"]
            if isinstance(data, str):
                data = json.loads(data)

            return _response(result["status"], result["message"], data)

    except Exception as ex:
        return _response("error", str(ex))    
    

'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 2025-08-11 15:01:24
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 2025-08-11 15:58:18
 # @ Description: Function for getting Insurance Payment List
'''
def get_insurance_claim_list(record: InsuranceClaimInformationRequest):
    try:
        with get_db_connection() as conn: # calling get_db_connection for getting the connection string
            rows = call_db_function(conn, "public.fn_get_insurance_claim_list", [record.json()]) # calling fn_get_assets_list function from DB  to get data.

            if not rows:
                return _response("failed", "Error Occured While Processing Request")

            result = rows[0]  
            data = result["data"]
            if isinstance(data, str):
                data = json.loads(data)

            return _response(result["status"], result["message"], data)

    except Exception as ex:
        return _response("error", str(ex))      


'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 2025-09-01 15:01:24
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 2025-09-01 15:58:18
 # @ Description: Function for getting Insurance Status History
'''
def get_insurance_status_history(record: InsuranceStatusHistoryRequest):
    try:
        with get_db_connection() as conn: # calling get_db_connection for getting the connection string
            rows = call_db_function(conn, "public.fn_get_insurance_status_history", [record.json()]) # calling fn_get_assets_list function from DB  to get data.

            if not rows:
                return _response("failed", "Error Occured While Processing Request")

            result = rows[0]  
            data = result["data"]
            if isinstance(data, str):
                data = json.loads(data)

            return _response(result["status"], result["message"], data)

    except Exception as ex:
        return _response("error", str(ex))
