

import json
from rest_framework.permissions import BasePermission
from django.db import connection
from common.common_class.util import _response
from db import call_db_function, get_db_connection
from user_management_system.helper.model_class import AuthUserModuleAccessRequest
from user_management_system.helper.user_management_helper_class import get_auth_module_access

class HasModuleAccess(BasePermission):

    '''
    # @ Author: Tanmay Anthony Gomes
    # @ Create Time: 14-Jul-2025 04:04:15 PM
    # @ Modified by: -
    # @ Modified time: 14-Jul-2025 04:16:37 PM
    # @ Description: Function for getting module access
    '''
    def has_permission(self, request, view):
        user = request.user
        required_module = getattr(view, 'required_module', None)
        
        if not required_module:
            return True  # No module restriction
        
        # Build record to call DB function
        record = AuthUserModuleAccessRequest(
            by_user_id=user.id,
            module_code=required_module
        )
        result = get_auth_module_access(record)
        
        # If it's a dict response from _response() → check status and data
        if result.get("status") != "success":
            return False

        if result.get("data") is None or result.get("data") == []:
            return False

        return True


    
