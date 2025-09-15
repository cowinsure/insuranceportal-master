from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AuthUserModuleAccessRequest(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    module_code: Optional[str] = None
    is_active: Optional[bool] = None
    by_user_id: int = Field(..., description="Auto-injected from request.user.id")