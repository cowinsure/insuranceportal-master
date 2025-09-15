# user_management_system/helper/user_management_helper_class.py
import psycopg2
from django.conf import settings
import json

from pydantic import ValidationError
from common.common_class.util import _response
from db import *
from livestock_management_system.helper.model_class import *

'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 2025-06-11 15:01:24
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 2025-06-11 15:58:18
 # @ Description: Function for getting asset list from DB
'''
def get_assets_list(record: AssetInfoRequest):
    try:
        with get_db_connection() as conn: # calling get_db_connection for getting the connection string
            print(record.dict()) 
            rows = call_db_function(conn, "public.fn_get_assets_list", [record.json()]) # calling fn_get_assets_list function from DB  to get data.

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
 # @ Create Time: 2025-06-12 12:44:24
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 
 # @ Description: Function For Inserting Livestock Health records 
 '''
def add_assets_health_record(record: HealthRecordRequest):
    try:
        with get_db_connection() as conn: # calling get_db_connection for getting the connection string
            rows = call_db_function(conn, "public.fn_insert_assets_health_records_v2", [record.json()]) # calling fn_get_assets_list function from DB  to get data.

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
 # @ Modified time: 2025-06-12 17:44:57
 # @ Description: To get Live stock's health records
 '''
def get_assets_health_record(record: HealthRecordRequest):
    try:
        with get_db_connection() as conn: # calling get_db_connection for getting the connection string
            rows = call_db_function(conn, "public.fn_get_assets_health_record_list", [record.json()]) # calling fn_get_assets_list function from DB  to get data.

            if not rows:
                return _response("failed", "Error Occured While Processing Request")

            result = rows[0]  
            data = result["data"]
            if isinstance(data, str):
                data = json.loads(data)

            return _response(result["status"], result["message"], data)

    except Exception as ex:
        return _response("error", str(ex))


def get_asset_vaccine_list(record: VaccineRequest):
    try:
        with get_db_connection() as conn: # calling get_db_connection for getting the connection string
            rows = call_db_function(conn, "public.fn_get_asset_vaccine", [record.json()]) # calling fn_get_assets_list function from DB  to get data.

            if not rows:
                return _response("failed", "Error Occured While Processing Request")

            result = rows[0]  
            data = result["data"]
            if isinstance(data, str):
                data = json.loads(data)

            return _response(result["status"], result["message"], data)

    except Exception as ex:
        return _response("error", str(ex))
    
def add_asset_vaccination_schedule(record: VaccinationScheduleRequest):
    try:
        with get_db_connection() as conn: # calling get_db_connection for getting the connection string
            rows = call_db_function(conn, "public.fn_insert_assets_vaccination_schedule", [record.json()]) # calling fn_get_assets_list function from DB  to get data.

            if not rows:
                return _response("failed", "Error Occured While Processing Request")

            result = rows[0]  
            data = result["data"]
            if isinstance(data, str):
                data = json.loads(data)

            return _response(result["status"], result["message"], data)

    except Exception as ex:
        return _response("error", str(ex))


def get_asset_vaccination_schedule(record: VaccinationScheduleRequest):
    try:
        with get_db_connection() as conn: # calling get_db_connection for getting the connection string
            rows = call_db_function(conn, "public.fn_get_asset_vaccination_schedule", [record.json()]) # calling fn_get_assets_list function from DB  to get data.

            if not rows:
                return _response("failed", "Error Occured While Processing Request")

            result = rows[0]  
            data = result["data"]
            if isinstance(data, str):
                data = json.loads(data)

            return _response(result["status"], result["message"], data)

    except Exception as ex:
        return _response("error", str(ex))




def get_asset_medical_condition(record: AssetMedicalConditionRequest):
    try:
        with get_db_connection() as conn: # calling get_db_connection for getting the connection string
            rows = call_db_function(conn, "public.fn_get_asset_medical_condition", [record.json()]) # calling fn_get_assets_list function from DB  to get data.

            if not rows:
                return _response("failed", "Error Occured While Processing Request")

            result = rows[0]  
            data = result["data"]
            if isinstance(data, str):
                data = json.loads(data)

            return _response(result["status"], result["message"], data)

    except Exception as ex:
        return _response("error", str(ex))

def get_asset_medical_condition_severity(record: AssetMedicalConditionSeverityRequest):
    try:
        with get_db_connection() as conn: # calling get_db_connection for getting the connection string
            rows = call_db_function(conn, "public.fn_get_asset_medical_condition_severity", [record.json()]) # calling fn_get_assets_list function from DB  to get data.

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
 # @ Create Time: 2025-06-12 12:44:24
 # @ Modified by: Tanmay Anthony Gomes
 # @ Modified time: 
 # @ Description: Function For Inserting Livestock Health records 
 '''
