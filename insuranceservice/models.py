import uuid
from datetime import date, timedelta
from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError

from assetservice.models import Asset


class InsuranceCompany(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="insurance_company")
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logo/')

    def __str__(self):
        return self.name


class InsuranceCategory(models.Model):
    company = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE, related_name="insurance_categories")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class InsuranceType(models.Model):
    category = models.ForeignKey(InsuranceCategory, on_delete=models.CASCADE, related_name="insurance_types")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class InsurancePeriod(models.Model):
    type = models.ForeignKey(InsuranceType, on_delete=models.CASCADE, related_name="insurance_periods")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PremiumPercentage(models.Model):
    insurance_period = models.ForeignKey(InsurancePeriod, on_delete=models.CASCADE, related_name="premium_percentages")
    percentage = models.FloatField(help_text="Premium as percentage of asset value annually")

    def __str__(self):
        return f" {self.percentage}% per {self.insurance_period.name}"

class InsuranceProduct(models.Model):
    insurance_company = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE, related_name="insurance_products")
    insurance_category = models.ForeignKey(InsuranceCategory, on_delete=models.CASCADE, related_name="insurance_products")
    insurance_type = models.ForeignKey(InsuranceType, on_delete=models.CASCADE, related_name="insurance_products")
    insurance_period = models.ForeignKey(InsurancePeriod, on_delete=models.CASCADE, related_name="insurance_products")
    premium_percentage = models.FloatField()

    def __str__(self):
        return f"{self.insurance_type.name} - {self.insurance_period.name} ({self.premium_percentage}%)"

class InsuranceStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    UNDER_REVIEW = 'under_review', 'Under Review'
    ADDITIONAL_INFO_REQUIRED = 'additional_info_required', 'Additional Info Required'
    APPROVED = 'application_approved', 'Application Approved'
    REJECTED = 'rejected', 'Rejected'

    # Payment & Billing Status
    PAYMENT_PENDING = 'payment_pending', 'Payment Pending'
    PAID = 'paid', 'Paid'
    PAYMENT_VERIFIED = 'payment_verified', 'Payment Verified'
    PAYMENT_FAILED = 'payment_failed', 'Payment Failed'
    REFUNDED = 'refunded', 'Refunded'

    PENDING_PAYMENT_VERIFICATION = 'pending_payment_verification', 'Pending Payment Verification'
    # Policy Lifecycle
    ACTIVE = 'active', 'Active'
    PENDING_ACTIVATION = 'pending_activation', 'Pending Activation'
    IN_GRACE_PERIOD = 'in_grace_period', 'In Grace Period'
    SUSPENDED = 'suspended', 'Suspended'
    LAPSED = 'lapsed', 'Lapsed'
    EXPIRED = 'expired', 'Expired'
    RENEWAL_DUE = 'renewal_due', 'Renewal Due'
    RENEWED = 'renewed', 'Renewed'

    # Termination & Cancellation
    CANCELLED = 'cancelled', 'Cancelled'
    CANCELLATION_REQUESTED = 'cancellation_requested', 'Cancellation Requested'
    TERMINATED = 'terminated', 'Terminated'
    VOIDED = 'voided', 'Voided'

    # Compliance & Verification
    KYC_PENDING = 'kyc_pending', 'KYC Pending'
    KYC_VERIFIED = 'kyc_verified', 'KYC Verified'
    DOCUMENTS_PENDING = 'documents_pending', 'Documents Pending'
    FRAUD_SUSPECTED = 'fraud_suspected', 'Fraud Suspected'
    AUDIT_REQUIRED = 'audit_required', 'Audit Required'


