from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404

from insuranceportal.utils import insurance_company_required
from insuranceservice.models import InsuranceCategory, InsuranceType, InsurancePeriod, PremiumPercentage, \
    AssetInsurance, PaymentInformation
from insuranceservice.serializers import PaymentInformationDetailSerializer


@login_required
def dashboard(request):
    context = {}
    return render(request, 'pages/insurance_company/dashboard.html', context)


@login_required
@user_passes_test(insurance_company_required)
def insurance_category_list(request):
    insurance_company = request.user.insurance_company
    insurance_categories = InsuranceCategory.objects.filter(company=insurance_company)
    return render(request, 'pages/insurance_company/InsuranceCategory/insurance_category_list.html', {'insurance_categories': insurance_categories})

@login_required
@user_passes_test(insurance_company_required)
def view_insurance_application(request, pk):
    application = get_object_or_404(AssetInsurance, pk=pk)
    application.view_count += 1
    application.save()
    # Redirect or render a detailed view
    return redirect('insurance_company_service:insurance_application_detail', pk=pk)

@login_required
@user_passes_test(insurance_company_required)
def insurance_application_list(request):
    insurance_company = request.user.insurance_company
    insurance_application = AssetInsurance.objects.filter(insurance_provider=insurance_company)
    return render(request, 'pages/insurance_company/InsuranceApplication/insurance_application_list.html', {'insurance_application': insurance_application})

