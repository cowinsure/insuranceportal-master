from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class HealthRecordRequest(BaseModel):
    condition_id: Optional[int] = None
    severity_id: Optional[int] = None
    symptoms: Optional[str] = None
    treatment: Optional[str] = None
    treatment_date: Optional[datetime] = None
    veterinarian: Optional[str] = None
    remarks: Optional[str] = None
    asset_id: Optional[int] = None
    by_user_id: int = Field(..., description="Auto-injected from request.user.id")
    current_status_id: Optional[int] = None
    start_record : Optional[int] = None
    page_size: Optional[int] = None

class VaccineRequest(BaseModel):
    id: Optional[int] = None 
    name: Optional[str] = None
    remarks: Optional[str] = None
    start_record : Optional[int] = None
    page_size: Optional[int] = None
    by_user_id: int = Field(..., description="Auto-injected from request.user.id")


class VaccinationScheduleRequest(BaseModel):
    id: Optional[int] = None
    asset_id: Optional[int] = None
    vaccine_id: Optional[int] = None
    due_date: Optional[datetime] = None
    is_completed: Optional[bool] = None
    completed_at: Optional[datetime] = None
    remarks: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: Optional[bool] = None
    created_by: Optional[int] = None
    modified_by: Optional[int] = None           
    start_record : Optional[int] = None
    page_size: Optional[int] = None
    by_user_id: int = Field(..., description="Auto-injected from request.user.id")


class AssetMedicalConditionRequest(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    start_record : Optional[int] = None
    page_size: Optional[int] = None
    by_user_id: int = Field(..., description="Auto-injected from request.user.id")

class AssetMedicalConditionSeverityRequest(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    start_record : Optional[int] = None
    page_size: Optional[int] = None
    by_user_id: int = Field(..., description="Auto-injected from request.user.id")

class AssetInfoRequest(BaseModel):
    asset_id : Optional[int] = -1
    start_record : Optional[int] = None
    page_size: Optional[int] = None
    by_user_id: int = Field(..., description="Auto-injected from request.user.id")


class AssetHealthStatusRequest(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    asset_status_id: Optional[int] = None
    start_record : Optional[int] = None
    page_size: Optional[int] = None
    by_user_id: int = Field(..., description="Auto-injected from request.user.id")    


class AssetLocationHistoryRequest(BaseModel):
    id: int = None
    asset_id: int = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    created_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None
    start_record : Optional[int] = None
    page_size: Optional[int] = None
    by_user_id: int = Field(..., description="Auto-injected from request.user.id")  


class AssetProductionRecordsRequest(BaseModel):
    id: int = None
    production_type_id: int = None
    quantity: float = None
    date: Optional[datetime] = None
    remarks: Optional[str] = None
    created_at: Optional[datetime] = None
    created_by: Optional[int] = None
    modified_at: Optional[datetime] = None
    modified_by: Optional[int] = None
    is_active: Optional[bool] = None
    asset_id: int = None
    by_user_id: int = Field(..., description="Auto-injected from request.user.id")  