def update_assets_health_record_status(record: HealthRecordRequest):
    try:
        with get_db_connection() as conn: # calling get_db_connection for getting the connection string
            rows = call_db_function(conn, "public.fn_update_assets_health_record_status", [record.json()]) # calling fn_get_assets_list function from DB  to get data.

            if not rows:
                return _response("failed", "Error Occured While Processing Request")

            result = rows[0]  
            data = result["data"]
            if isinstance(data, str):
                data = json.loads(data)

            return _response(result["status"], result["message"], data)

    except Exception as ex:
        return _response("error", str(ex))
    

def get_asset_health_status(record: AssetHealthStatusRequest):
    try:
        with get_db_connection() as conn: # calling get_db_connection for getting the connection string
            rows = call_db_function(conn, "public.fn_get_asset_health_status", [record.json()]) # calling fn_get_assets_list function from DB  to get data.

            if not rows:
                return _response("failed", "Error Occured While Processing Request")

            result = rows[0]  
            data = result["data"]
            if isinstance(data, str):
                data = json.loads(data)

            return _response(result["status"], result["message"], data)

    except Exception as ex:
        return _response("error", str(ex))    
    
def add_assets_location_history(record: AssetLocationHistoryRequest):
    try:
        with get_db_connection() as conn: # calling get_db_connection for getting the connection string
            rows = call_db_function(conn, "public.fn_insert_assets_location_history", [record.json()]) # calling fn_get_assets_list function from DB  to get data.

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
 # @ Create Time: 11-Jun-2025 03:01:24 PM
 # @ Modified by: -
 # @ Modified time: 15-Jul-2025 10:40:20 AM
 # @ Description: FUnction to validate and store asset location data
 '''
def add_aseet_location(request_data: dict) -> dict:
    try:
        record = AssetLocationHistoryRequest(**request_data)  # validate
        return add_assets_location_history(record)  # returns dict
    except ValidationError as e:
        return {"status": "failed", "errors": e.errors()}       
    

'''
 # @ Author: Tanmay Anthony Gomes
 # @ Create Time: 14-Sep-2025 03:01:24 PM
 # @ Modified by: -
 # @ Modified time: -
 # @ Description: FUnction to store assets production records
 '''
def add_asset_production_records(record: AssetProductionRecordsRequest):
    try:
        with get_db_connection() as conn: # calling get_db_connection for getting the connection string
            rows = call_db_function(conn, "public.fn_insert_assetservice_asset_production_records", [record.json()]) # calling fn_get_assets_list function from DB  to get data.

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
 # @ Create Time: 14-Sep-2025 03:01:24 PM
 # @ Modified by: -
 # @ Modified time: -
 # @ Description: FUnction for getting assets production records
 '''
def get_asset_production_records(record: AssetProductionRecordsRequest):
    try:
        with get_db_connection() as conn: # calling get_db_connection for getting the connection string
            rows = call_db_function(conn, "public.fn_get_assetservice_asset_production_records", [record.json()]) # calling fn_get_assets_list function from DB  to get data.

            if not rows:
                return _response("failed", "Error Occured While Processing Request")

            result = rows[0]  
            data = result["data"]
            if isinstance(data, str):
                data = json.loads(data)

            return _response(result["status"], result["message"], data)

    except Exception as ex:
        return _response("error", str(ex))       