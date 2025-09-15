from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class GlsLedgersRequest(BaseModel):
    ledger_id: Optional[int] = None
    code: Optional[str] = None
    name_ledger: Optional[str] = None
    name_ledger_bangla: Optional[str] = None
    type: Optional[str] = None
    is_control_item: Optional[bool] = None
    is_cost_revinue_center: Optional[bool] = None
    is_product_line: Optional[bool] = None
    is_vendor: Optional[bool] = None
    is_customer: Optional[bool] = None
    sort: Optional[int] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    gls_organization_id: Optional[int] = None
    is_cash: Optional[bool] = None
    is_bank: Optional[bool] = None
    is_petty_cash: Optional[bool] = None
    is_petty_cash_expense: Optional[bool] = None
    is_ie_account: Optional[bool] = None
    is_bank_investment: Optional[bool] = None
    created_by: Optional[int] = None
    modified_by: Optional[int] = None
    ledger_activity: Optional[str] = None
    by_user_id: int = Field(..., description="Auto-injected from request.user.id")


class IncomeExpenseRequest(BaseModel):
    ledger_id: Optional[int] = None
    amount: Optional[int] = None
    txn_date: Optional[datetime] = None
    description: Optional[str] = None
    organization_id: Optional[int] = None
    branch_id: Optional[int] = None
    created_by: Optional[int] = None
    start_record : Optional[int] = None
    page_size: Optional[int] = None
    by_user_id: int = Field(..., description="Auto-injected from request.user.id")

class FMSDashboardRequest(BaseModel):
    start_record : Optional[int] = None
    page_size: Optional[int] = None
    by_user_id: int = Field(..., description="Auto-injected from request.user.id")    