class AssetInsurance(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="insurances")
    insurance_provider = models.ForeignKey(InsuranceCompany, on_delete=models.SET_NULL, null=True, blank=True)
    insurance_number = models.CharField(max_length=100, unique=True, blank=True)
    sum_insured = models.DecimalField(max_digits=10, decimal_places=2)
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    view_count = models.PositiveIntegerField(default=0)
    insurance_product = models.ForeignKey(InsuranceProduct, on_delete=models.CASCADE, related_name="asset_insurances")

    insurance_start_date = models.DateField(blank=True, null=True)
    insurance_end_date = models.DateField(blank=True, null=True)
    insurance_status = models.CharField(max_length=255, choices=InsuranceStatus.choices, default=InsuranceStatus.PENDING)

    policy_terms = models.TextField(blank=True, null=True)
    insurance_certificate = models.FileField(upload_to='asset/insurance_certificates/', blank=True, null=True)
    insurance_agent = models.CharField(max_length=255, blank=True, null=True)

    renewal_reminder_sent = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="asset_insurance_created"
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="asset_insurance_updated"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    remarks = models.TextField(blank=True, null=True)
    is_claimed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Insurance {self.insurance_number} for Asset ID {self.asset.id}"

    @property
    def is_currently_active(self):
        today = date.today()
        return self.insurance_start_date <= today <= self.insurance_end_date and self.insurance_status == InsuranceStatus.ACTIVE

    @property
    def days_until_expiry(self):
        if self.insurance_end_date:
            return (self.insurance_end_date - date.today()).days
        return None

    def save(self, *args, **kwargs):
        # Auto-generate the insurance number if not already set
        if not self.insurance_number:
            current_time = uuid.uuid4().hex[:8]  #
            self.insurance_number = f"INC-{current_time}"

        # Populate insurance data based on the selected product
        if self.insurance_product:
            self.insurance_provider = self.insurance_product.insurance_company

            # Auto-calculate the premium amount
            self.premium_amount = (self.sum_insured * Decimal(str(self.insurance_product.premium_percentage))) / 100

            # Set start date as today if not already set
            if not self.insurance_start_date:
                self.insurance_start_date = date.today()

            # Calculate end date based on the insurance period
            period_name = self.insurance_product.insurance_period.name.lower()

            # Determine the period length (e.g., "12 Month")
            period_parts = period_name.split()
            if len(period_parts) == 2 and period_parts[1] in ["month", "months"]:
                months = int(period_parts[0])
                self.insurance_end_date = self.insurance_start_date + relativedelta(months=months)
            elif len(period_parts) == 2 and period_parts[1] in ["year", "years"]:
                years = int(period_parts[0])
                self.insurance_end_date = self.insurance_start_date + relativedelta(years=years)
            elif len(period_parts) == 2 and period_parts[1] in ["day", "days"]:
                days = int(period_parts[0])
                self.insurance_end_date = self.insurance_start_date + timedelta(days=days)
        if self.view_count > 0 and self.insurance_status == InsuranceStatus.PENDING:
            self.insurance_status = InsuranceStatus.UNDER_REVIEW
        super().save(*args, **kwargs)

