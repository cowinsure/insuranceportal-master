from rest_framework import permissions


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

def superuser_required(user):
    return user.is_authenticated and user.is_superuser
def is_insurecow_agent(user):
    return user.is_authenticated and user.is_insurecow_agent

def enterprise_required(user):
    return user.is_authenticated and user.role.name == 'Enterprise'

def is_enterprise_agent(user):
    return user.is_authenticated and user.is_enterprise_agent

def insurance_company_required(user):
    return user.is_authenticated and user.role.name == 'Insurance Company'

def is_insurance_agent(user):
    return user.is_authenticated and user.is_insurance_agent