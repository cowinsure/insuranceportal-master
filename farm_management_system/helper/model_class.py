from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


class FarmOrgInfoRequest(BaseModel):
    farm_org_id: Optional[int] = None
    organization_id: Optional[int] = None
    farm_size: Optional[float] = None
    livestock_type: Optional[str] = None
    number_of_animals: Optional[int] = None
    owner_person_id: Optional[int] = None
    registration_no: Optional[str] = None
    farm_lat: Optional[str] = None
    farm_long: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: Optional[bool] = None
    modified_by: Optional[int] = None
    start_record : Optional[int] = None
    page_size: Optional[int] = None
    by_user_id: int = Field(..., description="Auto-injected from request.user.id")


class FarmOrgUserInfoRequest(BaseModel):
    farm_org_user_id: Optional[int] = None
    com_org_id: Optional[int] = None
    user_id: Optional[int] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    is_active: Optional[bool] = None
    modified_by: Optional[int] = None
    start_record : Optional[int] = None
    page_size: Optional[int] = None
    by_user_id: int = Field(..., description="Auto-injected from request.user.id")


