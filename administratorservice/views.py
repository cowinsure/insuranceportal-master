from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.timezone import now

from assetservice.models import AssetType, Breed, Color, VaccinationStatus, DewormingStatus, Asset
from authservice.models import Role, User, UserPersonalInfo, UserFinancialInfo, UserNomineeInfo, OrganizationInfo, \
    OTPVerification
from insuranceportal.utils import superuser_required
from insuranceservice.models import InsuranceCompany, AssetInsurance
from user_management_system.helper.model_class import AuthUserModuleAccessRequest
from user_management_system.helper.user_management_helper_class import add_auth_module_access, get_auth_module_access


@login_required
@user_passes_test(superuser_required)
def dashboard(request):
    # Get the current date
    current_date = now().date()

    # Get today's user count
    user_count = User.objects.count()

    # Get yesterday's date
    previous_date = current_date - timedelta(days=1)

    # Calculate user count up to the previous date
    previous_count = User.objects.filter(date_joined__lt=previous_date).count()

    # Calculate growth percentage
    if previous_count > 0:
        growth_percentage = round(((user_count - previous_count) / previous_count) * 100, 2)
    else:
        growth_percentage = 100.0 if user_count > 0 else 0.0
    farmer = 'Farmer'
    farmer_count = User.objects.filter(role__name=farmer).count()

    # Calculate farmer count up to the previous date
    previous_count = User.objects.filter(date_joined__lt=previous_date).count()

    # Calculate growth percentage
    if previous_count > 0:
        growth_percentage = round(((farmer_count - previous_count) / previous_count) * 100, 2)
    else:
        growth_percentage = 100.0 if farmer_count > 0 else 0.0

    total_assets = Asset.objects.count()

    # Get yesterday's date
    previous_date = current_date - timedelta(days=1)

    # Calculate asset count up to the previous date
    previous_count = Asset.objects.filter(created_at__lt=previous_date).count()

    # Calculate growth percentage
    if previous_count > 0:
        growth_percentage = round(((total_assets - previous_count) / previous_count) * 100, 2)
    else:
        growth_percentage = 100.0 if total_assets > 0 else 0.0

    total_asset_insurance = AssetInsurance.objects.count()

    # Get yesterday's date
    previous_date = current_date - timedelta(days=1)

    # Calculate asset insurance count up to the previous date
    previous_count = AssetInsurance.objects.filter(created_at__lt=previous_date).count()

    # Calculate growth percentage
    if previous_count > 0:
        growth_percentage = round(((total_asset_insurance - previous_count) / previous_count) * 100, 2)
    else:
        growth_percentage = 100.0 if total_asset_insurance > 0 else 0.0

    context = {
        'total_asset_insurance': total_asset_insurance,
        'insurance_growth_percentage': growth_percentage,
        'total_assets': total_assets,
        'asset_growth_percentage': growth_percentage,
        'farmer_count': farmer_count,
        'farmer_growth_percentage': growth_percentage,
        'user_count': user_count,
        'user_growth_percentage': growth_percentage,
    }
    return render(request, 'pages/administrator/dashboard.html', context)





@login_required
@user_passes_test(superuser_required)
def roles_list(request):
    roles = Role.objects.all()
    return render(request, 'pages/administrator/roles/roles_list.html', {'roles': roles})

@login_required
@user_passes_test(superuser_required)
def otp_list(request):
    otp = OTPVerification.objects.all().order_by('-created_at')
    return render(request, 'pages/administrator/otp/otp_list.html', {'otp': otp})


@login_required
@user_passes_test(superuser_required)
def asset_type_list(request):
    asset_type = AssetType.objects.all()
    return render(request, 'pages/administrator/asset_type/asset_type_list.html', {'asset_type': asset_type})

@login_required
@user_passes_test(superuser_required)
def breed_list(request):
    breed_list = Breed.objects.all()
    return render(request, 'pages/administrator/breed/breed_list_list.html', {'breed_list': breed_list})


@login_required
@user_passes_test(superuser_required)
def color_list(request):
    color_list = Color.objects.all()
    return render(request, 'pages/administrator/color/color_list.html', {'color_list': color_list})


@login_required
@user_passes_test(superuser_required)
def vaccination_status_list(request):
    vaccination_status_list = VaccinationStatus.objects.all()
    return render(request, 'pages/administrator/vaccination_status/vaccination_status_list.html', {'vaccination_status_list': vaccination_status_list})


@login_required
@user_passes_test(superuser_required)
def deworming_status_list(request):
    deworming_status_list = DewormingStatus.objects.all()
    return render(request, 'pages/administrator/deworming_status/deworming_status_list.html', {'deworming_status_list': deworming_status_list})


