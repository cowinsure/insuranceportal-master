from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render, redirect

from authservice.models import User, Role, UserPersonalInfo, UserFinancialInfo, UserNomineeInfo
from insuranceportal.utils import enterprise_required, is_enterprise_agent


@login_required
@user_passes_test(enterprise_required)
def dashboard(request):
    context = {}
    return render(request, 'pages/enterprise/dashboard.html', context)

@login_required
@user_passes_test(is_enterprise_agent)
def agent_dashboard(request):
    context = {}
    return render(request, 'pages/enterprise/agent/dashboard.html', context)


@login_required
@user_passes_test(enterprise_required)
def users_list(request):
    user = User.objects.filter(parent_enterprise=request.user)
    return render(request, 'pages/enterprise/user/user_list.html', {'user': user})


@login_required
@user_passes_test(enterprise_required)
def create_farmer(request):
    if request.method == "POST":
        # Get form data
        mobile_number = request.POST.get('mobile_number')
        password = request.POST.get('password')

        # User Personal Info
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        thana = request.POST.get('thana')
        union = request.POST.get('union')
        village = request.POST.get('village')
        zilla = request.POST.get('zilla')

        nid = request.POST.get('nid')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        tin = request.POST.get('tin')

        # Financial Info
        bank_name = request.POST.get('bank_name')
        branch_name = request.POST.get('branch_name')
        account_name = request.POST.get('account_name')
        account_number = request.POST.get('account_number')

        # Nominee Info
        nominee_name = request.POST.get('nominee_name')
        nominee_phone = request.POST.get('nominee_phone')
        nominee_email = request.POST.get('nominee_email')
        nominee_nid = request.POST.get('nominee_nid')

        # Handle file uploads for profile image and NID images
        profile_image = request.FILES.get('profile_image')
        nid_front = request.FILES.get('nid_front')
        nid_back = request.FILES.get('nid_back')

        # Check if role_id exists in the Role model
        try:
            role = Role.objects.get(name='Farmer')
        except Role.DoesNotExist:
            return JsonResponse({'error': 'Invalid role'}, status=400)

        # Create the user
        user = User.objects.create(
            mobile_number=mobile_number,
            role=role,
            password=make_password(password),
            onboarded_by_id=request.user.id,
            parent_enterprise=request.user,
        )

        UserPersonalInfo.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,

            thana=thana,
            union=union,
            village=village,
            zilla=zilla,

            nid=nid,
            date_of_birth=date_of_birth,
            gender=gender,
            tin=tin,
            profile_image=profile_image,
            nid_front=nid_front,
            nid_back=nid_back
        )
        UserFinancialInfo.objects.create(user=user, bank_name=bank_name, branch_name=branch_name,
                                         account_name=account_name, account_number=account_number)
        UserNomineeInfo.objects.create(user=user, nominee_name=nominee_name, phone=nominee_phone, email=nominee_email,
                                       nid=nominee_nid)

        messages.success(request, 'User created successfully!')
        # Redirect to the user list
        return redirect('enterprise_service:dashboard')

    else:
        return render(request, 'pages/enterprise/user/create_user.html')

@login_required
@user_passes_test(enterprise_required)
def create_staff(request):
    if request.method == "POST":
        # Get form data
        mobile_number = request.POST.get('mobile_number')
        password = request.POST.get('password')

        # User Personal Info
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        thana = request.POST.get('thana')
        union = request.POST.get('union')
        village = request.POST.get('village')
        zilla = request.POST.get('zilla')
        nid = request.POST.get('nid')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')
        profile_image = request.FILES.get('profile_image')
        nid_front = request.FILES.get('nid_front')
        nid_back = request.FILES.get('nid_back')

        # Create the user
        user = User.objects.create(
            mobile_number=mobile_number,
            password=make_password(password),
            onboarded_by_id=request.user.id,
            parent_enterprise=request.user,
            is_enterprise_agent=True
        )

        UserPersonalInfo.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,

            thana=thana,
            union=union,
            village=village,
            zilla=zilla,

            nid=nid,
            date_of_birth=date_of_birth,
            gender=gender,
            profile_image=profile_image,
            nid_front=nid_front,
            nid_back=nid_back
        )

        messages.success(request, 'User created successfully!')
        # Redirect to the user list
        return redirect('enterprise_service:dashboard')

    else:
        return render(request, 'pages/enterprise/user/create_enterprise_agent.html')