class ClaimDocument(models.Model):
    asset_insurance = models.ForeignKey(AssetInsurance, on_delete=models.CASCADE, related_name="claim_documents")
    file_name = models.CharField(max_length=100)
    file = models.FileField(upload_to='asset/claim_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for Insurance ID {self.asset_insurance.id}"
class InsuranceClaim(models.Model):
    class ClaimStatus(models.TextChoices):
        CLAIM_PENDING = 'claim_pending', 'Claim Pending'
        CLAIM_IN_REVIEW = 'claim_in_review', 'Claim In Review'
        CLAIM_APPROVED = 'claim_approved', 'Claim Approved'
        CLAIM_REJECTED = 'claim_rejected', 'Claim Rejected'
        CLAIM_SETTLED = 'claim_settled', 'Claim Settled'

    asset_insurance = models.ForeignKey(AssetInsurance, on_delete=models.CASCADE, related_name="claims")
    claim_date = models.DateField(auto_now_add=True)
    reason = models.TextField()
    amount_claimed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amount_approved = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    claim_status = models.CharField(max_length=20, choices=ClaimStatus.choices, default=ClaimStatus.CLAIM_PENDING)
    claim_muzzle = models.ImageField(upload_to='claims/claim_muzzle/', blank=True, null=True)
    claim_documents = models.ManyToManyField(ClaimDocument, blank=True, related_name="claims")
    rejection_reason = models.TextField(blank=True, null=True)
    processed_date = models.DateField(blank=True, null=True)
    settlement_documents = models.FileField(upload_to='asset/settlement_documents/', blank=True, null=True)
    insured_asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="claims", blank=True)
    reference_id = models.TextField(unique=True, null=False, blank=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="insurance_created"
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="insurance_updated"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    remarks = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Claim {self.id} for Insurance {self.asset_insurance.insurance_number}"

    def save(self, *args, **kwargs):
        if self.asset_insurance:
            self.insured_asset = self.asset_insurance.asset
            asset_reference_id = self.asset_insurance.asset.reference_id
            if not asset_reference_id:
                raise ValidationError("The linked Asset does not have a reference_id.")

            # Check if the reference_id is already set and does not match
            if self.reference_id and self.reference_id != asset_reference_id:
                raise ValidationError("The reference_id of the claim must match the asset's reference_id.")

            # Set the reference_id to ensure consistency
            self.reference_id = asset_reference_id
        else:
            raise ValidationError("AssetInsurance must be provided to save an InsuranceClaim.")

        super().save(*args, **kwargs)


from django.db import models
from django.conf import settings
class PaymentInformation(models.Model):
    TRX_TYPE_CHOICES = [
        ('cash', 'Cash'),
        ('bank', 'Bank Transfer'),
        ('MFS', 'MFS'),
        ('cheque', 'Cheque'),
        ('other', 'Other'),
    ]

    trx_id = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=6, max_digits=20)
    trx_date = models.DateField()
    trx_type = models.CharField(max_length=20, choices=TRX_TYPE_CHOICES)
    trx_through = models.CharField(max_length=100)
    assetInsuranceId = models.ForeignKey(AssetInsurance, on_delete=models.CASCADE, related_name="insurance_payments")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='payments_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('trx_id', 'amount', 'trx_through','assetInsuranceId')  # ensures uniqueness on this pair
        ordering = ['-created_at']  # optional: newest first

    def __str__(self):
        return f"Transaction {self.trx_id} via {self.trx_through} on {self.trx_date} amount of {self.amount}"


def trx_document_upload_path(instance, filename):
    return f"trx_documents/{instance.payment.trx_id}/{filename}"


class TransactionDocument(models.Model):
    payment = models.ForeignKey(
        PaymentInformation,
        on_delete=models.CASCADE,
        related_name='trx_documents'
    )
    document = models.FileField(upload_to=trx_document_upload_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.payment.trx_id}"

@receiver(post_save, sender=PaymentInformation)
def update_insurance_status_on_payment(sender, instance, created, **kwargs):
    if created:
        try:
            insurance = instance.assetInsuranceId
            insurance.insurance_status = InsuranceStatus.PENDING_PAYMENT_VERIFICATION
            insurance.save()
            print(f"[SIGNAL] Updated insurance {insurance.id} status to PENDING_PAYMENT_VERIFICATION")
        except Exception as e:
            print(f"[SIGNAL ERROR] Failed to update insurance status: {e}")

@receiver(post_save, sender=PremiumPercentage)
def create_or_update_insurance_product(sender, instance, created, **kwargs):
    insurance_type = instance.insurance_period.type
    insurance_category = insurance_type.category
    insurance_company = insurance_category.company

    # Create or update the InsuranceProduct
    InsuranceProduct.objects.update_or_create(
        insurance_company=insurance_company,
        insurance_category=insurance_category,
        insurance_type=insurance_type,
        insurance_period=instance.insurance_period,
        defaults={'premium_percentage': instance.percentage}
    )