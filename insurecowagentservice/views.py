from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

from insuranceportal.utils import is_insurecow_agent


@login_required
@user_passes_test(is_insurecow_agent)
def dashboard(request):
    context = {}
    return render(request, 'pages/insurecow_agent/dashboard.html',context)
