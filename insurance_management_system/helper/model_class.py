from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field


class FarmersInfoRequest(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    asset_status_id: Optional[int] = None
    start_record : Optional[int] = None
    page_size: Optional[int] = None
    by_user_id: int = Field(..., description="Auto-injected from request.user.id")


class InsuranceApplicationRequest(BaseModel):
    id: Optional[int] = None
    insurance_number: Optional[str] = None
    sum_insured: Optional[float] = None
    premium_amount: Optional[float] = None
    insurance_start_date: Optional[date] = None
    insurance_end_date: Optional[date] = None
    insurance_status: Optional[str] = None
    policy_terms: Optional[str] = None
    insurance_certificate: Optional[str] = None
    insurance_agent: Optional[str] = None
    renewal_reminder_sent: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    remarks: Optional[str] = None
    asset_id: Optional[int] = None
    created_by_id: Optional[int] = None
    updated_by_id: Optional[int] = None
    insurance_provider_id: Optional[int] = None
    is_claimed: Optional[bool] = None
    insurance_product_id: Optional[int] = None
    view_count: Optional[int] = None
    start_record : Optional[int] = None
    page_size: Optional[int] = None    
    current_status_id: Optional[int] = None 
    by_user_id: int = Field(..., description="Auto-injected from request.user.id")


class InsuranceProductRequest(BaseModel):
    id: Optional[int] = None
    premium_percentage: Optional[float] = None
    insurance_period_id: Optional[int] = None
    insurance_type_id: Optional[int] = None
    insurance_category_id: Optional[int] = None
    insurance_company_id: Optional[int] = None
    start_record : Optional[int] = None
    page_size: Optional[int] = None   
    by_user_id: int = Field(..., description="Auto-injected from request.user.id")  


class InsuranceStatusRequest(BaseModel):
    insurance_status_id: Optional[int] = None
    status_name: Optional[str] = None
    is_active: Optional[bool] = None
    created_by: Optional[int] = None
    created_at: Optional[datetime] = None
    modified_by: Optional[int] = None
    modified_at: Optional[datetime] = None
    by_user_id: int = Field(..., description="Auto-injected from request.user.id")                


class InsurancePaymentInformationRequest(BaseModel):
    id: Optional[int] = None
    trx_id: Optional[str] = None
    trx_date: Optional[date] = None
    trx_type: Optional[str] = None
    trx_through: Optional[str] = None
    created_at: Optional[datetime] = None
    remarks: Optional[str] = None
    asset_insurance_id: Optional[int] = None
    created_by_id: Optional[int] = None
    amount: Optional[float] = None
    by_user_id: int = Field(..., description="Auto-injected from request.user.id")  

class InsuranceClaimInformationRequest(BaseModel):
    id: Optional[int] = None
    claim_date: Optional[date] = None
    reason: Optional[str] = None
    amount_claimed: Optional[float] = None
    amount_approved: Optional[float] = None
    claim_status: Optional[str] = None
    rejection_reason: Optional[str] = None
    processed_date: Optional[date] = None
    settlement_documents: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    remarks: Optional[str] = None
    asset_insurance_id: Optional[int] = None
    created_by_id: Optional[int] = None
    updated_by_id: Optional[int] = None
    claim_muzzle: Optional[str] = None
    insured_asset_id: Optional[int] = None
    reference_id: Optional[str] = None
    by_user_id: int = Field(..., description="Auto-injected from request.user.id")         

class InsuranceStatusHistoryRequest(BaseModel):
    insurance_status_id: Optional[int] = None
    status_name: Optional[str] = None
    asset_insurance_id : Optional[int] = None
    by_user_id: int = Field(..., description="Auto-injected from request.user.id")  