@login_required
@user_passes_test(superuser_required)
def create_roles(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        is_active = request.POST.get('is_active') == 'on'  # Assuming a checkbox is used for the 'is_active' field

        if name:  # Basic validation to check if name is provided
            role = Role.objects.create(name=name, is_active=is_active)
            messages.success(request, 'Role created successfully.')
            return redirect('administrator_service:roles_list')
        else:
            messages.error(request, 'Name field is required.')

    return render(request, 'pages/administrator/roles/create_role.html')

@login_required
@user_passes_test(superuser_required)
def create_asset_type(request):
    if request.method == 'POST':
        name = request.POST.get('name')

        if name:  # Basic validation to check if name is provided
            asset_type = AssetType.objects.create(name=name)
            messages.success(request, 'Asset Type created successfully.')
            return redirect('administrator_service:asset_type_list')
        else:
            messages.error(request, 'Name field is required.')

    return render(request, 'pages/administrator/asset_type/create_asset_type.html')

@login_required
@user_passes_test(superuser_required)
def create_breed(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        if name:  # Basic validation to check if name is provided
            create_breed = Breed.objects.create(name=name)
            messages.success(request, 'Breed created successfully.')
            return redirect('administrator_service:breed_list')
        else:
            messages.error(request, 'Name field is required.')

    return render(request, 'pages/administrator/breed/create_breed.html')


@login_required
@user_passes_test(superuser_required)
def create_color(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        if name:  # Basic validation to check if name is provided
            create_color = Color.objects.create(name=name, description=description)
            print(create_color)
            messages.success(request, 'Color created successfully.')
            return redirect('administrator_service:color_list')
        else:
            messages.error(request, 'Name field is required.')

    return render(request, 'pages/administrator/color/create_color.html')

@login_required
@user_passes_test(superuser_required)
def create_vaccination_status(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        if name:  # Basic validation to check if name is provided
            create_vaccination_status = VaccinationStatus.objects.create(name=name, description=description)
            messages.success(request, 'Vaccination status created successfully.')
            return redirect('administrator_service:vaccination_status_list')
        else:
            messages.error(request, 'Name field is required.')

    return render(request, 'pages/administrator/vaccination_status/create_vaccination_status.html')

@login_required
@user_passes_test(superuser_required)
def create_deworming_status(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        if name:  # Basic validation to check if name is provided
            create_deworming_status = DewormingStatus.objects.create(name=name, description=description)
            messages.success(request, 'Deworming status created successfully.')
            return redirect('administrator_service:deworming_status_list')
        else:
            messages.error(request, 'Name field is required.')

    return render(request, 'pages/administrator/deworming_status/create_deworming_status.html')


@login_required
@user_passes_test(superuser_required)
def users_list(request):
    user = User.objects.all()
    return render(request, 'pages/administrator/user/user_list.html', {'user': user})

@login_required
@user_passes_test(superuser_required)
def create_user(request):
    if request.method == "POST":
        # Get form data
        mobile_number = request.POST.get('mobile_number')
        password = request.POST.get('password')
        role_id = request.POST.get('role')

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
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return JsonResponse({'error': 'Invalid role'}, status=400)

        # Create the user
        user = User.objects.create(
            mobile_number=mobile_number,
            role=role,
            password=make_password(password),
            onboarded_by_id=request.user.id,
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


        if role.id in [2, 3]:
            OrganizationInfo.objects.create(
                user=user,
                name=request.POST.get('organization_name'),
                logo=request.FILES.get('organization_logo'),
                established=request.POST.get('organization_established'),
                tin=request.POST.get('organization_tin'),
                bin=request.POST.get('organization_bin')
            )
        if role.id in [3]:
            InsuranceCompany.objects.create(
                user=user,
                name=request.POST.get('organization_name'),
                logo=request.FILES.get('organization_logo'),
            )

        messages.success(request, 'User created successfully!')
        # Redirect to the user list
        return redirect('administrator_service:dashboard')

    else:
        # GET method to load roles and display the user creation form
        roles = Role.objects.all()
        return render(request, 'pages/administrator/user/create_user.html', {'roles': roles})
@login_required
@user_passes_test(superuser_required)
def create_insurecow_agent(request):
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
            is_insurecow_agent=True,
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
        return redirect('administrator_service:dashboard')

    else:
        # GET method to load roles and display the user creation form
        roles = Role.objects.all()
        return render(request, 'pages/administrator/user/create_insurecow_agent.html', {'roles': roles})
    

@login_required
@user_passes_test(superuser_required)
def user_module_access_list(request):
    # Prepare the request payload for permission check
    record = AuthUserModuleAccessRequest(
        by_user_id=-1,
        module_code='-1',  # replace with your actual module code if needed
    )

    # Call the permission function
    permission_response = get_auth_module_access(record)

    # if permission_response['status'] != 'success':
    #     # Permission denied - show error or unauthorized page
    #     return render(request, 'pages/unauthorized.html', {
    #         'message': permission_response.get('message', 'Permission denied')
    #     })

    # Permission granted - load actual data from permission_response['data']
    user_module_access_list = permission_response['data']

    return render(request, 'pages/administrator/user_module_access/user_module_access_list.html', {
        'user_module_access_list': user_module_access_list,
        'permissions': permission_response['data'],  # optional
    })


@login_required
@user_passes_test(superuser_required)
def create_user_module_access(request):
    user = User.objects.all()

    if request.method == 'POST':
        try:
            user = request.POST.get('user')  # optional, not used in logic
            module = request.POST.get('module')  # optional

            record = AuthUserModuleAccessRequest(
                by_user_id=request.user.id,
                user_id=user,         
                module_code=module    
            )

            # Call DB function
            permission_response = add_auth_module_access(record)

            if permission_response['status'] == 'success':
                messages.success(request, 'Module access created successfully.')
                return redirect('administrator_service:user_module_access_list')  # adjust URL name
            else:
                messages.error(request, permission_response.get('message', 'Failed to create access.'))

        except Exception as e:
            messages.error(request, f"Error occurred: {str(e)}")

    return render(request, 'pages/administrator/user_module_access/create_user_module_access.html', {'user': user})