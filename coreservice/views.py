from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render


@login_required
def entry_view(request):
    try:
        user = request.user
        if user.is_superuser:
            return redirect('administrator_service:dashboard')
        elif user.is_insurecow_agent:
            return redirect('insurecow_agent_service:dashboard')
        elif user.is_enterprise_agent:
            return redirect('enterprise_service:agent_dashboard')
        elif hasattr(user, 'role'):
            if user.role.name == 'Farmer':
                return redirect('core_service:dashboard')
            elif user.role.name == 'Enterprise':
                return redirect('enterprise_service:dashboard')
            elif user.role.name == 'Insurance Company':
                return redirect('insurance_company_service:dashboard')

        messages.success(request, 'Something went wrong!')
        return redirect('auth_service:login')

    except Exception as e:
        print(f"Error: {e}")
        return HttpResponse("Error: Unable to retrieve user details or redirect.", status=500)
# def entry_view(request):
#     return render(request,'pages/administrator/dashboard.html',context={})

@login_required
def dashboard(request):
    context = {}
    return render(request, 'pages/user/dashboard.html',context)