@login_required
@user_passes_test(insurance_company_required)
def update_insurance_status(request, pk):
    insurance = get_object_or_404(AssetInsurance, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('insurance_status')
        if new_status:
            insurance.insurance_status = new_status
            insurance.save()
    return redirect('insurance_company_service:insurance_application_detail', pk=pk)
def insurance_application_detail(request, pk):
    insurance_application = get_object_or_404(AssetInsurance, pk=pk)
    status_choices = AssetInsurance._meta.get_field('insurance_status').choices

    # Filter out 'under_review' and 'pending' if current status is 'under_review'
    if insurance_application.insurance_status == 'under_review':
        status_choices = [(k, v) for k, v in status_choices if k not in ('under_review', 'pending')]
    if insurance_application.insurance_status == 'approved':
        status_choices = [(k, v) for k, v in status_choices if k not in ('under_review', 'pending','approved')]
    return render(request, 'pages/insurance_company/InsuranceApplication/insurance_application_detail.html', {'insurance_application': insurance_application,
        'status_choices': status_choices,})

@login_required
@user_passes_test(insurance_company_required)
def create_insurance_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        if name:
            insurance_company = request.user.insurance_company
            InsuranceCategory.objects.create(company=insurance_company, name=name, description=description)
            messages.success(request, 'Insurance category created successfully.')
            return redirect('insurance_company_service:InsuranceCategory_list')
        else:
            messages.error(request, 'Name field is required.')

    return render(request, 'pages/insurance_company/InsuranceCategory/create_insurance_category.html')


@login_required
@user_passes_test(insurance_company_required)
def insurance_type_list(request):
    # Retrieve only the insurance types of the logged-in company
    insurance_company = request.user.insurance_company
    insurance_types = InsuranceType.objects.filter(category__company=insurance_company)
    return render(request, 'pages/administrator/InsuranceType/insurance_type_list.html', {'insurance_types': insurance_types})

@login_required
@user_passes_test(insurance_company_required)
def create_insurance_type(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')

        if name and category_id:  # Validate that name and category are provided
            insurance_company = request.user.insurance_company
            try:
                category = InsuranceCategory.objects.get(id=category_id, company=insurance_company)
                InsuranceType.objects.create(category=category, name=name, description=description)
                messages.success(request, 'Insurance type created successfully.')
                return redirect('insurance_company_service:insurance_type_list')
            except InsuranceCategory.DoesNotExist:
                messages.error(request, 'Selected category does not exist or does not belong to your company.')
        else:
            messages.error(request, 'Name and category fields are required.')

    # Retrieve all categories for the logged-in company to populate the dropdown
    insurance_company = request.user.insurance_company
    categories = InsuranceCategory.objects.filter(company=insurance_company)

    return render(request, 'pages/administrator/InsuranceType/create_insurance_type.html', {'categories': categories})

@login_required
@user_passes_test(insurance_company_required)
def insurance_period_list(request):
    # Retrieve insurance periods for the logged-in company
    insurance_company = request.user.insurance_company
    insurance_periods = InsurancePeriod.objects.filter(type__category__company=insurance_company)
    return render(request, 'pages/administrator/InsurancePeriod/insurance_period_list.html', {'insurance_periods': insurance_periods})

@login_required
@user_passes_test(insurance_company_required)
def create_insurance_period(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        type_id = request.POST.get('type')

        if name and type_id:  # Validate that name and category are provided
            insurance_company = request.user.insurance_company
            try:
                type = InsuranceType.objects.get(id=type_id, category__company=insurance_company)
                InsurancePeriod.objects.create(type=type, name=name)
                messages.success(request, 'Insurance period created successfully.')
                return redirect('insurance_company_service:insurance_period_list')
            except InsuranceCategory.DoesNotExist:
                messages.error(request, 'Selected category does not exist or does not belong to your company.')
        else:
            messages.error(request, 'Name and category fields are required.')

    # Retrieve all categories for the logged-in company to populate the dropdown
    insurance_company = request.user.insurance_company
    types = InsuranceType.objects.filter(category__company=insurance_company)

    return render(request, 'pages/administrator/InsurancePeriod/create_insurance_period.html', {'types': types})


@login_required
@user_passes_test(insurance_company_required)
def insurance_premium_percentage_list(request):
    # Retrieve the insurance company associated with the logged-in user
    insurance_company = request.user.insurance_company

    # Filter the PremiumPercentage by the insurance periods belonging to the insurance company
    premium_percentages = PremiumPercentage.objects.filter(
        insurance_period__type__category__company=insurance_company
    )

    return render(request, 'pages/administrator/InsurancePeriod/insurance_premium_percentage_list.html', {
        'premium_percentages': premium_percentages
    })

@login_required
@user_passes_test(insurance_company_required)
def create_insurance_premium_percentage(request):
    if request.method == 'POST':
        insurance_period_id = request.POST.get('insurance_period')
        percentage = request.POST.get('percentage')

        if insurance_period_id and percentage:  # Validate that both fields are provided
            insurance_company = request.user.insurance_company
            try:
                insurance_period = InsurancePeriod.objects.get(id=insurance_period_id, type__category__company=insurance_company)
                PremiumPercentage.objects.create(insurance_period=insurance_period, percentage=float(percentage))
                messages.success(request, 'Premium percentage created successfully.')
                return redirect('insurance_company_service:insurance_premium_percentage_list')
            except InsurancePeriod.DoesNotExist:
                messages.error(request, 'Selected insurance period does not exist or does not belong to your company.')
        else:
            messages.error(request, 'Insurance period and percentage fields are required.')

    # Retrieve all insurance periods for the logged-in company to populate the dropdown
    insurance_company = request.user.insurance_company
    insurance_periods = InsurancePeriod.objects.filter(type__category__company=insurance_company)

    return render(request, 'pages/administrator/InsurancePeriod/create_insurance_premium_percentage.html', {'insurance_periods': insurance_periods})


@login_required
def payment_info_by_insurance(request, insurance_id):
    payments = PaymentInformation.objects.filter(assetInsuranceId=insurance_id).select_related('assetInsuranceId')
    insurance = get_object_or_404(AssetInsurance, id=insurance_id)

    context = {
        'payments': payments,
        'insurance': insurance,
    }
    return render(request, 'pages/administrator/InsurancePeriod/insurance_company_service/payment_info.html', context)