from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Model Class for SMS request
class SendSMSRequest(BaseModel):
    msisdn: Optional[list[str]] = None
    message: Optional[str] = None
    clienttransid: Optional[str] = None


class MsgSMSlogRequest(BaseModel):
    sms_log_id: Optional[int] = None
    message_id: Optional[str] = None
    message_body: Optional[str] = None
    mobile_no: Optional[str] = None
    person_id: Optional[int] = None
    amount: Optional[float] = None
    sms_flag: Optional[bool] = None
    sms_type: Optional[int] = None
    remarks: Optional[str] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None
    created_by: Optional[int] = None
    modified_by: Optional[int] = None
    record_updated_date: Optional[datetime] = None
    client_ref_id: Optional[str] = None
    server_ref_id: Optional[str] = None